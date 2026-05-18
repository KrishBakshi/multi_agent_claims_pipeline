# Missing Test Case Artefacts

This directory is the intended output location for the missing artefacts implied by `tests/test_cases.json`.

Source files:
- `data/test_case_missing_artifacts_manifest.json`
- `data/test_case_prompt_templates.md`

Generation flow:
- Read one artefact entry from the manifest.
- Use the referenced prompt template.
- Fill in the seed fields and special constraints.
- Save the generated file at the artefact `target_path`.
