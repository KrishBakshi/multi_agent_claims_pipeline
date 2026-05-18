# TC007 — MRI Without Pre-Authorization

> MRI scan costing ₹15,000 submitted without pre-authorization. Policy requires pre-auth for MRI above ₹10,000.

**Claim ID:** `B9E63344`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 3.52s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP007` |
| Claim Category | `DIAGNOSTIC` |
| Treatment Date | 2024-11-02 |
| Claimed Amount | ₹15,000 |
| Policy ID | `PLUM_GHI_2024` |

**Documents submitted:**

- `F012`  type=`PRESCRIPTION`
- `F013`  type=`LAB_REPORT`
- `F014`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Suresh Patil' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-11-02 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'DIAGNOSTIC' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹15000.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F012` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 7 | `DocParserAgent` | `parse_F013` | ✅ `PASS` | Parsed LAB_REPORT (quality=GOOD, confidence=1.00) |
| 8 | `DocParserAgent` | `parse_F014` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 9 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for DIAGNOSTIC: PRESCRIPTION, LAB_REPORT, HOSPITAL_BILL |
| 10 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 11 | `DecisionMakerAgent` | `exclusion_check` | ✅ `PASS` | No exclusion matched. A lumbar disc herniation is a standard medical condition that does not fall under any of the listed exclusions such as self-inflicted injuries, elective cosmetic procedures, or specific excluded treatments like substance abuse or bariatric surgery. |
| 12 | `DecisionMakerAgent` | `waiting_period_initial` | ✅ `PASS` | Initial waiting period satisfied (215 days since join) |
| 13 | `DecisionMakerAgent` | `waiting_period_specific` | ✅ `PASS` | No specific waiting period matched. Lumbar disc herniation involves spinal discs, which is distinct from an abdominal or inguinal hernia (the type of hernia typically covered by such condition lists). |
| 14 | `DecisionMakerAgent` | `pre_auth_check` | ❌ `FAIL` | Pre-authorisation is required for this procedure (amount ₹15000.0 exceeds the ₹10000 threshold for high-value diagnostic tests). To resubmit: obtain pre-authorisation from your insurer, then re-file the claim with the pre-auth reference number. Pre-auth is valid for 30 days. |

---

## Decision

### 🔴 REJECTED

**Confidence:** 100%

**Reason:** Pre-authorisation is required for this procedure (amount ₹15000.0 exceeds the ₹10000 threshold for high-value diagnostic tests). To resubmit: obtain pre-authorisation from your insurer, then re-file the claim with the pre-auth reference number. Pre-auth is valid for 30 days.

**Rejection reasons:** `PRE_AUTH_MISSING`

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `REJECTED` | `REJECTED` |

### Checks

