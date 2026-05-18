# TC010 — Network Hospital — Discount Applied

> Valid claim at Apollo Hospitals, a network hospital. Network discount must be applied before co-pay.

**Claim ID:** `A09237F5`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 2.96s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP010` |
| Claim Category | `CONSULTATION` |
| Treatment Date | 2024-11-03 |
| Claimed Amount | ₹4,500 |
| Policy ID | `PLUM_GHI_2024` |
| Hospital | Apollo Hospitals |
| YTD Claims | ₹8,000 |

**Documents submitted:**

- `F019`  type=`PRESCRIPTION`
- `F020`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Deepak Shah' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-11-03 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹4500.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F019` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 7 | `DocParserAgent` | `parse_F020` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 8 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for CONSULTATION: PRESCRIPTION, HOSPITAL_BILL |
| 9 | `DocValidatorAgent` | `patient_name_consistency` | ✅ `PASS` | All named documents reference the same patient: 'deepak shah' |
| 10 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 11 | `DecisionMakerAgent` | `exclusion_check` | ✅ `PASS` | No exclusion matched. Acute Bronchitis is a common medical condition and does not fall under any of the listed exclusions such as self-inflicted injuries, cosmetic procedures, or elective treatments. |
| 12 | `DecisionMakerAgent` | `waiting_period_initial` | ✅ `PASS` | Initial waiting period satisfied (216 days since join) |
| 13 | `DecisionMakerAgent` | `waiting_period_specific` | ✅ `PASS` | No specific waiting period matched. Acute bronchitis is a short-term respiratory infection and does not fall under the listed chronic or elective conditions. |
| 14 | `DecisionMakerAgent` | `pre_auth_check` | ✅ `PASS` | Pre-authorisation not required or already obtained |
| 15 | `DecisionMakerAgent` | `per_claim_limit` | ✅ `PASS` | Claimed ₹4500.0 within per-claim limit ₹5000 |
| 16 | `DecisionMakerAgent` | `sub_limit` | ℹ️ `INFO` | Annual sub-limit for CONSULTATION: ₹2000.0 (YTD tracking not applied per-claim) |
| 17 | `DecisionMakerAgent` | `network_discount` | ℹ️ `INFO` | Network discount 20% applied: ₹4500.0 → ₹3600.0 |
| 18 | `DecisionMakerAgent` | `copay` | ℹ️ `INFO` | Co-pay 10% applied: ₹3600.0 → ₹3240.0 (deducted ₹360.0) |
| 19 | `DecisionMakerAgent` | `final_decision` | ℹ️ `INFO` | Decision: APPROVED \| Approved: ₹3240.0 |

---

## Decision

### 🟢 APPROVED

**Confidence:** 100%

**Reason:** Claim approved for ₹3240.0. Network discount (20%) of ₹900.0 applied. Co-pay (10%) of ₹360.0 deducted.

### Amount Breakdown

| | Amount |
|--|--|
| Claimed | ₹4,500.00 |
| Network discount (20%) | − ₹900.00 |
| After discount | ₹3,600.00 |
| Co-pay (10%) | − ₹360.00 |
| **Approved** | **₹3,240.00** |

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `APPROVED` | `APPROVED` |
| Approved amount | ₹3,240 | ₹3,240.00 |

### Checks

