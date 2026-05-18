# TC009 — Fraud Signal — Multiple Same-Day Claims

> Member EMP008 has already submitted 3 claims today before this one arrives. This is the 4th claim from the same member on the same day.

**Claim ID:** `5C482387`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 0.01s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP008` |
| Claim Category | `CONSULTATION` |
| Treatment Date | 2024-10-30 |
| Claimed Amount | ₹4,800 |
| Policy ID | `PLUM_GHI_2024` |

**Documents submitted:**

- `F017`  type=`PRESCRIPTION`
- `F018`  type=`HOSPITAL_BILL`

**Claims history (same day):**

- `CLM_0081` — ₹1,200 at City Clinic A on 2024-10-30
- `CLM_0082` — ₹1,800 at City Clinic B on 2024-10-30
- `CLM_0083` — ₹2,100 at Wellness Center on 2024-10-30

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Ravi Menon' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-10-30 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹4800.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F017` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 7 | `DocParserAgent` | `parse_F018` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 8 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for CONSULTATION: PRESCRIPTION, HOSPITAL_BILL |
| 9 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 10 | `DecisionMakerAgent` | `fraud_same_day` | ⚠️ `WARNING` | Member has 3 prior claim(s) on 2024-10-30 (limit: 2) |
| 11 | `DecisionMakerAgent` | `manual_review_trigger` | ℹ️ `INFO` | Routing to MANUAL_REVIEW: Member has 3 prior claim(s) on 2024-10-30 (limit: 2) |

---

## Decision

### 🟠 MANUAL REVIEW

**Confidence:** 100%

**Reason:** Claim flagged for manual review due to unusual activity patterns.

**Manual review signals:**

- Member has 3 prior claim(s) on 2024-10-30 (limit: 2)

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `MANUAL_REVIEW` | `MANUAL_REVIEW` |

### Checks

✅ Decision: expected **MANUAL_REVIEW**, got **MANUAL_REVIEW**
✅ System must: _Flag the unusual same-day claim pattern_
✅ System must: _Route to manual review rather than auto-rejecting_
⚠️  System must: _Include the specific signals that triggered the flag in the output_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:34 | INFO     | claims.pipeline.graph            | [5C482387] Pipeline started — member=EMP008 category=CONSULTATION amount=₹4800.00 docs=2 simulate_failure=False
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] → entering node: DataValidatorAgent
13:03:34 | INFO     | claims.agents.data_validator     | [5C482387] Starting — member=EMP008 category=CONSULTATION amount=₹4800.00 docs=2
13:03:34 | DEBUG    | claims.agents.data_validator     | [5C482387] PASS policy_id — PLUM_GHI_2024
13:03:34 | INFO     | claims.agents.data_validator     | [5C482387] PASS member_lookup — 'Ravi Menon' (joined 2024-04-01)
13:03:34 | INFO     | claims.agents.data_validator     | [5C482387] PASS policy_period — treatment 2024-10-30 within [2024-04-01, 2025-03-31]
13:03:34 | DEBUG    | claims.agents.data_validator     | [5C482387] PASS category — CONSULTATION
13:03:34 | DEBUG    | claims.agents.data_validator     | [5C482387] PASS minimum_amount — ₹4800.00 ≥ ₹500
13:03:34 | INFO     | claims.agents.data_validator     | [5C482387] Complete — all checks passed
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] ← exiting node: DataValidatorAgent
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] → entering node: DocParserAgent
13:03:34 | INFO     | claims.agents.doc_parser         | [5C482387] Starting — parsing 2 document(s)
13:03:34 | DEBUG    | claims.agents.doc_parser         | [5C482387] Parsing PRESCRIPTION (file_id=F017) from pre-supplied content
13:03:34 | DEBUG    | claims.agents.doc_parser         | [5C482387] Extracted PRESCRIPTION — patient=— diagnosis=Migraine items=0
13:03:34 | DEBUG    | claims.agents.doc_parser         | [5C482387] Parsing HOSPITAL_BILL (file_id=F018) from pre-supplied content
13:03:34 | DEBUG    | claims.agents.doc_parser         | [5C482387] Extracted HOSPITAL_BILL — patient=— diagnosis=— items=0
13:03:34 | INFO     | claims.agents.doc_parser         | [5C482387] Complete — 2 extracted, 0 failed, confidence=1.00
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] ← exiting node: DocParserAgent
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] → entering node: DocValidatorAgent
13:03:34 | INFO     | claims.agents.doc_validator      | [5C482387] Starting — category=CONSULTATION docs=2
13:03:34 | DEBUG    | claims.agents.doc_validator      | [5C482387] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'HOSPITAL_BILL': 1}
13:03:34 | INFO     | claims.agents.doc_validator      | [5C482387] PASS doc_types — all required docs present: PRESCRIPTION, HOSPITAL_BILL
13:03:34 | INFO     | claims.agents.doc_validator      | [5C482387] Complete — all document checks passed
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] ← exiting node: DocValidatorAgent
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] → entering node: DecisionMakerAgent
13:03:34 | INFO     | claims.agents.decision_maker     | [5C482387] Starting — category=CONSULTATION amount=₹4800.00 diagnosis=Migraine hospital=—
13:03:34 | WARNING  | claims.agents.decision_maker     | [5C482387] Fraud signal — same-day: Member has 3 prior claim(s) on 2024-10-30 (limit: 2)
13:03:34 | WARNING  | claims.agents.decision_maker     | [5C482387] Routing to MANUAL_REVIEW — 1 signal(s) triggered
13:03:34 | DEBUG    | claims.pipeline.graph            | [5C482387] ← exiting node: DecisionMakerAgent
13:03:34 | INFO     | claims.pipeline.graph            | [5C482387] Pipeline complete — decision=MANUAL_REVIEW approved=₹— confidence=1.0000 failures=none
```
