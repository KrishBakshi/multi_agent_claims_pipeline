# TC011 — Component Failure — Graceful Degradation

> One component of your system fails mid-processing (simulate with the flag below). The overall pipeline must continue, produce a decision, and make the failure visible in the output with an appropriately reduced confidence score.

**Claim ID:** `BCAB69A2`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 3.24s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP006` |
| Claim Category | `ALTERNATIVE_MEDICINE` |
| Treatment Date | 2024-10-28 |
| Claimed Amount | ₹4,000 |
| Policy ID | `PLUM_GHI_2024` |
| Component Failure | ⚡ Simulated |

**Documents submitted:**

- `F021`  type=`PRESCRIPTION`
- `F022`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `simulate_failure` | 🔥 `ERROR` | Simulated component failure — continuing with degraded confidence |
| 2 | `DocParserAgent` | `parse_F021` | ✅ `PASS` | Parsed PRESCRIPTION (quality=GOOD, confidence=1.00) |
| 3 | `DocParserAgent` | `parse_F022` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 4 | `DocValidatorAgent` | `simulate_failure` | 🔥 `ERROR` | Simulated component failure in DocValidatorAgent — skipping doc validation |
| 5 | `DecisionMakerAgent` | `exclusion_check` | ✅ `PASS` | No exclusion matched. Panchakarma therapy is not explicitly listed in the provided policy exclusions, nor does it fall under the broad categories such as experimental treatments or cosmetic procedures based strictly on the provided list. |
| 6 | `DecisionMakerAgent` | `waiting_period_initial` | ✅ `PASS` | Initial waiting period satisfied (210 days since join) |
| 7 | `DecisionMakerAgent` | `waiting_period_specific` | ✅ `PASS` | No specific waiting period matched. Chronic joint pain does not fall under the specified waiting-period conditions like diabetes, hypertension, or joint replacement, and Panchakarma is an alternative therapy not listed as a condition. |
| 8 | `DecisionMakerAgent` | `pre_auth_check` | ✅ `PASS` | Pre-authorisation not required or already obtained |
| 9 | `DecisionMakerAgent` | `per_claim_limit` | ✅ `PASS` | Claimed ₹4000.0 within per-claim limit ₹5000 |
| 10 | `DecisionMakerAgent` | `sub_limit` | ℹ️ `INFO` | Annual sub-limit for ALTERNATIVE_MEDICINE: ₹8000.0 (YTD tracking not applied per-claim) |
| 11 | `DecisionMakerAgent` | `final_decision` | ℹ️ `INFO` | Decision: APPROVED \| Approved: ₹4000.0 |

---

## Decision

### 🟢 APPROVED

**Confidence:** 65%

**Reason:** Claim approved for ₹4000.0. Note: manual review recommended due to incomplete processing.

**⚡ Component failures:** `DataValidatorAgent`, `DocValidatorAgent`

### Amount Breakdown

| | Amount |
|--|--|
| Claimed | ₹4,000.00 |
| **Approved** | **₹4,000.00** |

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `APPROVED` | `APPROVED` |

### Checks

✅ Decision: expected **APPROVED**, got **APPROVED**
⚠️  System must: _Not crash or return a 500 error_
✅ System must: _Indicate in the output that a component failed and was skipped_
⚠️  System must: _Return a confidence score lower than a normal full-pipeline approval_
✅ System must: _Include a note that manual review is recommended due to incomplete processing_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:37 | INFO     | claims.pipeline.graph            | [BCAB69A2] Pipeline started — member=EMP006 category=ALTERNATIVE_MEDICINE amount=₹4000.00 docs=2 simulate_failure=True
13:03:37 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] → entering node: DataValidatorAgent
13:03:37 | INFO     | claims.agents.data_validator     | [BCAB69A2] Starting — member=EMP006 category=ALTERNATIVE_MEDICINE amount=₹4000.00 docs=2
13:03:37 | WARNING  | claims.agents.data_validator     | [BCAB69A2] Simulated component failure triggered — continuing degraded
13:03:37 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] ← exiting node: DataValidatorAgent
13:03:37 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] → entering node: DocParserAgent
13:03:37 | INFO     | claims.agents.doc_parser         | [BCAB69A2] Starting — parsing 2 document(s)
13:03:37 | DEBUG    | claims.agents.doc_parser         | [BCAB69A2] Parsing PRESCRIPTION (file_id=F021) from pre-supplied content
13:03:37 | DEBUG    | claims.agents.doc_parser         | [BCAB69A2] Extracted PRESCRIPTION — patient=— diagnosis=Chronic Joint Pain items=0
13:03:37 | DEBUG    | claims.agents.doc_parser         | [BCAB69A2] Parsing HOSPITAL_BILL (file_id=F022) from pre-supplied content
13:03:37 | DEBUG    | claims.agents.doc_parser         | [BCAB69A2] Extracted HOSPITAL_BILL — patient=— diagnosis=— items=2
13:03:37 | INFO     | claims.agents.doc_parser         | [BCAB69A2] Complete — 2 extracted, 0 failed, confidence=0.80
13:03:37 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] ← exiting node: DocParserAgent
13:03:37 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] → entering node: DocValidatorAgent
13:03:37 | INFO     | claims.agents.doc_validator      | [BCAB69A2] Starting — category=ALTERNATIVE_MEDICINE docs=2
13:03:37 | WARNING  | claims.agents.doc_validator      | [BCAB69A2] Simulated component failure triggered — skipping doc validation
13:03:37 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] ← exiting node: DocValidatorAgent
13:03:37 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] → entering node: DecisionMakerAgent
13:03:37 | INFO     | claims.agents.decision_maker     | [BCAB69A2] Starting — category=ALTERNATIVE_MEDICINE amount=₹4000.00 diagnosis=Chronic Joint Pain hospital=Ayur Wellness Centre
13:03:37 | DEBUG    | claims.agents.decision_maker     | [BCAB69A2] Calling Gemini for exclusion check — diagnosis='Chronic Joint Pain' treatment='Panchakarma Therapy'
13:03:38 | DEBUG    | claims.agents.decision_maker     | [BCAB69A2] PASS exclusion_check — Panchakarma therapy is not explicitly listed in the provided policy exclusions, nor does it fall under the broad categories such as experimental treatments or cosmetic procedures based strictly on the provided list.
13:03:38 | DEBUG    | claims.agents.decision_maker     | [BCAB69A2] Calling Gemini for waiting-period condition match — diagnosis='Chronic Joint Pain'
13:03:40 | DEBUG    | claims.agents.decision_maker     | [BCAB69A2] No specific waiting period matched — Chronic joint pain does not fall under the specified waiting-period conditions like diabetes, hypertension, or joint replacement, and Panchakarma is an alternative therapy not listed as a condition.
13:03:40 | INFO     | claims.agents.decision_maker     | [BCAB69A2] Complete — decision=APPROVED approved=₹4000.00 confidence=0.65 network=NO
13:03:40 | DEBUG    | claims.pipeline.graph            | [BCAB69A2] ← exiting node: DecisionMakerAgent
13:03:40 | INFO     | claims.pipeline.graph            | [BCAB69A2] Pipeline complete — decision=APPROVED approved=₹4000.00 confidence=0.6500 failures=['DataValidatorAgent', 'DocValidatorAgent']
```
