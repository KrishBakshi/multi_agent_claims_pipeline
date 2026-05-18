# TC003 — Documents Belong to Different Patients

> The prescription is for Rajesh Kumar but the hospital bill is for a different patient, Arjun Mehta.

**Claim ID:** `1D1CD9F2`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 0.00s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP001` |
| Claim Category | `CONSULTATION` |
| Treatment Date | 2024-11-01 |
| Claimed Amount | ₹1,500 |
| Policy ID | `PLUM_GHI_2024` |

**Documents submitted:**

- `prescription_rajesh.jpg`  type=`PRESCRIPTION`  👤 `Rajesh Kumar`
- `bill_arjun.jpg`  type=`HOSPITAL_BILL`  👤 `Arjun Mehta`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Rajesh Kumar' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-11-01 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹1500.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F005` | ⚠️ `WARNING` | No content or file data for F005 — skipping |
| 7 | `DocParserAgent` | `parse_F006` | ⚠️ `WARNING` | No content or file data for F006 — skipping |
| 8 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for CONSULTATION: PRESCRIPTION, HOSPITAL_BILL |
| 9 | `DocValidatorAgent` | `patient_name_consistency` | ❌ `FAIL` | Documents appear to belong to different patients: PRESCRIPTION (F005): 'rajesh kumar'; HOSPITAL_BILL (F006): 'arjun mehta'. All documents in a single claim must be for the same patient. Please review and resubmit with matching documents. |

---

## Decision

### 🛑 STOPPED

**Confidence:** 65%

**Stopped:** Documents appear to belong to different patients: PRESCRIPTION (F005): 'rajesh kumar'; HOSPITAL_BILL (F006): 'arjun mehta'. All documents in a single claim must be for the same patient. Please review and resubmit with matching documents.

**Reason:** Documents appear to belong to different patients: PRESCRIPTION (F005): 'rajesh kumar'; HOSPITAL_BILL (F006): 'arjun mehta'. All documents in a single claim must be for the same patient. Please review and resubmit with matching documents.

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `STOPPED (null)` | `STOPPED (null)` |

### Checks

✅ Pipeline stopped (no decision reached)
✅ System must: _Detect that the documents belong to different people_
✅ System must: _Surface this to the member with the specific names found on each document_
✅ System must: _Not proceed to a claim decision_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:17 | INFO     | claims.pipeline.graph            | [1D1CD9F2] Pipeline started — member=EMP001 category=CONSULTATION amount=₹1500.00 docs=2 simulate_failure=False
13:03:17 | DEBUG    | claims.pipeline.graph            | [1D1CD9F2] → entering node: DataValidatorAgent
13:03:17 | INFO     | claims.agents.data_validator     | [1D1CD9F2] Starting — member=EMP001 category=CONSULTATION amount=₹1500.00 docs=2
13:03:17 | DEBUG    | claims.agents.data_validator     | [1D1CD9F2] PASS policy_id — PLUM_GHI_2024
13:03:17 | INFO     | claims.agents.data_validator     | [1D1CD9F2] PASS member_lookup — 'Rajesh Kumar' (joined 2024-04-01)
13:03:17 | INFO     | claims.agents.data_validator     | [1D1CD9F2] PASS policy_period — treatment 2024-11-01 within [2024-04-01, 2025-03-31]
13:03:17 | DEBUG    | claims.agents.data_validator     | [1D1CD9F2] PASS category — CONSULTATION
13:03:17 | DEBUG    | claims.agents.data_validator     | [1D1CD9F2] PASS minimum_amount — ₹1500.00 ≥ ₹500
13:03:17 | INFO     | claims.agents.data_validator     | [1D1CD9F2] Complete — all checks passed
13:03:17 | DEBUG    | claims.pipeline.graph            | [1D1CD9F2] ← exiting node: DataValidatorAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [1D1CD9F2] → entering node: DocParserAgent
13:03:17 | INFO     | claims.agents.doc_parser         | [1D1CD9F2] Starting — parsing 2 document(s)
13:03:17 | WARNING  | claims.agents.doc_parser         | [1D1CD9F2] No content or file_data for PRESCRIPTION (file_id=F005) — skipping
13:03:17 | WARNING  | claims.agents.doc_parser         | [1D1CD9F2] No content or file_data for HOSPITAL_BILL (file_id=F006) — skipping
13:03:17 | INFO     | claims.agents.doc_parser         | [1D1CD9F2] Complete — 2 extracted, 0 failed, confidence=0.80
13:03:17 | DEBUG    | claims.pipeline.graph            | [1D1CD9F2] ← exiting node: DocParserAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [1D1CD9F2] → entering node: DocValidatorAgent
13:03:17 | INFO     | claims.agents.doc_validator      | [1D1CD9F2] Starting — category=CONSULTATION docs=2
13:03:17 | DEBUG    | claims.agents.doc_validator      | [1D1CD9F2] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'HOSPITAL_BILL': 1}
13:03:17 | INFO     | claims.agents.doc_validator      | [1D1CD9F2] PASS doc_types — all required docs present: PRESCRIPTION, HOSPITAL_BILL
13:03:17 | WARNING  | claims.agents.doc_validator      | [1D1CD9F2] Patient name mismatch across documents: PRESCRIPTION (F005): 'rajesh kumar'; HOSPITAL_BILL (F006): 'arjun mehta'
13:03:17 | WARNING  | claims.agents.doc_validator      | [1D1CD9F2] HALT [patient_name_consistency] — Documents appear to belong to different patients: PRESCRIPTION (F005): 'rajesh kumar'; HOSPITAL_BILL (F006): 'arjun mehta'. All documents in a single claim must be for the same patient. Please review and resubmit with matching documents.
13:03:17 | DEBUG    | claims.pipeline.graph            | [1D1CD9F2] ← exiting node: DocValidatorAgent
13:03:17 | WARNING  | claims.pipeline.graph            | [1D1CD9F2] Pipeline halted early — reason: Documents appear to belong to different patients: PRESCRIPTION (F005): 'rajesh kumar'; HOSPITAL_BILL (F006): 'arjun mehta'. All documents in a single claim must be for the same patient. Please review and resubmit with matching documents.
```
