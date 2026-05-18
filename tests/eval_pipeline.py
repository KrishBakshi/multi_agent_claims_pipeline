"""
tests/eval_pipeline.py

Runs all 12 test cases through the live pipeline and writes:
  - One Markdown report per case  →  experiments/output/evaluation/TC001_*.md
  - One summary roll-up           →  experiments/output/evaluation/00_summary.md
  - One combined log file         →  experiments/output/evaluation/eval_run.log

Usage:
    uv run python tests/eval_pipeline.py
    uv run python tests/eval_pipeline.py --output-dir experiments/output/evaluation
"""
from __future__ import annotations

import argparse
import io
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from src.core.logger import get_logger, setup_logging
from src.core.policy_loader import PolicyLoader
from src.models.claim import ClaimInput, ClaimsHistory, Document, DocumentContent, LineItem
from src.models.decision import DecisionOutput
from src.pipeline.graph import run_pipeline

setup_logging(console_level=logging.WARNING)  # suppress console noise during batch run

_log = get_logger("eval_pipeline")

TEST_CASES_PATH = ROOT / "tests" / "test_cases.json"
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "output" / "evaluation"

# ── badges ────────────────────────────────────────────────────────────────────

BADGE = {
    "APPROVED":      "🟢 APPROVED",
    "PARTIAL":       "🟡 PARTIAL",
    "REJECTED":      "🔴 REJECTED",
    "MANUAL_REVIEW": "🟠 MANUAL REVIEW",
    "STOPPED":       "🛑 STOPPED",
    None:            "🛑 STOPPED",
}

TRACE_ICON = {
    "PASS":    "✅",
    "FAIL":    "❌",
    "WARNING": "⚠️",
    "ERROR":   "🔥",
    "INFO":    "ℹ️",
}

# ── build ClaimInput from test-case dict (mirrors conftest.py) ─────────────────

def _build_claim(inp: dict) -> ClaimInput:
    docs = []
    for d in inp.get("documents", []):
        content_raw = d.get("content")
        content = None
        if content_raw:
            raw = dict(content_raw)
            if raw.get("line_items"):
                raw["line_items"] = [LineItem(**li) for li in raw["line_items"]]
            content = DocumentContent(**raw)
        docs.append(Document(
            file_id=d.get("file_id", ""),
            file_name=d.get("file_name"),
            actual_type=d.get("actual_type", ""),
            quality=d.get("quality", "GOOD"),
            patient_name_on_doc=d.get("patient_name_on_doc"),
            content=content,
        ))
    history = [ClaimsHistory(**h) for h in inp.get("claims_history", [])]
    return ClaimInput(
        member_id=inp["member_id"],
        policy_id=inp["policy_id"],
        claim_category=inp["claim_category"],
        treatment_date=inp["treatment_date"],
        claimed_amount=inp["claimed_amount"],
        documents=docs,
        hospital_name=inp.get("hospital_name"),
        ytd_claims_amount=inp.get("ytd_claims_amount", 0.0),
        claims_history=history,
        simulate_component_failure=inp.get("simulate_component_failure", False),
    )


# ── log capture ───────────────────────────────────────────────────────────────

class _StringHandler(logging.Handler):
    """Captures every log record emitted under the 'claims' hierarchy."""

    def __init__(self) -> None:
        super().__init__(level=logging.DEBUG)
        self.buf = io.StringIO()
        fmt = "%(asctime)s | %(levelname)-8s | %(name)-32s | [%(claim_id)-8s] %(message)s"

        class _ClaimIdFilter(logging.Filter):
            def filter(self, record):
                if not hasattr(record, "claim_id"):
                    record.claim_id = "--------"
                return True

        self.addFilter(_ClaimIdFilter())
        self.setFormatter(logging.Formatter(fmt, datefmt="%H:%M:%S"))

    def emit(self, record: logging.LogRecord) -> None:
        self.buf.write(self.format(record) + "\n")

    def getvalue(self) -> str:
        return self.buf.getvalue()


def _attach_capture() -> _StringHandler:
    handler = _StringHandler()
    logging.getLogger("claims").addHandler(handler)
    return handler


