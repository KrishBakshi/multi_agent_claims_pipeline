# TC004 — Clean Consultation — Full Approval

> Complete, valid consultation claim with correct documents, valid member, covered treatment, within all limits.

**Claim ID:** `F8405546`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 8.23s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP001` |
| Claim Category | `CONSULTATION` |
| Treatment Date | 2024-11-01 |
| Claimed Amount | ₹1,500 |
| Policy ID | `PLUM_GHI_2024` |
| YTD Claims | ₹5,000 |

**Documents submitted:**

- `F007`  type=`PRESCRIPTION`
- `F008`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Rajesh Kumar' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-11-01 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'CONSULTATION' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹1500.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F007` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 7 | `DocParserAgent` | `parse_F008` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 8 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for CONSULTATION: PRESCRIPTION, HOSPITAL_BILL |
| 9 | `DocValidatorAgent` | `patient_name_consistency` | ✅ `PASS` | All named documents reference the same patient: 'rajesh kumar' |
| 10 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 11 | `DecisionMakerAgent` | `exclusion_check` | ✅ `PASS` | No exclusion matched. Viral fever is a common medical condition and is not listed in the policy exclusions provided. |
| 12 | `DecisionMakerAgent` | `waiting_period_initial` | ✅ `PASS` | Initial waiting period satisfied (214 days since join) |
| 13 | `DecisionMakerAgent` | `waiting_period_specific` | ✅ `PASS` | No specific waiting period matched. Viral fever is an acute, short-term illness and does not fall under the categories of chronic conditions or specific medical procedures listed in the waiting-period criteria. |
| 14 | `DecisionMakerAgent` | `pre_auth_check` | ✅ `PASS` | Pre-authorisation not required or already obtained |
| 15 | `DecisionMakerAgent` | `per_claim_limit` | ✅ `PASS` | Claimed ₹1500.0 within per-claim limit ₹5000 |
| 16 | `DecisionMakerAgent` | `sub_limit` | ℹ️ `INFO` | Annual sub-limit for CONSULTATION: ₹2000.0 (YTD tracking not applied per-claim) |
| 17 | `DecisionMakerAgent` | `copay` | ℹ️ `INFO` | Co-pay 10% applied: ₹1500.0 → ₹1350.0 (deducted ₹150.0) |
| 18 | `DecisionMakerAgent` | `final_decision` | ℹ️ `INFO` | Decision: APPROVED \| Approved: ₹1350.0 |

---

## Decision

### 🟢 APPROVED

**Confidence:** 100%

**Reason:** Claim approved for ₹1350.0. Co-pay (10%) of ₹150.0 deducted.

### Amount Breakdown

| | Amount |
|--|--|
| Claimed | ₹1,500.00 |
| Co-pay (10%) | − ₹150.00 |
| **Approved** | **₹1,350.00** |

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `APPROVED` | `APPROVED` |
| Approved amount | ₹1,350 | ₹1,350.00 |

### Checks

