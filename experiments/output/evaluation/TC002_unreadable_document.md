# TC002 — Unreadable Document

> Member uploads a valid prescription but a blurry, unreadable photo of their pharmacy bill.

**Claim ID:** `DC4662C9`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 0.00s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP004` |
| Claim Category | `PHARMACY` |
| Treatment Date | 2024-10-25 |
| Claimed Amount | ₹800 |
| Policy ID | `PLUM_GHI_2024` |

**Documents submitted:**

- `prescription.jpg`  type=`PRESCRIPTION`
- `blurry_bill.jpg`  type=`PHARMACY_BILL`  ⚠️ quality=`UNREADABLE`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Sneha Reddy' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-10-25 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'PHARMACY' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹800.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F003` | ⚠️ `WARNING` | No content or file data for F003 — skipping |
| 7 | `DocParserAgent` | `quality_F004` | ⚠️ `WARNING` | PHARMACY_BILL (file_id=F004) is unreadable — member must re-upload a clear copy |
| 8 | `DocValidatorAgent` | `doc_quality` | ❌ `FAIL` | The following document(s) could not be read: PHARMACY_BILL (file: blurry_bill.jpg). Please re-upload a clear, well-lit photo or scan of each. |

---

## Decision

### 🛑 STOPPED

**Confidence:** 60%

**Stopped:** The following document(s) could not be read: PHARMACY_BILL (file: blurry_bill.jpg). Please re-upload a clear, well-lit photo or scan of each.

**Reason:** The following document(s) could not be read: PHARMACY_BILL (file: blurry_bill.jpg). Please re-upload a clear, well-lit photo or scan of each.

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `STOPPED (null)` | `STOPPED (null)` |

### Checks

✅ Pipeline stopped (no decision reached)
✅ System must: _Identify that the pharmacy bill cannot be read_
✅ System must: _Ask the member to re-upload that specific document_
✅ System must: _Not reject the claim outright_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:17 | INFO     | claims.pipeline.graph            | [DC4662C9] Pipeline started — member=EMP004 category=PHARMACY amount=₹800.00 docs=2 simulate_failure=False
13:03:17 | DEBUG    | claims.pipeline.graph            | [DC4662C9] → entering node: DataValidatorAgent
13:03:17 | INFO     | claims.agents.data_validator     | [DC4662C9] Starting — member=EMP004 category=PHARMACY amount=₹800.00 docs=2
13:03:17 | DEBUG    | claims.agents.data_validator     | [DC4662C9] PASS policy_id — PLUM_GHI_2024
13:03:17 | INFO     | claims.agents.data_validator     | [DC4662C9] PASS member_lookup — 'Sneha Reddy' (joined 2024-04-01)
13:03:17 | INFO     | claims.agents.data_validator     | [DC4662C9] PASS policy_period — treatment 2024-10-25 within [2024-04-01, 2025-03-31]
13:03:17 | DEBUG    | claims.agents.data_validator     | [DC4662C9] PASS category — PHARMACY
13:03:17 | DEBUG    | claims.agents.data_validator     | [DC4662C9] PASS minimum_amount — ₹800.00 ≥ ₹500
13:03:17 | INFO     | claims.agents.data_validator     | [DC4662C9] Complete — all checks passed
13:03:17 | DEBUG    | claims.pipeline.graph            | [DC4662C9] ← exiting node: DataValidatorAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [DC4662C9] → entering node: DocParserAgent
13:03:17 | INFO     | claims.agents.doc_parser         | [DC4662C9] Starting — parsing 2 document(s)
13:03:17 | WARNING  | claims.agents.doc_parser         | [DC4662C9] No content or file_data for PRESCRIPTION (file_id=F003) — skipping
13:03:17 | WARNING  | claims.agents.doc_parser         | [DC4662C9] UNREADABLE PHARMACY_BILL (file_id=F004) — member must re-upload
13:03:17 | INFO     | claims.agents.doc_parser         | [DC4662C9] Complete — 2 extracted, 0 failed, confidence=0.75
13:03:17 | DEBUG    | claims.pipeline.graph            | [DC4662C9] ← exiting node: DocParserAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [DC4662C9] → entering node: DocValidatorAgent
13:03:17 | INFO     | claims.agents.doc_validator      | [DC4662C9] Starting — category=PHARMACY docs=2
13:03:17 | WARNING  | claims.agents.doc_validator      | [DC4662C9] Unreadable documents detected: PHARMACY_BILL (file: blurry_bill.jpg)
13:03:17 | WARNING  | claims.agents.doc_validator      | [DC4662C9] HALT [doc_quality] — The following document(s) could not be read: PHARMACY_BILL (file: blurry_bill.jpg). Please re-upload a clear, well-lit photo or scan of each.
13:03:17 | DEBUG    | claims.pipeline.graph            | [DC4662C9] ← exiting node: DocValidatorAgent
13:03:17 | WARNING  | claims.pipeline.graph            | [DC4662C9] Pipeline halted early — reason: The following document(s) could not be read: PHARMACY_BILL (file: blurry_bill.jpg). Please re-upload a clear, well-lit photo or scan of each.
```
