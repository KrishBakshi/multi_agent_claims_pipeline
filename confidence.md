# Confidence Calculation

In this codebase, `confidence` is not a model probability. It is a deterministic pipeline-health score.

The core rule is in [src/pipeline/graph.py](src/pipeline/graph.py:174): every claim starts at `1.0`. Each agent either leaves it unchanged or subtracts a fixed penalty when something goes wrong. The final `DecisionOutput.confidence_score` is just the rounded final value from state at [src/pipeline/graph.py](src/pipeline/graph.py:209) and [src/pipeline/graph.py](src/pipeline/graph.py:235).

The penalties come from a few places:

- `DataValidatorAgent`: `-0.20` for a simulated/component-style failure, or if it halts on bad structured input at [src/agents/data_validator.py](src/agents/data_validator.py:30) and [src/agents/data_validator.py](src/agents/data_validator.py:76)
- `DocParserAgent`: `-0.15` for an unreadable document and `-0.10` for a parse/extraction failure or missing file data at [src/agents/doc_parser.py](src/agents/doc_parser.py:32), [src/agents/doc_parser.py](src/agents/doc_parser.py:236), [src/agents/doc_parser.py](src/agents/doc_parser.py:281), and [src/agents/doc_parser.py](src/agents/doc_parser.py:309)
- `DocValidatorAgent`: `-0.15` when it hits a simulated/component-style failure or halts on document validation issues at [src/agents/doc_validator.py](src/agents/doc_validator.py:18) and [src/agents/doc_validator.py](src/agents/doc_validator.py:60)
- Safe wrapper around any unhandled node exception: `-0.20` at [src/pipeline/graph.py](src/pipeline/graph.py:52)

`DecisionMakerAgent` does not compute a new confidence from approval/rejection logic. It just reads the accumulated value and returns it unchanged at [src/agents/decision_maker.py](src/agents/decision_maker.py:158). So a claim can be:

- `REJECTED` with `confidence = 1.0` if the rejection is clean and deterministic
- `APPROVED` with `confidence < 1.0` if earlier parsing/validation degraded the pipeline

A simple example:

- Start: `1.0`
- One unreadable doc in parser: `1.0 - 0.15 = 0.85`
- Later a doc-validator simulated failure: `0.85 - 0.15 = 0.70`
- Final output confidence: `0.70`

One important distinction: the OCR layer also stores per-document extraction confidence, like `0.95` or `0.60`, in extracted docs at [src/agents/doc_parser.py](src/agents/doc_parser.py:66) and [src/agents/doc_parser.py](src/agents/doc_parser.py:204). That document-level score is for traceability; it does not currently feed into the overall claim confidence.
