"""Streamlit UI for the Multi-Agent Claims Pipeline.

Run with:
    streamlit run src/frontend/app.py

Modes:
  - Test Case    : full dropdown of all TC001–TC012
  - Manual Entry : free-form fields + file upload, with five Gradio-style
                   quick-example rows that auto-fill every field when clicked
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.logger import get_logger, setup_logging  # noqa: E402
from src.models.claim import ClaimInput, Document, DocumentContent, LineItem  # noqa: E402
from src.pipeline.graph import run_pipeline  # noqa: E402

setup_logging()
_log = get_logger("frontend.streamlit")

# ── constants ─────────────────────────────────────────────────────────────────

TEST_CASES_PATH = ROOT / "tests" / "test_cases.json"
QUICK_EXAMPLES_PATH = ROOT / "data" / "quick_examples.json"
CATEGORIES = [
    "CONSULTATION", "DIAGNOSTIC", "PHARMACY",
    "DENTAL", "VISION", "ALTERNATIVE_MEDICINE",
]
MEMBERS = [
    "EMP001", "EMP002", "EMP003", "EMP004", "EMP005",
    "EMP006", "EMP007", "EMP008", "EMP009", "EMP010",
]
DECISION_BADGE = {
    "APPROVED": "🟢", "PARTIAL": "🟡",
    "REJECTED": "🔴", "MANUAL_REVIEW": "🟠",
    "STOPPED": "🛑",
}

# Required and optional document types per claim category (mirrors policy_terms.json).
REQUIRED_DOCS: dict[str, dict[str, list[str]]] = {
    "CONSULTATION":        {"required": ["PRESCRIPTION", "HOSPITAL_BILL"],               "optional": ["LAB_REPORT", "DIAGNOSTIC_REPORT"]},
    "DIAGNOSTIC":          {"required": ["PRESCRIPTION", "LAB_REPORT", "HOSPITAL_BILL"], "optional": ["DISCHARGE_SUMMARY"]},
    "PHARMACY":            {"required": ["PRESCRIPTION", "PHARMACY_BILL"],               "optional": []},
    "DENTAL":              {"required": ["HOSPITAL_BILL"],                               "optional": ["PRESCRIPTION", "DENTAL_REPORT"]},
    "VISION":              {"required": ["PRESCRIPTION", "HOSPITAL_BILL"],               "optional": []},
    "ALTERNATIVE_MEDICINE":{"required": ["PRESCRIPTION", "HOSPITAL_BILL"],               "optional": []},
}

DOC_TYPE_LABELS: dict[str, str] = {
    "PRESCRIPTION":      "Prescription / Doctor's Note",
    "HOSPITAL_BILL":     "Hospital Bill / Receipt",
    "LAB_REPORT":        "Lab Report",
    "PHARMACY_BILL":     "Pharmacy Bill",
    "DENTAL_REPORT":     "Dental Report",
    "DIAGNOSTIC_REPORT": "Diagnostic Report",
    "DISCHARGE_SUMMARY": "Discharge Summary",
}

# ── page config ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="Claims Pipeline", page_icon="🏥", layout="wide")

# ── helpers ───────────────────────────────────────────────────────────────────

@st.cache_data
def load_test_cases() -> list[dict]:
    with open(TEST_CASES_PATH) as f:
        return json.load(f)["test_cases"]


@st.cache_data
def load_quick_examples() -> list[dict]:
    with open(QUICK_EXAMPLES_PATH) as f:
        return json.load(f)["examples"]


def build_claim_from_test(tc: dict) -> ClaimInput:
    inp = tc["input"]
    docs = []
    for d in inp.get("documents", []):
        content_raw = d.get("content")
        content = None
        if content_raw:
            li_raw = content_raw.get("line_items")
            if li_raw:
                content_raw = dict(content_raw)
                content_raw["line_items"] = [LineItem(**li) for li in li_raw]
            content = DocumentContent(**content_raw)
        docs.append(Document(
            file_id=d.get("file_id", ""),
            file_name=d.get("file_name"),
            actual_type=d.get("actual_type", ""),
            quality=d.get("quality", "GOOD"),
            patient_name_on_doc=d.get("patient_name_on_doc"),
            content=content,
        ))

    history = []
    for h in inp.get("claims_history", []):
        from src.models.claim import ClaimsHistory
        history.append(ClaimsHistory(**h))

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


def build_doc_from_spec(spec: dict) -> Document | None:
    """Load a Document from the file path in a quick-example spec.

    Returns None if the file does not exist so the caller can skip it.
    """
    full_path = ROOT / spec["path"]
    if not full_path.exists():
        return None
    file_bytes = full_path.read_bytes()
    ext = full_path.suffix.lower()
    media_type = (
        "image/png" if ext == ".png"
        else "application/pdf" if ext == ".pdf"
        else "image/jpeg"
    )
    return Document(
        file_id=spec["file_name"],
        file_name=spec["file_name"],
        actual_type=spec["actual_type"],
        quality=spec.get("quality", "GOOD"),
        file_data=file_bytes,
        media_type=media_type,
    )


# ── load data once ────────────────────────────────────────────────────────────

all_test_cases = load_test_cases()
tc_options: dict[str, dict] = {
    f"{tc['case_id']} — {tc['case_name']}": tc for tc in all_test_cases
}
tc_keys = list(tc_options.keys())
quick_examples = load_quick_examples()

# ── page title ────────────────────────────────────────────────────────────────

st.title("🏥 Health Insurance Claims Pipeline")

# ── sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.title("Claims Pipeline")
mode = st.sidebar.radio(
    "Mode", ["Test Case", "Manual Entry"], key="mode_radio"
)

# ── main input area ───────────────────────────────────────────────────────────

claim_input: ClaimInput | None = None

if mode == "Test Case":
    if "tc_select" not in st.session_state:
        st.session_state["tc_select"] = tc_keys[0]

    selected_label: str = st.selectbox(
        "Select a test case", tc_keys, key="tc_select"
    )
    selected_tc = tc_options[selected_label]

    inp = selected_tc["input"]
    exp = selected_tc.get("expected", {})
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Member", inp["member_id"])
    s2.metric("Category", inp["claim_category"])
    s3.metric("Amount", f"₹{inp['claimed_amount']:,.0f}")
    decision_val = exp.get("decision") or "—"
    s4.metric(
        "Expected",
        f"{DECISION_BADGE.get(decision_val, '⚪')} {decision_val}",
    )

    with st.expander("Full test case details", expanded=False):
        st.json(selected_tc)

    if st.button("Run Pipeline", type="primary", key="run_tc"):
        claim_input = build_claim_from_test(selected_tc)

else:  # Manual Entry
    # ── Gradio-style examples ──────────────────────────────────────────────────
    st.subheader("Examples")
    st.caption(
        "Click **Load** on any card to auto-fill all fields with a real synthetic invoice — "
        "then press **Run Pipeline**."
    )

    ex_cols = st.columns(len(quick_examples), gap="small")
    for col, ex in zip(ex_cols, quick_examples):
        n_docs = len(ex["documents"])
        n_ready = sum(1 for d in ex["documents"] if (ROOT / d["path"]).exists())
        exp = ex.get("expected", {})
        outcome = exp.get("outcome") or ("STOPPED" if exp.get("decision") is None else exp.get("decision"))
        badge = DECISION_BADGE.get(outcome, "⚪")

        with col:
            with st.container(border=True):
                st.markdown(f"**{ex['label']}**")
                st.caption(f"👤 {ex['member_id']}  ·  {ex['claim_category']}")
                st.caption(f"₹{ex['claimed_amount']:,.0f}  ·  📄 {n_ready}/{n_docs} docs")

                # Expected result block
                if exp:
                    st.markdown(
                        f"<div style='background:#1e1e2e;border-radius:6px;padding:6px 8px;margin:4px 0'>"
                        f"<span style='font-size:0.78em;color:#888'>Expected</span><br>"
                        f"<span style='font-size:0.95em;font-weight:600'>{badge} {outcome}</span><br>"
                        f"<span style='font-size:0.75em;color:#aaa'>{exp.get('summary', '')}</span>"
                        + (
                            f"<br><span style='font-size:0.75em;color:#6f6'>₹{exp['approved_amount']:,.0f} approved</span>"
                            if exp.get("approved_amount") else ""
                        )
                        + (
                            f"<br><span style='font-size:0.75em;color:#f88'>"
                            + ", ".join(exp["rejection_reasons"])
                            + "</span>"
                            if exp.get("rejection_reasons") else ""
                        )
                        + "</div>",
                        unsafe_allow_html=True,
                    )

                if st.button("Load", key=f"qex_{ex['id']}", use_container_width=True):
                    st.session_state["me_member_id"] = ex["member_id"]
                    st.session_state["me_claim_category"] = ex["claim_category"]
                    st.session_state["me_treatment_date"] = datetime.date.fromisoformat(
                        ex["treatment_date"]
                    )
                    st.session_state["me_claimed_amount"] = float(ex["claimed_amount"])
                    st.session_state["me_policy_id"] = ex["policy_id"]
                    st.session_state["me_doc_specs"] = ex["documents"]
                    st.session_state["me_active_example"] = ex["id"]
                    st.rerun()

    st.divider()

    # ── form fields ───────────────────────────────────────────────────────────
    active_ex = st.session_state.get("me_active_example")

    col1, col2 = st.columns(2)
    with col1:
        me_mid = st.session_state.get("me_member_id", MEMBERS[0])
        member_id = st.selectbox(
            "Member ID", MEMBERS,
            index=MEMBERS.index(me_mid) if me_mid in MEMBERS else 0,
        )
        me_cat = st.session_state.get("me_claim_category", CATEGORIES[0])
        claim_category = st.selectbox(
            "Claim Category", CATEGORIES,
            index=CATEGORIES.index(me_cat) if me_cat in CATEGORIES else 0,
        )
        treatment_date = st.date_input(
            "Treatment Date",
            value=st.session_state.get("me_treatment_date", datetime.date.today()),
        )
    with col2:
        claimed_amount = st.number_input(
            "Claimed Amount (₹)", min_value=0.0, step=100.0,
            value=st.session_state.get("me_claimed_amount", 0.0),
        )
        policy_id = st.text_input(
            "Policy ID",
            value=st.session_state.get("me_policy_id", "PLUM_GHI_2024"),
        )

    # ── documents ─────────────────────────────────────────────────────────────
    st.subheader("Documents")

    uploaded_doc_pairs: list[tuple[str, object]] = []  # (actual_type, UploadedFile)

    if active_ex and st.session_state.get("me_doc_specs"):
        doc_specs = st.session_state["me_doc_specs"]
        for spec in doc_specs:
            if (ROOT / spec["path"]).exists():
                st.caption(
                    f"🖼 **{spec['file_name']}** ({spec['actual_type']}) — "
                    "found, will run through OCR"
                )
            else:
                st.caption(
                    f"⚠️ **{spec['file_name']}** ({spec['actual_type']}) — "
                    f"not found at `{spec['path']}`, will be skipped"
                )
        if st.button("✕ Clear example", type="secondary"):
            for k in [
                "me_active_example", "me_doc_specs", "me_member_id",
                "me_claim_category", "me_treatment_date",
                "me_claimed_amount", "me_policy_id",
            ]:
                st.session_state.pop(k, None)
            st.rerun()
    else:
        # Dynamic labeled upload slots derived from the selected category.
        # Keys include the category so slots reset automatically when category changes.
        doc_config = REQUIRED_DOCS.get(claim_category, {"required": ["HOSPITAL_BILL"], "optional": []})

        for doc_type in doc_config["required"]:
            label = DOC_TYPE_LABELS.get(doc_type, doc_type)
            uf = st.file_uploader(
                f"{label} ✱",
                key=f"upload_{claim_category}_{doc_type}",
                type=["jpg", "jpeg", "png", "pdf"],
                help=f"Required for {claim_category} claims",
            )
            if uf:
                uploaded_doc_pairs.append((doc_type, uf))

        if doc_config["optional"]:
            with st.expander("Optional documents"):
                for doc_type in doc_config["optional"]:
                    label = DOC_TYPE_LABELS.get(doc_type, doc_type)
                    uf = st.file_uploader(
                        label,
                        key=f"upload_opt_{claim_category}_{doc_type}",
                        type=["jpg", "jpeg", "png", "pdf"],
                    )
                    if uf:
                        uploaded_doc_pairs.append((doc_type, uf))

        st.caption("✱ Required  ·  Hospital name is read from the document — no need to enter it manually.")

    # ── run button ────────────────────────────────────────────────────────────
    can_run = bool(
        (active_ex and st.session_state.get("me_doc_specs")) or uploaded_doc_pairs
    )
    if st.button("Run Pipeline", type="primary", key="run_manual", disabled=not can_run):
        if active_ex and st.session_state.get("me_doc_specs"):
            docs = [
                d for s in st.session_state["me_doc_specs"]
                if (d := build_doc_from_spec(s)) is not None
            ]
        else:
            docs = []
            for doc_type, uf in uploaded_doc_pairs:
                ext = uf.name.lower()
                media_type = "application/pdf" if ext.endswith(".pdf") else "image/jpeg"
                docs.append(Document(
                    file_id=uf.name,
                    file_name=uf.name,
                    actual_type=doc_type,
                    quality="GOOD",
                    file_data=uf.read(),
                    media_type=media_type,
                ))
        claim_input = ClaimInput(
            member_id=member_id,
            policy_id=policy_id,
            claim_category=claim_category,
            treatment_date=str(treatment_date),
            claimed_amount=claimed_amount,
            documents=docs,
        )

# ── pipeline execution ────────────────────────────────────────────────────────

if claim_input is not None:
    with st.spinner("Running pipeline…"):
        try:
            _log.info(
                "Submitting — member=%s category=%s amount=₹%.2f",
                claim_input.member_id,
                claim_input.claim_category,
                claim_input.claimed_amount,
            )
            result = run_pipeline(claim_input)
            _log.info(
                "Result — claim_id=%s decision=%s confidence=%.4f",
                result.claim_id,
                result.decision.value if result.decision else "None",
                result.confidence_score,
            )
        except Exception as exc:
            _log.error("Pipeline error: %s", exc, exc_info=True)
            st.error(f"Pipeline error: {exc}")
            st.stop()

    # ── results ───────────────────────────────────────────────────────────────

    st.divider()
    st.subheader("Decision")

    col_a, col_b, col_c = st.columns(3)
    decision_str = result.decision.value if result.decision else None
    col_a.markdown(
        f"### {DECISION_BADGE.get(decision_str, '⚪')} **{decision_str or 'STOPPED'}**"
    )
    col_b.metric(
        "Approved Amount",
        f"₹{result.approved_amount:,.2f}" if result.approved_amount is not None else "—",
    )
    col_c.metric("Confidence", f"{result.confidence_score:.0%}")

    if result.halt_message:
        st.error(f"**Stopped:** {result.halt_message}")
    if result.reason:
        st.info(result.reason)
    if result.rejection_reasons:
        st.warning("Rejection reasons: " + ", ".join(result.rejection_reasons))
    if result.manual_review_signals:
        st.warning(
            "Manual review signals:\n"
            + "\n".join(f"- {s}" for s in result.manual_review_signals)
        )
    if result.component_failures:
        st.error("Component failures: " + ", ".join(result.component_failures))

    # Amount breakdown
    if result.breakdown:
        st.subheader("Amount Breakdown")
        bd = result.breakdown
        rows = [("Claimed amount", f"₹{bd.claimed_amount:,.2f}")]
        if bd.network_discount_percent:
            rows.append((
                f"Network discount ({bd.network_discount_percent:.0f}%)",
                f"− ₹{bd.network_discount_amount:,.2f}",
            ))
            rows.append(("After discount", f"₹{bd.amount_after_discount:,.2f}"))
        if bd.copay_percent:
            rows.append((
                f"Co-pay ({bd.copay_percent:.0f}%)",
                f"− ₹{bd.copay_amount:,.2f}",
            ))
        if bd.sub_limit_applied:
            rows.append(("Sub-limit cap", f"₹{bd.sub_limit_applied:,.2f}"))
        rows.append(("**Approved amount**", f"**₹{bd.approved_amount:,.2f}**"))
        for label, value in rows:
            c1, c2 = st.columns([3, 1])
            c1.markdown(label)
            c2.markdown(value)

    # Line-item decisions
    if result.line_item_decisions:
        st.subheader("Line Item Decisions")
        for li in result.line_item_decisions:
            icon = "✅" if li.approved else "❌"
            reason = f" — {li.reason}" if li.reason else ""
            st.markdown(f"{icon} **{li.description}** ₹{li.amount:,.2f}{reason}")

    # Full audit trace
    with st.expander("Full Audit Trace", expanded=False):
        icons = {
            "PASS": "✅", "FAIL": "❌", "WARNING": "⚠️",
            "ERROR": "🔥", "INFO": "ℹ️",
        }
        for entry in result.trace:
            icon = icons.get(entry.result, "•")
            st.markdown(
                f"{icon} `{entry.agent}` / `{entry.step}` — {entry.detail}"
            )
