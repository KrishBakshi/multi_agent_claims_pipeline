# TC008 — Per-Claim Limit Exceeded

> Claimed amount of ₹7,500 exceeds the per-claim limit of ₹5,000.

**Claim ID:** `AF3FDCB4`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 2.60s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP003` |
| Claim Category | `CONSULTATION` |
| Treatment Date | 2024-10-20 |
| Claimed Amount | ₹7,500 |
| Policy ID | `PLUM_GHI_2024` |
| YTD Claims | ₹10,000 |

**Documents submitted:**

- `F015`  type=`PRESCRIPTION`
- `F016`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Amit Verma' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-10-20 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹7500.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F015` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 7 | `DocParserAgent` | `parse_F016` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 8 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for CONSULTATION: PRESCRIPTION, HOSPITAL_BILL |
| 9 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 10 | `DecisionMakerAgent` | `exclusion_check` | ✅ `PASS` | No exclusion matched. Gastroenteritis is a common medical condition and is not listed among the specified policy exclusions. |
| 11 | `DecisionMakerAgent` | `waiting_period_initial` | ✅ `PASS` | Initial waiting period satisfied (202 days since join) |
| 12 | `DecisionMakerAgent` | `waiting_period_specific` | ✅ `PASS` | No specific waiting period matched. Gastroenteritis is an acute gastrointestinal infection and does not fall under any of the listed chronic conditions or specified waiting-period categories such as diabetes, hypertension, or maternity. |
| 13 | `DecisionMakerAgent` | `pre_auth_check` | ✅ `PASS` | Pre-authorisation not required or already obtained |
| 14 | `DecisionMakerAgent` | `per_claim_limit` | ❌ `FAIL` | Claimed amount ₹7500.0 exceeds the per-claim limit of ₹5000. Claims above this limit cannot be processed. |

---

## Decision

### 🔴 REJECTED

**Confidence:** 100%

**Reason:** Claimed amount ₹7500.0 exceeds the per-claim limit of ₹5000. Claims above this limit cannot be processed.

**Rejection reasons:** `PER_CLAIM_EXCEEDED`

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `REJECTED` | `REJECTED` |

### Checks

✅ Decision: expected **REJECTED**, got **REJECTED**
✅ Rejection reason **PER_CLAIM_EXCEEDED** present
✅ System must: _State the per-claim limit and the claimed amount clearly in the rejection message_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:31 | INFO     | claims.pipeline.graph            | [AF3FDCB4] Pipeline started — member=EMP003 category=CONSULTATION amount=₹7500.00 docs=2 simulate_failure=False
13:03:31 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] → entering node: DataValidatorAgent
13:03:31 | INFO     | claims.agents.data_validator     | [AF3FDCB4] Starting — member=EMP003 category=CONSULTATION amount=₹7500.00 docs=2
13:03:31 | DEBUG    | claims.agents.data_validator     | [AF3FDCB4] PASS policy_id — PLUM_GHI_2024
13:03:31 | INFO     | claims.agents.data_validator     | [AF3FDCB4] PASS member_lookup — 'Amit Verma' (joined 2024-04-01)
13:03:31 | INFO     | claims.agents.data_validator     | [AF3FDCB4] PASS policy_period — treatment 2024-10-20 within [2024-04-01, 2025-03-31]
13:03:31 | DEBUG    | claims.agents.data_validator     | [AF3FDCB4] PASS category — CONSULTATION
13:03:31 | DEBUG    | claims.agents.data_validator     | [AF3FDCB4] PASS minimum_amount — ₹7500.00 ≥ ₹500
13:03:31 | INFO     | claims.agents.data_validator     | [AF3FDCB4] Complete — all checks passed
13:03:31 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] ← exiting node: DataValidatorAgent
13:03:31 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] → entering node: DocParserAgent
13:03:31 | INFO     | claims.agents.doc_parser         | [AF3FDCB4] Starting — parsing 2 document(s)
13:03:31 | DEBUG    | claims.agents.doc_parser         | [AF3FDCB4] Parsing PRESCRIPTION (file_id=F015) from pre-supplied content
13:03:31 | DEBUG    | claims.agents.doc_parser         | [AF3FDCB4] Extracted PRESCRIPTION — patient=— diagnosis=Gastroenteritis items=0
13:03:31 | DEBUG    | claims.agents.doc_parser         | [AF3FDCB4] Parsing HOSPITAL_BILL (file_id=F016) from pre-supplied content
13:03:31 | DEBUG    | claims.agents.doc_parser         | [AF3FDCB4] Extracted HOSPITAL_BILL — patient=— diagnosis=— items=2
13:03:31 | INFO     | claims.agents.doc_parser         | [AF3FDCB4] Complete — 2 extracted, 0 failed, confidence=1.00
13:03:31 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] ← exiting node: DocParserAgent
13:03:31 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] → entering node: DocValidatorAgent
13:03:31 | INFO     | claims.agents.doc_validator      | [AF3FDCB4] Starting — category=CONSULTATION docs=2
13:03:31 | DEBUG    | claims.agents.doc_validator      | [AF3FDCB4] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'HOSPITAL_BILL': 1}
13:03:31 | INFO     | claims.agents.doc_validator      | [AF3FDCB4] PASS doc_types — all required docs present: PRESCRIPTION, HOSPITAL_BILL
13:03:31 | INFO     | claims.agents.doc_validator      | [AF3FDCB4] Complete — all document checks passed
13:03:31 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] ← exiting node: DocValidatorAgent
13:03:31 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] → entering node: DecisionMakerAgent
13:03:31 | INFO     | claims.agents.decision_maker     | [AF3FDCB4] Starting — category=CONSULTATION amount=₹7500.00 diagnosis=Gastroenteritis hospital=—
13:03:31 | DEBUG    | claims.agents.decision_maker     | [AF3FDCB4] Calling Gemini for exclusion check — diagnosis='Gastroenteritis' treatment='—'
13:03:32 | DEBUG    | claims.agents.decision_maker     | [AF3FDCB4] PASS exclusion_check — Gastroenteritis is a common medical condition and is not listed among the specified policy exclusions.
13:03:32 | DEBUG    | claims.agents.decision_maker     | [AF3FDCB4] Calling Gemini for waiting-period condition match — diagnosis='Gastroenteritis'
13:03:34 | DEBUG    | claims.agents.decision_maker     | [AF3FDCB4] No specific waiting period matched — Gastroenteritis is an acute gastrointestinal infection and does not fall under any of the listed chronic conditions or specified waiting-period categories such as diabetes, hypertension, or maternity.
13:03:34 | WARNING  | claims.agents.decision_maker     | [AF3FDCB4] REJECTED — per-claim limit: ₹7500.00 > ₹5000.00
13:03:34 | DEBUG    | claims.pipeline.graph            | [AF3FDCB4] ← exiting node: DecisionMakerAgent
13:03:34 | INFO     | claims.pipeline.graph            | [AF3FDCB4] Pipeline complete — decision=REJECTED approved=₹— confidence=1.0000 failures=none
```