✅ Decision: expected **REJECTED**, got **REJECTED**
✅ Rejection reason **PRE_AUTH_MISSING** present
✅ System must: _Explain that pre-authorization was required and not obtained_
✅ System must: _Tell the member what they should do to resubmit with pre-auth_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:28 | INFO     | claims.pipeline.graph            | [B9E63344] Pipeline started — member=EMP007 category=DIAGNOSTIC amount=₹15000.00 docs=3 simulate_failure=False
13:03:28 | DEBUG    | claims.pipeline.graph            | [B9E63344] → entering node: DataValidatorAgent
13:03:28 | INFO     | claims.agents.data_validator     | [B9E63344] Starting — member=EMP007 category=DIAGNOSTIC amount=₹15000.00 docs=3
13:03:28 | DEBUG    | claims.agents.data_validator     | [B9E63344] PASS policy_id — PLUM_GHI_2024
13:03:28 | INFO     | claims.agents.data_validator     | [B9E63344] PASS member_lookup — 'Suresh Patil' (joined 2024-04-01)
13:03:28 | INFO     | claims.agents.data_validator     | [B9E63344] PASS policy_period — treatment 2024-11-02 within [2024-04-01, 2025-03-31]
13:03:28 | DEBUG    | claims.agents.data_validator     | [B9E63344] PASS category — DIAGNOSTIC
13:03:28 | DEBUG    | claims.agents.data_validator     | [B9E63344] PASS minimum_amount — ₹15000.00 ≥ ₹500
13:03:28 | INFO     | claims.agents.data_validator     | [B9E63344] Complete — all checks passed
13:03:28 | DEBUG    | claims.pipeline.graph            | [B9E63344] ← exiting node: DataValidatorAgent
13:03:28 | DEBUG    | claims.pipeline.graph            | [B9E63344] → entering node: DocParserAgent
13:03:28 | INFO     | claims.agents.doc_parser         | [B9E63344] Starting — parsing 3 document(s)
13:03:28 | DEBUG    | claims.agents.doc_parser         | [B9E63344] Parsing PRESCRIPTION (file_id=F012) from pre-supplied content
13:03:28 | DEBUG    | claims.agents.doc_parser         | [B9E63344] Extracted PRESCRIPTION — patient=— diagnosis=Suspected Lumbar Disc Herniation items=0
13:03:28 | DEBUG    | claims.agents.doc_parser         | [B9E63344] Parsing LAB_REPORT (file_id=F013) from pre-supplied content
13:03:28 | DEBUG    | claims.agents.doc_parser         | [B9E63344] Extracted LAB_REPORT — patient=— diagnosis=— items=0
13:03:28 | DEBUG    | claims.agents.doc_parser         | [B9E63344] Parsing HOSPITAL_BILL (file_id=F014) from pre-supplied content
13:03:28 | DEBUG    | claims.agents.doc_parser         | [B9E63344] Extracted HOSPITAL_BILL — patient=— diagnosis=— items=1
13:03:28 | INFO     | claims.agents.doc_parser         | [B9E63344] Complete — 3 extracted, 0 failed, confidence=1.00
13:03:28 | DEBUG    | claims.pipeline.graph            | [B9E63344] ← exiting node: DocParserAgent
13:03:28 | DEBUG    | claims.pipeline.graph            | [B9E63344] → entering node: DocValidatorAgent
13:03:28 | INFO     | claims.agents.doc_validator      | [B9E63344] Starting — category=DIAGNOSTIC docs=3
13:03:28 | DEBUG    | claims.agents.doc_validator      | [B9E63344] Required types: ['PRESCRIPTION', 'LAB_REPORT', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'LAB_REPORT': 1, 'HOSPITAL_BILL': 1}
13:03:28 | INFO     | claims.agents.doc_validator      | [B9E63344] PASS doc_types — all required docs present: PRESCRIPTION, LAB_REPORT, HOSPITAL_BILL
13:03:28 | INFO     | claims.agents.doc_validator      | [B9E63344] Complete — all document checks passed
13:03:28 | DEBUG    | claims.pipeline.graph            | [B9E63344] ← exiting node: DocValidatorAgent
13:03:28 | DEBUG    | claims.pipeline.graph            | [B9E63344] → entering node: DecisionMakerAgent
13:03:28 | INFO     | claims.agents.decision_maker     | [B9E63344] Starting — category=DIAGNOSTIC amount=₹15000.00 diagnosis=Suspected Lumbar Disc Herniation hospital=—
13:03:28 | DEBUG    | claims.agents.decision_maker     | [B9E63344] Calling Gemini for exclusion check — diagnosis='Suspected Lumbar Disc Herniation' treatment='—'
13:03:30 | DEBUG    | claims.agents.decision_maker     | [B9E63344] PASS exclusion_check — A lumbar disc herniation is a standard medical condition that does not fall under any of the listed exclusions such as self-inflicted injuries, elective cosmetic procedures, or specific excluded treatments like substance abuse or bariatric surgery.
13:03:30 | DEBUG    | claims.agents.decision_maker     | [B9E63344] Calling Gemini for waiting-period condition match — diagnosis='Suspected Lumbar Disc Herniation'
13:03:31 | DEBUG    | claims.agents.decision_maker     | [B9E63344] No specific waiting period matched — Lumbar disc herniation involves spinal discs, which is distinct from an abdominal or inguinal hernia (the type of hernia typically covered by such condition lists).
13:03:31 | WARNING  | claims.agents.decision_maker     | [B9E63344] REJECTED — pre-auth required for ['MRI Lumbar Spine'] ₹15000.00
13:03:31 | DEBUG    | claims.pipeline.graph            | [B9E63344] ← exiting node: DecisionMakerAgent
13:03:31 | INFO     | claims.pipeline.graph            | [B9E63344] Pipeline complete — decision=REJECTED approved=₹— confidence=1.0000 failures=none
```
