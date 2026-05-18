# TC006 — Dental Partial Approval — Cosmetic Exclusion

> Bill includes root canal treatment (covered) and teeth whitening (cosmetic, excluded). System must approve only the covered procedure.

**Claim ID:** `033AA9BD`  
**Run:** 2026-05-18 13:03:17  
**Duration:** 0.01s

---

## Input

| Field | Value |
|-------|-------|
| Member ID | `EMP002` |
| Claim Category | `DENTAL` |
| Treatment Date | 2024-10-15 |
| Claimed Amount | ₹12,000 |
| Policy ID | `PLUM_GHI_2024` |

**Documents submitted:**

- `F011`  type=`HOSPITAL_BILL`

---

## Pipeline Trace

| # | Agent | Step | Result | Detail |
|---|-------|------|--------|--------|
| 1 | `DataValidatorAgent` | `member_lookup` | ✅ `PASS` | Member 'Priya Singh' found (joined 2024-04-01) |
| 2 | `DataValidatorAgent` | `policy_period` | ✅ `PASS` | Treatment date 2024-10-15 is within policy period (2024-04-01 → 2025-03-31) |
| 3 | `DataValidatorAgent` | `category_valid` | ✅ `PASS` | Category 'DENTAL' is valid |
| 4 | `DataValidatorAgent` | `minimum_amount` | ✅ `PASS` | Claimed ₹12000.0 meets minimum ₹500 |
| 5 | `DataValidatorAgent` | `data_validation` | ✅ `PASS` | All claim fields validated successfully |
| 6 | `DocParserAgent` | `parse_F011` | ✅ `PASS` | Parsed HOSPITAL_BILL (quality=GOOD, confidence=1.00) |
| 7 | `DocValidatorAgent` | `doc_types` | ✅ `PASS` | All required documents present for DENTAL: HOSPITAL_BILL |
| 8 | `DocValidatorAgent` | `doc_validation` | ✅ `PASS` | Document validation passed all checks |
| 9 | `DecisionMakerAgent` | `waiting_period_initial` | ✅ `PASS` | Initial waiting period satisfied (197 days since join) |
| 10 | `DecisionMakerAgent` | `pre_auth_check` | ✅ `PASS` | Pre-authorisation not required or already obtained |
| 11 | `DecisionMakerAgent` | `line_item` | ✅ `PASS` | Approved: Root Canal Treatment ₹8000.0 |
| 12 | `DecisionMakerAgent` | `line_item` | ❌ `FAIL` | Rejected: Teeth Whitening ₹4000.0 — excluded |
| 13 | `DecisionMakerAgent` | `per_claim_limit` | ✅ `PASS` | Approved dental amount ₹8000.0 within sub-limit ₹10000.0 |
| 14 | `DecisionMakerAgent` | `sub_limit` | ℹ️ `INFO` | Annual sub-limit for DENTAL: ₹10000.0 (YTD tracking not applied per-claim) |
| 15 | `DecisionMakerAgent` | `final_decision` | ℹ️ `INFO` | Decision: PARTIAL \| Approved: ₹8000.0 |

---

## Decision

### 🟡 PARTIAL

**Confidence:** 100%

**Reason:** Claim partially approved for ₹8000.0 of ₹12000.0 claimed. Some line items were excluded — see line-item breakdown for details.

### Amount Breakdown

| | Amount |
|--|--|
| Claimed | ₹12,000.00 |
| **Approved** | **₹8,000.00** |

### Line Item Decisions

✅ **Root Canal Treatment** ₹8,000.00
❌ **Teeth Whitening** ₹4,000.00 — 'Teeth Whitening' is a cosmetic/excluded procedure under the dental policy.

---

## Expected vs Actual

| | Expected | Actual |
|--|----------|--------|
| Decision | `PARTIAL` | `PARTIAL` |
| Approved amount | ₹8,000 | ₹8,000.00 |

### Checks

✅ Decision: expected **PARTIAL**, got **PARTIAL**
✅ Approved amount: expected ₹8,000, got ₹8,000.00
✅ System must: _Itemize which line items were approved and which were rejected_
✅ System must: _State the reason for each rejection at the line-item level_

### Verdict: ✅ **PASS**

---

## Raw Logs

```
13:03:28 | INFO     | claims.pipeline.graph            | [033AA9BD] Pipeline started — member=EMP002 category=DENTAL amount=₹12000.00 docs=1 simulate_failure=False
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] → entering node: DataValidatorAgent
13:03:28 | INFO     | claims.agents.data_validator     | [033AA9BD] Starting — member=EMP002 category=DENTAL amount=₹12000.00 docs=1
13:03:28 | DEBUG    | claims.agents.data_validator     | [033AA9BD] PASS policy_id — PLUM_GHI_2024
13:03:28 | INFO     | claims.agents.data_validator     | [033AA9BD] PASS member_lookup — 'Priya Singh' (joined 2024-04-01)
13:03:28 | INFO     | claims.agents.data_validator     | [033AA9BD] PASS policy_period — treatment 2024-10-15 within [2024-04-01, 2025-03-31]
13:03:28 | DEBUG    | claims.agents.data_validator     | [033AA9BD] PASS category — DENTAL
13:03:28 | DEBUG    | claims.agents.data_validator     | [033AA9BD] PASS minimum_amount — ₹12000.00 ≥ ₹500
13:03:28 | INFO     | claims.agents.data_validator     | [033AA9BD] Complete — all checks passed
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] ← exiting node: DataValidatorAgent
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] → entering node: DocParserAgent
13:03:28 | INFO     | claims.agents.doc_parser         | [033AA9BD] Starting — parsing 1 document(s)
13:03:28 | DEBUG    | claims.agents.doc_parser         | [033AA9BD] Parsing HOSPITAL_BILL (file_id=F011) from pre-supplied content
13:03:28 | DEBUG    | claims.agents.doc_parser         | [033AA9BD] Extracted HOSPITAL_BILL — patient=Priya Singh diagnosis=— items=2
13:03:28 | INFO     | claims.agents.doc_parser         | [033AA9BD] Complete — 1 extracted, 0 failed, confidence=1.00
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] ← exiting node: DocParserAgent
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] → entering node: DocValidatorAgent
13:03:28 | INFO     | claims.agents.doc_validator      | [033AA9BD] Starting — category=DENTAL docs=1
13:03:28 | DEBUG    | claims.agents.doc_validator      | [033AA9BD] Required types: ['HOSPITAL_BILL'] | Uploaded: {'HOSPITAL_BILL': 1}
13:03:28 | INFO     | claims.agents.doc_validator      | [033AA9BD] PASS doc_types — all required docs present: HOSPITAL_BILL
13:03:28 | INFO     | claims.agents.doc_validator      | [033AA9BD] Complete — all document checks passed
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] ← exiting node: DocValidatorAgent
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] → entering node: DecisionMakerAgent
13:03:28 | INFO     | claims.agents.decision_maker     | [033AA9BD] Starting — category=DENTAL amount=₹12000.00 diagnosis=— hospital=Smile Dental Clinic
13:03:28 | INFO     | claims.agents.decision_maker     | [033AA9BD] Complete — decision=PARTIAL approved=₹8000.00 confidence=1.00 network=NO
13:03:28 | DEBUG    | claims.pipeline.graph            | [033AA9BD] ← exiting node: DecisionMakerAgent
13:03:28 | INFO     | claims.pipeline.graph            | [033AA9BD] Pipeline complete — decision=PARTIAL approved=₹8000.00 confidence=1.0000 failures=none
```