✅ Decision: expected **APPROVED**, got **APPROVED**
✅ Approved amount: expected ₹3,240, got ₹3,240.00
✅ System must: _Apply network discount before co-pay, not after_
✅ System must: _Show the breakdown of discount and co-pay in the decision output_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:34 | INFO     | claims.pipeline.graph            | [A09237F5] Pipeline started — member=EMP010 category=CONSULTATION amount=₹4500.00 docs=2 simulate_failure=False
13:03:34 | DEBUG    | claims.pipeline.graph            | [A09237F5] → entering node: DataValidatorAgent
13:03:34 | INFO     | claims.agents.data_validator     | [A09237F5] Starting — member=EMP010 category=CONSULTATION amount=₹4500.00 docs=2
13:03:34 | DEBUG    | claims.agents.data_validator     | [A09237F5] PASS policy_id — PLUM_GHI_2024
13:03:34 | INFO     | claims.agents.data_validator     | [A09237F5] PASS member_lookup — 'Deepak Shah' (joined 2024-04-01)
13:03:34 | INFO     | claims.agents.data_validator     | [A09237F5] PASS policy_period — treatment 2024-11-03 within [2024-04-01, 2025-03-31]
13:03:34 | DEBUG    | claims.agents.data_validator     | [A09237F5] PASS category — CONSULTATION
13:03:34 | DEBUG    | claims.agents.data_validator     | [A09237F5] PASS minimum_amount — ₹4500.00 ≥ ₹500
13:03:34 | INFO     | claims.agents.data_validator     | [A09237F5] Complete — all checks passed
13:03:34 | DEBUG    | claims.pipeline.graph            | [A09237F5] ← exiting node: DataValidatorAgent
13:03:34 | DEBUG    | claims.pipeline.graph            | [A09237F5] → entering node: DocParserAgent
13:03:34 | INFO     | claims.agents.doc_parser         | [A09237F5] Starting — parsing 2 document(s)
13:03:34 | DEBUG    | claims.agents.doc_parser         | [A09237F5] Parsing PRESCRIPTION (file_id=F019) from pre-supplied content
13:03:34 | DEBUG    | claims.agents.doc_parser         | [A09237F5] Extracted PRESCRIPTION — patient=Deepak Shah diagnosis=Acute Bronchitis items=0
13:03:34 | DEBUG    | claims.agents.doc_parser         | [A09237F5] Parsing HOSPITAL_BILL (file_id=F020) from pre-supplied content
13:03:34 | DEBUG    | claims.agents.doc_parser         | [A09237F5] Extracted HOSPITAL_BILL — patient=Deepak Shah diagnosis=— items=2
13:03:34 | INFO     | claims.agents.doc_parser         | [A09237F5] Complete — 2 extracted, 0 failed, confidence=1.00
13:03:34 | DEBUG    | claims.pipeline.graph            | [A09237F5] ← exiting node: DocParserAgent
13:03:34 | DEBUG    | claims.pipeline.graph            | [A09237F5] → entering node: DocValidatorAgent
13:03:34 | INFO     | claims.agents.doc_validator      | [A09237F5] Starting — category=CONSULTATION docs=2
13:03:34 | DEBUG    | claims.agents.doc_validator      | [A09237F5] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'HOSPITAL_BILL': 1}
13:03:34 | INFO     | claims.agents.doc_validator      | [A09237F5] PASS doc_types — all required docs present: PRESCRIPTION, HOSPITAL_BILL
13:03:34 | INFO     | claims.agents.doc_validator      | [A09237F5] PASS patient_name_consistency — all docs reference 'deepak shah'
13:03:34 | INFO     | claims.agents.doc_validator      | [A09237F5] Complete — all document checks passed
13:03:34 | DEBUG    | claims.pipeline.graph            | [A09237F5] ← exiting node: DocValidatorAgent
13:03:34 | DEBUG    | claims.pipeline.graph            | [A09237F5] → entering node: DecisionMakerAgent
13:03:34 | INFO     | claims.agents.decision_maker     | [A09237F5] Starting — category=CONSULTATION amount=₹4500.00 diagnosis=Acute Bronchitis hospital=Apollo Hospitals
13:03:34 | DEBUG    | claims.agents.decision_maker     | [A09237F5] Calling Gemini for exclusion check — diagnosis='Acute Bronchitis' treatment='—'
13:03:35 | DEBUG    | claims.agents.decision_maker     | [A09237F5] PASS exclusion_check — Acute Bronchitis is a common medical condition and does not fall under any of the listed exclusions such as self-inflicted injuries, cosmetic procedures, or elective treatments.
13:03:35 | DEBUG    | claims.agents.decision_maker     | [A09237F5] Calling Gemini for waiting-period condition match — diagnosis='Acute Bronchitis'
13:03:37 | DEBUG    | claims.agents.decision_maker     | [A09237F5] No specific waiting period matched — Acute bronchitis is a short-term respiratory infection and does not fall under the listed chronic or elective conditions.
13:03:37 | INFO     | claims.agents.decision_maker     | [A09237F5] Complete — decision=APPROVED approved=₹3240.00 confidence=1.00 network=YES
13:03:37 | DEBUG    | claims.pipeline.graph            | [A09237F5] ← exiting node: DecisionMakerAgent
13:03:37 | INFO     | claims.pipeline.graph            | [A09237F5] Pipeline complete — decision=APPROVED approved=₹3240.00 confidence=1.0000 failures=none
```
