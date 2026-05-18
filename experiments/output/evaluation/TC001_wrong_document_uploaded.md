# TC001 — Wrong Document Uploaded

> Member submits two prescriptions for a consultation claim that requires a prescription and a hospital bill.

**Claim ID:** `B112D30F`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 0.01s

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

- `dr_sharma_prescription.jpg`  type=`PRESCRIPTION`
- `another_prescription.jpg`  type=`PRESCRIPTION`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Rajesh Kumar' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-11-01 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹1500.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F001` | ⚠️ `WARNING` | No content or file data for F001 — skipping |
| 7 | `DocParserAgent` | `parse_F002` | ⚠️ `WARNING` | No content or file data for F002 — skipping |
| 8 | `DocValidatorAgent` | `doc_types` | ❌ `FAIL` | Missing required document(s) for a CONSULTATION claim: HOSPITAL_BILL. You uploaded: 2× PRESCRIPTION. Please provide the missing document(s) and resubmit. |

---

## Decision

### 🛑 STOPPED

**Confidence:** 65%

**Stopped:** Missing required document(s) for a CONSULTATION claim: HOSPITAL_BILL. You uploaded: 2× PRESCRIPTION. Please provide the missing document(s) and resubmit.

**Reason:** Missing required document(s) for a CONSULTATION claim: HOSPITAL_BILL. You uploaded: 2× PRESCRIPTION. Please provide the missing document(s) and resubmit.

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `STOPPED (null)` | `STOPPED (null)` |

### Checks

✅ Pipeline stopped (no decision reached)
✅ System must: _Stop before making any claim decision_
✅ System must: _Tell the member specifically what document type was uploaded and what is needed instead_
✅ System must: _Not return a generic error — the message must name the uploaded document type and the required document type_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:17 | INFO     | claims.pipeline.graph            | [B112D30F] Pipeline started — member=EMP001 category=CONSULTATION amount=₹1500.00 docs=2 simulate_failure=False
13:03:17 | DEBUG    | claims.pipeline.graph            | [B112D30F] → entering node: DataValidatorAgent
13:03:17 | INFO     | claims.agents.data_validator     | [B112D30F] Starting — member=EMP001 category=CONSULTATION amount=₹1500.00 docs=2
13:03:17 | DEBUG    | claims.agents.data_validator     | [B112D30F] PASS policy_id — PLUM_GHI_2024
13:03:17 | INFO     | claims.agents.data_validator     | [B112D30F] PASS member_lookup — 'Rajesh Kumar' (joined 2024-04-01)
13:03:17 | INFO     | claims.agents.data_validator     | [B112D30F] PASS policy_period — treatment 2024-11-01 within [2024-04-01, 2025-03-31]
13:03:17 | DEBUG    | claims.agents.data_validator     | [B112D30F] PASS category — CONSULTATION
13:03:17 | DEBUG    | claims.agents.data_validator     | [B112D30F] PASS minimum_amount — ₹1500.00 ≥ ₹500
13:03:17 | INFO     | claims.agents.data_validator     | [B112D30F] Complete — all checks passed
13:03:17 | DEBUG    | claims.pipeline.graph            | [B112D30F] ← exiting node: DataValidatorAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [B112D30F] → entering node: DocParserAgent
13:03:17 | INFO     | claims.agents.doc_parser         | [B112D30F] Starting — parsing 2 document(s)
13:03:17 | WARNING  | claims.agents.doc_parser         | [B112D30F] No content or file_data for PRESCRIPTION (file_id=F001) — skipping
13:03:17 | WARNING  | claims.agents.doc_parser         | [B112D30F] No content or file_data for PRESCRIPTION (file_id=F002) — skipping
13:03:17 | INFO     | claims.agents.doc_parser         | [B112D30F] Complete — 2 extracted, 0 failed, confidence=0.80
13:03:17 | DEBUG    | claims.pipeline.graph            | [B112D30F] ← exiting node: DocParserAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [B112D30F] → entering node: DocValidatorAgent
13:03:17 | INFO     | claims.agents.doc_validator      | [B112D30F] Starting — category=CONSULTATION docs=2
13:03:17 | DEBUG    | claims.agents.doc_validator      | [B112D30F] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 2}
13:03:17 | WARNING  | claims.agents.doc_validator      | [B112D30F] Missing required documents: HOSPITAL_BILL (uploaded: 2× PRESCRIPTION)
13:03:17 | WARNING  | claims.agents.doc_validator      | [B112D30F] HALT [doc_types] — Missing required document(s) for a CONSULTATION claim: HOSPITAL_BILL. You uploaded: 2× PRESCRIPTION. Please provide the missing document(s) and resubmit.
13:03:17 | DEBUG    | claims.pipeline.graph            | [B112D30F] ← exiting node: DocValidatorAgent
13:03:17 | WARNING  | claims.pipeline.graph            | [B112D30F] Pipeline halted early — reason: Missing required document(s) for a CONSULTATION claim: HOSPITAL_BILL. You uploaded: 2× PRESCRIPTION. Please provide the missing document(s) and resubmit.
```
