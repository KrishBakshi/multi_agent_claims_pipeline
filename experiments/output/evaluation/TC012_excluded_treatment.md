# TC012 — Excluded Treatment

> Member claims for bariatric consultation and a diet program. Obesity treatment is explicitly excluded under the policy.

**Claim ID:** `AABD17C6`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 1.30s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP009` |
| Claim Category | `CONSULTATION` |
| Treatment Date | 2024-10-18 |
| Claimed Amount | ₹8,000 |
| Policy ID | `PLUM_GHI_2024` |

**Documents submitted:**

- `F023`  type=`PRESCRIPTION`
- `F024`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Anita Desai' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-10-18 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹8000.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F023` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 7 | `DocParserAgent` | `parse_F024` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 8 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for CONSULTATION: PRESCRIPTION, HOSPITAL_BILL |
| 9 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 10 | `DecisionMakerAgent` | `exclusion_check` | ❌ `FAIL` | Claim rejected: 'Obesity and weight loss programs' is excluded under the policy. Reason: The claim is for a bariatric consultation and a customised diet plan, which directly falls under the exclusion for obesity and weight loss programs. |

---

## Decision

### 🔴 REJECTED

**Confidence:** 100%

**Reason:** Claim rejected: 'Obesity and weight loss programs' is excluded under the policy. Reason: The claim is for a bariatric consultation and a customised diet plan, which directly falls under the exclusion for obesity and weight loss programs.

**Rejection reasons:** `EXCLUDED_CONDITION`

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `REJECTED` | `REJECTED` |

### Checks

✅ Decision: expected **REJECTED**, got **REJECTED**
✅ Rejection reason **EXCLUDED_CONDITION** present
✅ Confidence ≥ 90% (actual 100%)

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:40 | INFO     | claims.pipeline.graph            | [AABD17C6] Pipeline started — member=EMP009 category=CONSULTATION amount=₹8000.00 docs=2 simulate_failure=False
13:03:40 | DEBUG    | claims.pipeline.graph            | [AABD17C6] → entering node: DataValidatorAgent
13:03:40 | INFO     | claims.agents.data_validator     | [AABD17C6] Starting — member=EMP009 category=CONSULTATION amount=₹8000.00 docs=2
13:03:40 | DEBUG    | claims.agents.data_validator     | [AABD17C6] PASS policy_id — PLUM_GHI_2024
13:03:40 | INFO     | claims.agents.data_validator     | [AABD17C6] PASS member_lookup — 'Anita Desai' (joined 2024-04-01)
13:03:40 | INFO     | claims.agents.data_validator     | [AABD17C6] PASS policy_period — treatment 2024-10-18 within [2024-04-01, 2025-03-31]
13:03:40 | DEBUG    | claims.agents.data_validator     | [AABD17C6] PASS category — CONSULTATION
13:03:40 | DEBUG    | claims.agents.data_validator     | [AABD17C6] PASS minimum_amount — ₹8000.00 ≥ ₹500
13:03:40 | INFO     | claims.agents.data_validator     | [AABD17C6] Complete — all checks passed
13:03:40 | DEBUG    | claims.pipeline.graph            | [AABD17C6] ← exiting node: DataValidatorAgent
13:03:40 | DEBUG    | claims.pipeline.graph            | [AABD17C6] → entering node: DocParserAgent
13:03:40 | INFO     | claims.agents.doc_parser         | [AABD17C6] Starting — parsing 2 document(s)
13:03:40 | DEBUG    | claims.agents.doc_parser         | [AABD17C6] Parsing PRESCRIPTION (file_id=F023) from pre-supplied content
13:03:40 | DEBUG    | claims.agents.doc_parser         | [AABD17C6] Extracted PRESCRIPTION — patient=— diagnosis=Morbid Obesity — BMI 37 items=0
13:03:40 | DEBUG    | claims.agents.doc_parser         | [AABD17C6] Parsing HOSPITAL_BILL (file_id=F024) from pre-supplied content
13:03:40 | DEBUG    | claims.agents.doc_parser         | [AABD17C6] Extracted HOSPITAL_BILL — patient=— diagnosis=— items=2
13:03:40 | INFO     | claims.agents.doc_parser         | [AABD17C6] Complete — 2 extracted, 0 failed, confidence=1.00
13:03:40 | DEBUG    | claims.pipeline.graph            | [AABD17C6] ← exiting node: DocParserAgent
13:03:40 | DEBUG    | claims.pipeline.graph            | [AABD17C6] → entering node: DocValidatorAgent
13:03:40 | INFO     | claims.agents.doc_validator      | [AABD17C6] Starting — category=CONSULTATION docs=2
13:03:40 | DEBUG    | claims.agents.doc_validator      | [AABD17C6] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'HOSPITAL_BILL': 1}
13:03:40 | INFO     | claims.agents.doc_validator      | [AABD17C6] PASS doc_types — all required docs present: PRESCRIPTION, HOSPITAL_BILL
13:03:40 | INFO     | claims.agents.doc_validator      | [AABD17C6] Complete — all document checks passed
13:03:40 | DEBUG    | claims.pipeline.graph            | [AABD17C6] ← exiting node: DocValidatorAgent
13:03:40 | DEBUG    | claims.pipeline.graph            | [AABD17C6] → entering node: DecisionMakerAgent
13:03:40 | INFO     | claims.agents.decision_maker     | [AABD17C6] Starting — category=CONSULTATION amount=₹8000.00 diagnosis=Morbid Obesity — BMI 37 hospital=—
13:03:40 | DEBUG    | claims.agents.decision_maker     | [AABD17C6] Calling Gemini for exclusion check — diagnosis='Morbid Obesity — BMI 37' treatment='Bariatric Consultation and Customised Diet Plan'
13:03:41 | WARNING  | claims.agents.decision_maker     | [AABD17C6] EXCLUDED — matched: 'Obesity and weight loss programs'
13:03:41 | DEBUG    | claims.pipeline.graph            | [AABD17C6] ← exiting node: DecisionMakerAgent
13:03:41 | INFO     | claims.pipeline.graph            | [AABD17C6] Pipeline complete — decision=REJECTED approved=₹— confidence=1.0000 failures=none
```