def _detach_capture(handler: _StringHandler) -> str:
    logging.getLogger("claims").removeHandler(handler)
    return handler.getvalue()


# ── verdict check ─────────────────────────────────────────────────────────────

def _verdict(tc: dict, result: DecisionOutput) -> tuple[bool, list[str]]:
    """Returns (passed, list_of_check_lines)."""
    exp = tc.get("expected", {})
    checks: list[str] = []
    passed = True

    exp_decision = exp.get("decision")  # None means STOPPED
    actual_decision = result.decision.value if result.decision else None

    # Decision match
    if exp_decision is None:
        ok = result.halt_message is not None or actual_decision is None
        checks.append(f"{'✅' if ok else '❌'} Pipeline stopped (no decision reached)")
        if not ok:
            passed = False
    else:
        ok = actual_decision == exp_decision
        checks.append(
            f"{'✅' if ok else '❌'} Decision: expected **{exp_decision}**, got **{actual_decision or 'None'}**"
        )
        if not ok:
            passed = False

    # Approved amount (within 1% tolerance)
    if exp.get("approved_amount") is not None and result.approved_amount is not None:
        exp_amt = float(exp["approved_amount"])
        act_amt = float(result.approved_amount)
        ok = abs(exp_amt - act_amt) <= max(1.0, exp_amt * 0.01)
        checks.append(
            f"{'✅' if ok else '❌'} Approved amount: expected ₹{exp_amt:,.0f}, "
            f"got ₹{act_amt:,.2f}"
        )
        if not ok:
            passed = False

    # Rejection reasons
    for reason in exp.get("rejection_reasons", []):
        ok = reason in result.rejection_reasons
        checks.append(
            f"{'✅' if ok else '❌'} Rejection reason **{reason}** present"
        )
        if not ok:
            passed = False

    # Confidence band
    conf_note = exp.get("confidence_score") or exp.get("confidence")
    if conf_note and "above" in str(conf_note):
        try:
            threshold = float(str(conf_note).replace("above", "").strip())
            ok = result.confidence_score >= threshold
            checks.append(
                f"{'✅' if ok else '❌'} Confidence ≥ {threshold:.0%} "
                f"(actual {result.confidence_score:.0%})"
            )
            if not ok:
                passed = False
        except ValueError:
            pass

    # system_must items — textual check (soft, non-failing)
    for must in exp.get("system_must", []):
        # Search for keywords from the must-statement in halt_message + reason
        combined = " ".join([
            result.halt_message or "",
            result.reason or "",
            *result.rejection_reasons,
            *[t.detail for t in result.trace],
        ]).lower()
        keywords = [w for w in must.lower().split() if len(w) > 4]
        hit = sum(1 for k in keywords if k in combined)
        ok = hit >= max(1, len(keywords) // 3)
        checks.append(f"{'✅' if ok else '⚠️ '} System must: _{must}_")

    return passed, checks


# ── markdown renderer ─────────────────────────────────────────────────────────

def _doc_summary(docs: list[dict]) -> str:
    parts = []
    for d in docs:
        name = d.get("file_name") or d.get("file_id", "?")
        q = d.get("quality", "GOOD")
        q_tag = f" ⚠️ `{q}`" if q != "GOOD" else ""
        parts.append(f"`{name}` ({d['actual_type']}{q_tag})")
    return " · ".join(parts)


def _render_report(
    tc: dict,
    result: DecisionOutput,
    logs: str,
    duration: float,
    run_ts: str,
) -> str:
    inp = tc["input"]
    exp = tc.get("expected", {})
    verdict, checks = _verdict(tc, result)

    decision_str = result.decision.value if result.decision else None
    outcome_key = decision_str or "STOPPED"
    outcome_badge = BADGE.get(outcome_key, outcome_key)

    lines: list[str] = []

    # ── header ────────────────────────────────────────────────────────────────
    lines += [
        f"# {tc['case_id']} — {tc['case_name']}",
        "",
        f"> {tc.get('description', '')}",
        "",
        f"**Claim ID:** `{result.claim_id}`  ",
        f"**Run:** {run_ts}  ",
        f"**Duration:** {duration:.2f}s",
        "",
        "---",
        "",
    ]

    # ── input ─────────────────────────────────────────────────────────────────
    lines += [
        "## Input",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Member ID | `{inp['member_id']}` |",
        f"| Claim Category | `{inp['claim_category']}` |",
        f"| Treatment Date | {inp['treatment_date']} |",
        f"| Claimed Amount | ₹{inp['claimed_amount']:,.0f} |",
        f"| Policy ID | `{inp['policy_id']}` |",
    ]
    if inp.get("hospital_name"):
        lines.append(f"| Hospital | {inp['hospital_name']} |")
    if inp.get("ytd_claims_amount"):
        lines.append(f"| YTD Claims | ₹{inp['ytd_claims_amount']:,.0f} |")
    if inp.get("simulate_component_failure"):
        lines.append("| Component Failure | ⚡ Simulated |")

    lines += ["", "**Documents submitted:**", ""]
    for d in inp.get("documents", []):
        name = d.get("file_name") or d.get("file_id", "—")
        q = d.get("quality", "GOOD")
        q_tag = f"  ⚠️ quality=`{q}`" if q != "GOOD" else ""
        patient = d.get("patient_name_on_doc", "")
        patient_tag = f"  👤 `{patient}`" if patient else ""
        lines.append(f"- `{name}`  type=`{d['actual_type']}`{q_tag}{patient_tag}")

    if inp.get("claims_history"):
        lines += ["", "**Claims history (same day):**", ""]
        for h in inp["claims_history"]:
            lines.append(f"- `{h['claim_id']}` — ₹{h['amount']:,.0f} at {h['provider']} on {h['date']}")

    lines += ["", "---", ""]

    # ── pipeline trace ────────────────────────────────────────────────────────
    lines += ["## Pipeline Trace", ""]
    if result.trace:
        lines += [
            "| # | Agent | Step | Result | Detail |",
            "|---|-------|------|--------|--------|",
        ]
        for i, t in enumerate(result.trace, 1):
            icon = TRACE_ICON.get(t.result, "•")
            detail = t.detail.replace("|", "\\|")
            lines.append(f"| {i} | `{t.agent}` | `{t.step}` | {icon} `{t.result}` | {detail} |")
    else:
        lines.append("_No trace entries recorded._")

    lines += ["", "---", ""]

    # ── decision ──────────────────────────────────────────────────────────────
    lines += [
        "## Decision",
        "",
        f"### {outcome_badge}",
        "",
        f"**Confidence:** {result.confidence_score:.0%}",
        "",
    ]

    if result.halt_message:
        lines += [f"**Stopped:** {result.halt_message}", ""]

    if result.reason:
        lines += [f"**Reason:** {result.reason}", ""]

    if result.rejection_reasons:
        lines += [
            "**Rejection reasons:** "
            + ", ".join(f"`{r}`" for r in result.rejection_reasons),
            "",
        ]

    if result.manual_review_signals:
        lines += ["**Manual review signals:**", ""]
        for s in result.manual_review_signals:
            lines.append(f"- {s}")
        lines.append("")

    if result.component_failures:
        lines += [
            "**⚡ Component failures:** "
            + ", ".join(f"`{c}`" for c in result.component_failures),
            "",
        ]

    # Amount breakdown
    if result.breakdown:
        bd = result.breakdown
        lines += ["### Amount Breakdown", "", "| | Amount |", "|--|--|"]
        lines.append(f"| Claimed | ₹{bd.claimed_amount:,.2f} |")
        if bd.network_discount_percent:
            lines.append(
                f"| Network discount ({bd.network_discount_percent:.0f}%) | − ₹{bd.network_discount_amount:,.2f} |"
            )
            lines.append(f"| After discount | ₹{bd.amount_after_discount:,.2f} |")
        if bd.copay_percent:
            lines.append(
                f"| Co-pay ({bd.copay_percent:.0f}%) | − ₹{bd.copay_amount:,.2f} |"
            )
        if bd.sub_limit_applied:
            lines.append(f"| Sub-limit cap | ₹{bd.sub_limit_applied:,.2f} |")
        lines.append(f"| **Approved** | **₹{bd.approved_amount:,.2f}** |")
        lines.append("")

    # Approved amount (no breakdown)
    if result.approved_amount is not None and not result.breakdown:
        lines += [f"**Approved amount:** ₹{result.approved_amount:,.2f}", ""]

    # Line-item decisions
    if result.line_item_decisions:
        lines += ["### Line Item Decisions", ""]
        for li in result.line_item_decisions:
            icon = "✅" if li.approved else "❌"
            reason = f" — {li.reason}" if li.reason else ""
            lines.append(f"{icon} **{li.description}** ₹{li.amount:,.2f}{reason}")
        lines.append("")

    lines += ["---", ""]

    # ── expected vs actual ────────────────────────────────────────────────────
    exp_decision = exp.get("decision")
    exp_outcome = exp_decision or "STOPPED (null)"
    act_outcome = decision_str or "STOPPED (null)"

    lines += [
        "## Expected vs Actual",
        "",
        "| | Expected | Actual |",
        "|--|----------|--------|",
        f"| Decision | `{exp_outcome}` | `{act_outcome}` |",
    ]
    if exp.get("approved_amount"):
        lines.append(
            f"| Approved amount | ₹{exp['approved_amount']:,.0f} | "
            f"{'₹' + '{:,.2f}'.format(result.approved_amount) if result.approved_amount is not None else '—'} |"
        )
    lines += [""]

    lines += ["### Checks", ""]
    for check in checks:
        lines.append(check)
    lines.append("")

    overall = "✅ **PASS**" if verdict else "❌ **FAIL**"
    lines += [f"### Verdict: {overall}", "", "---", ""]

    # ── raw logs ──────────────────────────────────────────────────────────────
    lines += [
        "## Raw Logs",
        "",
        "```",
        logs.strip() if logs.strip() else "(no log output captured)",
        "```",
        "",
    ]

    return "\n".join(lines)


# ── summary renderer ──────────────────────────────────────────────────────────

def _render_summary(
    rows: list[dict],
    run_ts: str,
    total_duration: float,
) -> str:
    pass_count = sum(1 for r in rows if r["verdict"])
    fail_count = len(rows) - pass_count

    lines: list[str] = [
        "# Evaluation Summary",
        "",
        f"**Run:** {run_ts}  ",
        f"**Total duration:** {total_duration:.1f}s  ",
        f"**Result: {pass_count}/{len(rows)} PASS**"
        + ("  ✅" if fail_count == 0 else f"  ({fail_count} failed)"),
        "",
        "---",
        "",
        "| Case | Name | Expected | Actual | Approved | Confidence | Verdict | Time |",
        "|------|------|----------|--------|----------|------------|---------|------|",
    ]

    for r in rows:
        exp_d = r["expected_decision"] or "STOPPED"
        act_d = r["actual_decision"] or "STOPPED"
        badge_exp = BADGE.get(exp_d, exp_d)
        badge_act = BADGE.get(act_d, act_d)
        approved = f"₹{r['approved_amount']:,.0f}" if r["approved_amount"] is not None else "—"
        verdict_icon = "✅" if r["verdict"] else "❌"
        lines.append(
            f"| **{r['case_id']}** | {r['case_name']} | {badge_exp} | {badge_act} "
            f"| {approved} | {r['confidence']:.0%} | {verdict_icon} | {r['duration']:.1f}s |"
        )

    lines += ["", "---", "", "## Per-Case Notes", ""]
    for r in rows:
        verdict_icon = "✅" if r["verdict"] else "❌"
        lines.append(f"### {verdict_icon} {r['case_id']} — {r['case_name']}")
        if r.get("halt_message"):
            lines.append(f"> **Stopped:** {r['halt_message']}")
        elif r.get("reason"):
            lines.append(f"> {r['reason']}")
        if r.get("rejection_reasons"):
            lines.append("> Rejection reasons: " + ", ".join(f"`{x}`" for x in r["rejection_reasons"]))
        if r.get("component_failures"):
            lines.append("> ⚡ Component failures: " + ", ".join(r["component_failures"]))
        lines.append(f"> See [`{r['filename']}`]({r['filename']})")
        lines.append("")

    return "\n".join(lines)


# ── main runner ───────────────────────────────────────────────────────────────

def run_evaluation(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    test_cases: list[dict] = json.loads(TEST_CASES_PATH.read_text())["test_cases"]
    policy = PolicyLoader(ROOT / "config" / "policy_terms.json")
    run_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # combined log file for the whole run
    combined_log_path = output_dir / "eval_run.log"
    combined_log_fh = open(combined_log_path, "w", encoding="utf-8")
    combined_log_fh.write(f"# Evaluation run — {run_ts}\n{'='*70}\n\n")

    summary_rows: list[dict] = []
    eval_start = time.time()

    print(f"\n{'='*60}")
    print(f"  Claims Pipeline Evaluation — {run_ts}")
    print(f"  {len(test_cases)} test cases  →  {output_dir}")
    print(f"{'='*60}\n")

    for tc in test_cases:
        case_id = tc["case_id"]
        case_name = tc["case_name"]
        slug = case_name.lower().replace(" ", "_").replace("—", "").replace("-", "_")
        slug = "".join(c for c in slug if c.isalnum() or c == "_").strip("_")
        report_filename = f"{case_id}_{slug}.md"
        report_path = output_dir / report_filename

        print(f"  Running {case_id}: {case_name} ...", end=" ", flush=True)
        claim = _build_claim(tc["input"])

        # Attach log capture
        capture_handler = _attach_capture()
        t0 = time.time()
        try:
            result: DecisionOutput = run_pipeline(claim, policy=policy)
        except Exception as exc:
            _log.error("Pipeline raised for %s: %s", case_id, exc, exc_info=True)
            raise
        finally:
            duration = time.time() - t0
            logs = _detach_capture(capture_handler)

        verdict, _ = _verdict(tc, result)
        verdict_icon = "✅ PASS" if verdict else "❌ FAIL"
        print(f"{verdict_icon}  ({duration:.1f}s)")

        # Write per-case report
        report_md = _render_report(tc, result, logs, duration, run_ts)
        report_path.write_text(report_md, encoding="utf-8")

        # Append to combined log
        combined_log_fh.write(f"{'─'*60}\n")
        combined_log_fh.write(f"[{case_id}] {case_name}\n")
        combined_log_fh.write(f"{'─'*60}\n")
        combined_log_fh.write(logs or "(no output)\n")
        combined_log_fh.write("\n")

        exp = tc.get("expected", {})
        summary_rows.append({
            "case_id": case_id,
            "case_name": case_name,
            "filename": report_filename,
            "expected_decision": exp.get("decision"),
            "actual_decision": result.decision.value if result.decision else None,
            "approved_amount": result.approved_amount,
            "confidence": result.confidence_score,
            "rejection_reasons": result.rejection_reasons,
            "halt_message": result.halt_message,
            "reason": result.reason,
            "component_failures": result.component_failures,
            "verdict": verdict,
            "duration": duration,
        })

    total_duration = time.time() - eval_start
    combined_log_fh.close()

    # Write summary
    summary_md = _render_summary(summary_rows, run_ts, total_duration)
    summary_path = output_dir / "00_summary.md"
    summary_path.write_text(summary_md, encoding="utf-8")

    pass_count = sum(1 for r in summary_rows if r["verdict"])
    print(f"\n{'='*60}")
    print(f"  Result: {pass_count}/{len(summary_rows)} PASS  in {total_duration:.1f}s")
    print(f"  Reports → {output_dir}/")
    print(f"  Summary → {summary_path}")
    print(f"  Log     → {combined_log_path}")
    print(f"{'='*60}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Run all 12 test cases through the live pipeline and write Markdown reports."
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for reports (default: experiments/output/evaluation)",
    )
    return p


if __name__ == "__main__":
    args = _build_parser().parse_args()
    run_evaluation(args.output_dir)
