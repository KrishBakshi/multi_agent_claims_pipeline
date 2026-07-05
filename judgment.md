# LLM Judgment Cases

There are exactly two places where this code uses an LLM to make a semantic judgment, both in [src/agents/decision_maker.py](src/agents/decision_maker.py:15). Everything else in the decision flow is deterministic Python.

## 1. Exclusion judgment

This happens at [src/agents/decision_maker.py](src/agents/decision_maker.py:229). The model is wrapped with a structured schema `ExclusionCheckResult` at [src/agents/decision_maker.py](src/agents/decision_maker.py:44), so it must return:

```json
{
  "is_excluded": true,
  "matched_exclusion": "Obesity and weight loss programs",
  "reasoning": "..."
}
```

A real example comes from `TC012` in [tests/test_cases.json](tests/test_cases.json:531), with policy exclusions from [config/policy_terms.json](config/policy_terms.json:105).

### Raw Prompt Structure

```text
System prompt:
You check whether a medical claim is excluded under a health insurance policy.
Answer only based on the exclusion list provided.
Do NOT apply exclusions that contradict an explicitly covered claim category.

Variables:
- category_note
- diagnosis
- treatment
- exclusion_list

Human prompt template:
{category_note}
Diagnosis: {diagnosis}
Treatment: {treatment}
Policy exclusions: {exclusion_list}

Is this claim excluded? If yes, which exclusion matches?
```

### Example With Variables Replaced

The effective LLM input looks like:

```text
System:
You check whether a medical claim is excluded under a health insurance policy.
Answer only based on the exclusion list provided.
Do NOT apply exclusions that contradict an explicitly covered claim category.

Human:
Claim category: CONSULTATION
Diagnosis: Morbid Obesity — BMI 37
Treatment: Bariatric Consultation and Customised Diet Plan
Policy exclusions: [
  "Self-inflicted injuries",
  "War or nuclear hazard",
  "Substance abuse treatment",
  "Experimental treatments",
  "Infertility and assisted reproduction",
  "Obesity and weight loss programs",
  "Bariatric surgery",
  "Cosmetic or aesthetic procedures",
  "Vaccination (non-medically necessary)",
  "Health supplements and tonics",
  "Teeth whitening",
  "Orthodontic treatment",
  "Cosmetic dental procedures",
  "LASIK",
  "Refractive surgery"
]

Is this claim excluded? If yes, which exclusion matches?
```

### What the LLM does

- It is not calculating money or limits.
- It is doing semantic matching between the diagnosis/treatment text and the exclusion phrases.
- In this example, it should infer that “Morbid Obesity” plus “Bariatric Consultation and Customised Diet Plan” maps to the exclusion `Obesity and weight loss programs`, possibly also related to `Bariatric surgery`, but it is expected to choose the best matching explicit exclusion.

### How the code uses the result

- If `is_excluded == true`, the pipeline immediately rejects the claim with `EXCLUDED_CONDITION` at [src/agents/decision_maker.py](src/agents/decision_maker.py:269).
- If `false`, the pipeline continues to the next rule.

## 2. Waiting-period condition judgment

This happens at [src/agents/decision_maker.py](src/agents/decision_maker.py:321). The model is wrapped with `WaitingPeriodMatch` at [src/agents/decision_maker.py](src/agents/decision_maker.py:50), so it must return:

```json
{
  "matched_condition": "diabetes",
  "reasoning": "..."
}
```

A real example is `TC005` in [tests/test_cases.json](tests/test_cases.json:166), using waiting-period keys from [config/policy_terms.json](config/policy_terms.json:90).

### Raw Prompt Structure

```text
System prompt:
Map the given medical diagnosis to one of the condition keys in the waiting-period list, or null if it doesn't match any.

Variables:
- diagnosis
- treatment
- condition_keys

Human prompt template:
Diagnosis: {diagnosis}
Treatment: {treatment}
Condition keys: {condition_keys}
```

### Example With Variables Replaced

The effective LLM input looks like:

```text
System:
Map the given medical diagnosis to one of the condition keys in the waiting-period list, or null if it doesn't match any.

Human:
Diagnosis: Type 2 Diabetes Mellitus
Treatment: None
Condition keys: [
  "diabetes",
  "hypertension",
  "thyroid_disorders",
  "joint_replacement",
  "maternity",
  "mental_health",
  "obesity_treatment",
  "hernia",
  "cataract"
]
```

### What the LLM does

- It is not deciding approval directly.
- It is normalizing free-text diagnosis into one policy key.
- In this example, it should map `Type 2 Diabetes Mellitus` to `diabetes`.

### How the code uses the result

- The code then looks up the required waiting period for that key, here `diabetes: 90` days from [config/policy_terms.json](config/policy_terms.json:93).
- It compares that value against actual date arithmetic done in Python: `days_since_join = treatment_date - join_date`.
- For `TC005`, join date is `2024-09-01` and treatment date is `2024-10-15`, so only 44 days have passed.
- Since 44 < 90, the code rejects with `WAITING_PERIOD` and computes the eligibility date deterministically at [src/agents/decision_maker.py](src/agents/decision_maker.py:341).

## Summary

So the clean mental model is:

- LLM call 1: “Does this diagnosis/treatment semantically match an exclusion?”
- LLM call 2: “Which waiting-period condition key does this diagnosis semantically map to?”

After that, the actual business decision is made by normal code:

- reject if excluded,
- reject if mapped condition is still within its waiting window,
- otherwise continue through deterministic checks and amount calculation.