✅ Decision: expected **APPROVED**, got **APPROVED**
✅ Approved amount: expected ₹1,350, got ₹1,350.00
✅ Confidence ≥ 85% (actual 100%)

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:17 | INFO     | claims.pipeline.graph            | [F8405546] Pipeline started — member=EMP001 category=CONSULTATION amount=₹1500.00 docs=2 simulate_failure=False
13:03:17 | DEBUG    | claims.pipeline.graph            | [F8405546] → entering node: DataValidatorAgent
13:03:17 | INFO     | claims.agents.data_validator     | [F8405546] Starting — member=EMP001 category=CONSULTATION amount=₹1500.00 docs=2
13:03:17 | DEBUG    | claims.agents.data_validator     | [F8405546] PASS policy_id — PLUM_GHI_2024
13:03:17 | INFO     | claims.agents.data_validator     | [F8405546] PASS member_lookup — 'Rajesh Kumar' (joined 2024-04-01)
13:03:17 | INFO     | claims.agents.data_validator     | [F8405546] PASS policy_period — treatment 2024-11-01 within [2024-04-01, 2025-03-31]
13:03:17 | DEBUG    | claims.agents.data_validator     | [F8405546] PASS category — CONSULTATION
13:03:17 | DEBUG    | claims.agents.data_validator     | [F8405546] PASS minimum_amount — ₹1500.00 ≥ ₹500
13:03:17 | INFO     | claims.agents.data_validator     | [F8405546] Complete — all checks passed
13:03:17 | DEBUG    | claims.pipeline.graph            | [F8405546] ← exiting node: DataValidatorAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [F8405546] → entering node: DocParserAgent
13:03:17 | INFO     | claims.agents.doc_parser         | [F8405546] Starting — parsing 2 document(s)
13:03:17 | DEBUG    | claims.agents.doc_parser         | [F8405546] Parsing PRESCRIPTION (file_id=F007) from pre-supplied content
13:03:17 | DEBUG    | claims.agents.doc_parser         | [F8405546] Extracted PRESCRIPTION — patient=Rajesh Kumar diagnosis=Viral Fever items=0
13:03:17 | DEBUG    | claims.agents.doc_parser         | [F8405546] Parsing HOSPITAL_BILL (file_id=F008) from pre-supplied content
13:03:17 | DEBUG    | claims.agents.doc_parser         | [F8405546] Extracted HOSPITAL_BILL — patient=Rajesh Kumar diagnosis=— items=3
13:03:17 | INFO     | claims.agents.doc_parser         | [F8405546] Complete — 2 extracted, 0 failed, confidence=1.00
13:03:17 | DEBUG    | claims.pipeline.graph            | [F8405546] ← exiting node: DocParserAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [F8405546] → entering node: DocValidatorAgent
13:03:17 | INFO     | claims.agents.doc_validator      | [F8405546] Starting — category=CONSULTATION docs=2
13:03:17 | DEBUG    | claims.agents.doc_validator      | [F8405546] Required types: ['PRESCRIPTION', 'HOSPITAL_BILL'] | Uploaded: {'PRESCRIPTION': 1, 'HOSPITAL_BILL': 1}
13:03:17 | INFO     | claims.agents.doc_validator      | [F8405546] PASS doc_types — all required docs present: PRESCRIPTION, HOSPITAL_BILL
13:03:17 | INFO     | claims.agents.doc_validator      | [F8405546] PASS patient_name_consistency — all docs reference 'rajesh kumar'
13:03:17 | INFO     | claims.agents.doc_validator      | [F8405546] Complete — all document checks passed
13:03:17 | DEBUG    | claims.pipeline.graph            | [F8405546] ← exiting node: DocValidatorAgent
13:03:17 | DEBUG    | claims.pipeline.graph            | [F8405546] → entering node: DecisionMakerAgent
13:03:17 | INFO     | claims.agents.decision_maker     | [F8405546] Starting — category=CONSULTATION amount=₹1500.00 diagnosis=Viral Fever hospital=City Clinic, Bengaluru
13:03:17 | DEBUG    | claims.agents.decision_maker     | [F8405546] Calling Gemini for exclusion check — diagnosis='Viral Fever' treatment='—'
13:03:23 | DEBUG    | claims.agents.decision_maker     | [F8405546] PASS exclusion_check — Viral fever is a common medical condition and is not listed in the policy exclusions provided.
13:03:23 | DEBUG    | claims.agents.decision_maker     | [F8405546] Calling Gemini for waiting-period condition match — diagnosis='Viral Fever'
13:03:25 | DEBUG    | claims.agents.decision_maker     | [F8405546] No specific waiting period matched — Viral fever is an acute, short-term illness and does not fall under the categories of chronic conditions or specific medical procedures listed in the waiting-period criteria.
13:03:25 | INFO     | claims.agents.decision_maker     | [F8405546] Complete — decision=APPROVED approved=₹1350.00 confidence=1.00 network=NO
13:03:25 | DEBUG    | claims.pipeline.graph            | [F8405546] ← exiting node: DecisionMakerAgent
13:03:25 | INFO     | claims.pipeline.graph            | [F8405546] Pipeline complete — decision=APPROVED approved=₹1350.00 confidence=1.0000 failures=none
```
