# TC005 — Waiting Period — Diabetes

> Member joined 2024-09-01. Claims for diabetes treatment on 2024-10-15, which is within the 90-day waiting period for diabetes.

**Claim ID:** `2919B5DE`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 2.66s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP005` |
| Claim Category | `CONSULTATION` |
| Treatment Date | 2024-10-15 |
| Claimed Amount | ₹3,000 |
| Policy ID | `PLUM_GHI_2024` |

**Documents submitted:**

- `F009`  type=`PRESCRIPTION`
- `F010`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Vikram Joshi' found (joined 2024-09-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-10-15 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹3000.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F009` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 7 | `DocParserAgent` | `parse_F010` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 8 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for CONSULTATION: PRESCRIPTION, HOSPITAL_BILL |
| 9 | `DocValidatorAgent` | `patient_name_consistency` | ✅ `PASS` | All named documents reference the same patient: 'vikram joshi' |
| 10 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 11 | `DecisionMakerAgent` | `exclusion_check` | ✅ `PASS` | No exclusion matched. Type 2 Diabetes Mellitus does not fall under any of the listed policy exclusions. |
| 12 | `DecisionMakerAgent` | `waiting_period_initial` | ✅ `PASS` | Initial waiting period satisfied (44 days since join) |
| 13 | `DecisionMakerAgent` | `waiting_period_specific` | ❌ `FAIL` | Claim for 'diabetes' is within the 90-day waiting period. Member joined 2024-09-01; eligible for diabetes claims from 2024-11-30. |

---

## Decision

### 🔴 REJECTED

**Confidence:** 100%

**Reason:** Claim for 'diabetes' is within the 90-day waiting period. Member joined 2024-09-01; eligible for diabetes claims from 2024-11-30.

**Rejection reasons:** `WAITING_PERIOD`

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `REJECTED` | `REJECTED` |

### Checks

✅ Decision: expected **REJECTED**, got **REJECTED**
✅ Rejection reason **WAITING_PERIOD** present
✅ System must: _State the date from which the member will be eligible for diabetes-related claims_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:25 | INFO     | claims.pipeline.graph            | [2919B5DE] Pipeline started — member=EMP005 category=CONSULTATION amount=₹3000.00 docs=2 simulate_failure=False
13:03:25 | DEBUG    | claims.pipeline.graph            | [2919B5DE] → entering node: DataValidatorAgent
13:03:25 | INFO     | claims.agents.data_validator     | [2919B5DE] Starting — member=EMP005 category=CONSULTATION amount=₹3000.00 docs=2
13:03:25 | DEBUG    | claims.agents.data_validator     | [2919B5DE] PASS policy_id — PLUM_GHI_2024
13:03:25 | INFO     | claims.agents.data_validator     | [2919B5DE] PASS member_lookup — 'Vikram Joshi' (joined 2024-09-01)
13:03:25 | INFO     | claims.agents.data_validator     | [2919B5DE] PASS policy_period — treatment 2024-10-15 within [2024-04-01, 2025-03-31]
13:03:25 | DEBUG    | claims.agents.data_validator     | [2919B5DE] PASS category — CONSULTATION
13:03:25 | DEBUG    | claims.agents.data_validator     | [2919B5DE] PASS minimum_amount — ₹3000.00 ≥ ₹500
13:03:25 | INFO     | claims.agents.data_validator     | [2919B5DE] Complete — all checks passed
13:03:25 | DEBUG    | claims.pipeline.graph            | [2919B5DE] ← exiting node: DataValidatorAgent
13:03:25 | DEBUG    | claims.pipeline.graph            | [2919B5DE] → entering node: DocParserAgent
13:03:25 | INFO     | claims.agents.doc_parser         | [2919B5DE] Starting — parsing 2 document(s)
13:03:25 | DEBUG    | claims.agents.doc_parser         | [2919B5DE] Parsing PRESCRIPTION (file_id=F009) from pre-supplied content
13:03:25 | DEBUG    | claims.agents.doc_parser         | [2919B5DE] Extracted PRESCRIPTION — patient=Vikram Joshi diagnosis=Type 2 Diabetes Mellitus items=0
13:03:25 | DEBUG    | claims.agents.doc_parser         | [2919B5DE] Parsing HOSPITAL_BILL (file_id=F010) from pre-supplied content
13:03:25 | DEBUG    | claims.agents.doc_parser         | [2919B5DE] Extracted HOSPITAL_BILL — patient=Vikram Joshi diagnosis=— items=0
13:03:25 | INFO     | claims.agents.doc_parser         | [2919B5DE] Complete — 2 extracted, 0 failed, confidence=1.00
13:03:25 | DEBUG    | claims.pipeline.graph            | [2919B5DE] ← exiting node: DocParserAgent
13:03:25 | DEBUG    | claims.pipeline.graph            | [2919B5DE] → entering node: DocValidatorAgent
13:03:25 | INFO     | claims.agents.doc_validator      | [2919B5DE] Starting — category=CONSULTATION docs=2
13:03:25 | DEBUG    | claims.agents.doc_validator      | [2919B5DE] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'HOSPITAL_BILL': 1}
13:03:25 | INFO     | claims.agents.doc_validator      | [2919B5DE] PASS doc_types — all required docs present: PRESCRIPTION, HOSPITAL_BILL
13:03:25 | INFO     | claims.agents.doc_validator      | [2919B5DE] PASS patient_name_consistency — all docs reference 'vikram joshi'
13:03:25 | INFO     | claims.agents.doc_validator      | [2919B5DE] Complete — all document checks passed
13:03:25 | DEBUG    | claims.pipeline.graph            | [2919B5DE] ← exiting node: DocValidatorAgent
13:03:25 | DEBUG    | claims.pipeline.graph            | [2919B5DE] → entering node: DecisionMakerAgent
13:03:25 | INFO     | claims.agents.decision_maker     | [2919B5DE] Starting — category=CONSULTATION amount=₹3000.00 diagnosis=Type 2 Diabetes Mellitus hospital=—
13:03:25 | DEBUG    | claims.agents.decision_maker     | [2919B5DE] Calling Gemini for exclusion check — diagnosis='Type 2 Diabetes Mellitus' treatment='—'
13:03:26 | DEBUG    | claims.agents.decision_maker     | [2919B5DE] PASS exclusion_check — Type 2 Diabetes Mellitus does not fall under any of the listed policy exclusions.
13:03:26 | DEBUG    | claims.agents.decision_maker     | [2919B5DE] Calling Gemini for waiting-period condition match — diagnosis='Type 2 Diabetes Mellitus'
13:03:28 | DEBUG    | claims.agents.decision_maker     | [2919B5DE] Waiting period match — condition='diabetes' days=90 days_since_join=44
13:03:28 | WARNING  | claims.agents.decision_maker     | [2919B5DE] REJECTED — waiting period: Claim for 'diabetes' is within the 90-day waiting period. Member joined 2024-09-01; eligible for diabetes claims from 2024-11-30.
13:03:28 | DEBUG    | claims.pipeline.graph            | [2919B5DE] ← exiting node: DecisionMakerAgent
13:03:28 | INFO     | claims.pipeline.graph            | [2919B5DE] Pipeline complete — decision=REJECTED approved=₹— confidence=1.0000 failures=none
```
