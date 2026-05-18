# Evaluation Summary

**Run:** 2026-05-18 13:03:17  
**Total duration:** 24.5s  
**Result: 12/12 PASS**  ✅

---

| Case | Name | Expected | Actual | Approved | Confidence | Verdict | Time |
|------|------|----------|--------|----------|------------|---------|------|
| **TC001** | Wrong Document Uploaded | 🛑 STOPPED | 🛑 STOPPED | — | 65% | ✅ | 0.0s |
| **TC002** | Unreadable Document | 🛑 STOPPED | 🛑 STOPPED | — | 60% | ✅ | 0.0s |
| **TC003** | Documents Belong to Different Patients | 🛑 STOPPED | 🛑 STOPPED | — | 65% | ✅ | 0.0s |
| **TC004** | Clean Consultation — Full Approval | 🟢 APPROVED | 🟢 APPROVED | ₹1,350 | 100% | ✅ | 8.2s |
| **TC005** | Waiting Period — Diabetes | 🔴 REJECTED | 🔴 REJECTED | — | 100% | ✅ | 2.7s |
| **TC006** | Dental Partial Approval — Cosmetic Exclusion | 🟡 PARTIAL | 🟡 PARTIAL | ₹8,000 | 100% | ✅ | 0.0s |
| **TC007** | MRI Without Pre-Authorization | 🔴 REJECTED | 🔴 REJECTED | — | 100% | ✅ | 3.5s |
| **TC008** | Per-Claim Limit Exceeded | 🔴 REJECTED | 🔴 REJECTED | — | 100% | ✅ | 2.6s |
| **TC009** | Fraud Signal — Multiple Same-Day Claims | 🟠 MANUAL REVIEW | 🟠 MANUAL REVIEW | — | 100% | ✅ | 0.0s |
| **TC010** | Network Hospital — Discount Applied | 🟢 APPROVED | 🟢 APPROVED | ₹3,240 | 100% | ✅ | 3.0s |
| **TC011** | Component Failure — Graceful Degradation | 🟢 APPROVED | 🟢 APPROVED | ₹4,000 | 65% | ✅ | 3.2s |
| **TC012** | Excluded Treatment | 🔴 REJECTED | 🔴 REJECTED | — | 100% | ✅ | 1.3s |

---

## Per-Case Notes

### ✅ TC001 — Wrong Document Uploaded
> **Stopped:** Missing required document(s) for a CONSULTATION claim: HOSPITAL_BILL. You uploaded: 2× PRESCRIPTION. Please provide the missing document(s) and resubmit.
> See [`TC001_wrong_document_uploaded.md`](TC001_wrong_document_uploaded.md)

### ✅ TC002 — Unreadable Document
> **Stopped:** The following document(s) could not be read: PHARMACY_BILL (file: blurry_bill.jpg). Please re-upload a clear, well-lit photo or scan of each.
> See [`TC002_unreadable_document.md`](TC002_unreadable_document.md)

### ✅ TC003 — Documents Belong to Different Patients
> **Stopped:** Documents appear to belong to different patients: PRESCRIPTION (F005): 'rajesh kumar'; HOSPITAL_BILL (F006): 'arjun mehta'. All documents in a single claim must be for the same patient. Please review and resubmit with matching documents.
> See [`TC003_documents_belong_to_different_patients.md`](TC003_documents_belong_to_different_patients.md)

### ✅ TC004 — Clean Consultation — Full Approval
> Claim approved for ₹1350.0. Co-pay (10%) of ₹150.0 deducted.
> See [`TC004_clean_consultation__full_approval.md`](TC004_clean_consultation__full_approval.md)

### ✅ TC005 — Waiting Period — Diabetes
> Claim for 'diabetes' is within the 90-day waiting period. Member joined 2024-09-01; eligible for diabetes claims from 2024-11-30.
> Rejection reasons: `WAITING_PERIOD`
> See [`TC005_waiting_period__diabetes.md`](TC005_waiting_period__diabetes.md)

### ✅ TC006 — Dental Partial Approval — Cosmetic Exclusion
> Claim partially approved for ₹8000.0 of ₹12000.0 claimed. Some line items were excluded — see line-item breakdown for details.
> See [`TC006_dental_partial_approval__cosmetic_exclusion.md`](TC006_dental_partial_approval__cosmetic_exclusion.md)

### ✅ TC007 — MRI Without Pre-Authorization
> Pre-authorisation is required for this procedure (amount ₹15000.0 exceeds the ₹10000 threshold for high-value diagnostic tests). To resubmit: obtain pre-authorisation from your insurer, then re-file the claim with the pre-auth reference number. Pre-auth is valid for 30 days.
> Rejection reasons: `PRE_AUTH_MISSING`
> See [`TC007_mri_without_pre_authorization.md`](TC007_mri_without_pre_authorization.md)

### ✅ TC008 — Per-Claim Limit Exceeded
> Claimed amount ₹7500.0 exceeds the per-claim limit of ₹5000. Claims above this limit cannot be processed.
> Rejection reasons: `PER_CLAIM_EXCEEDED`
> See [`TC008_per_claim_limit_exceeded.md`](TC008_per_claim_limit_exceeded.md)

### ✅ TC009 — Fraud Signal — Multiple Same-Day Claims
> Claim flagged for manual review due to unusual activity patterns.
> See [`TC009_fraud_signal__multiple_same_day_claims.md`](TC009_fraud_signal__multiple_same_day_claims.md)

### ✅ TC010 — Network Hospital — Discount Applied
> Claim approved for ₹3240.0. Network discount (20%) of ₹900.0 applied. Co-pay (10%) of ₹360.0 deducted.
> See [`TC010_network_hospital__discount_applied.md`](TC010_network_hospital__discount_applied.md)

### ✅ TC011 — Component Failure — Graceful Degradation
> Claim approved for ₹4000.0. Note: manual review recommended due to incomplete processing.
> ⚡ Component failures: DataValidatorAgent, DocValidatorAgent
> See [`TC011_component_failure__graceful_degradation.md`](TC011_component_failure__graceful_degradation.md)

### ✅ TC012 — Excluded Treatment
> Claim rejected: 'Obesity and weight loss programs' is excluded under the policy. Reason: The claim is for a bariatric consultation and a customised diet plan, which directly falls under the exclusion for obesity and weight loss programs.
> Rejection reasons: `EXCLUDED_CONDITION`
> See [`TC012_excluded_treatment.md`](TC012_excluded_treatment.md)
