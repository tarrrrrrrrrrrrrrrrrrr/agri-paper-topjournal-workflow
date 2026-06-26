# agri-paper-topjournal-workflow

Codex skill for agricultural manuscript analysis and writing workflows.

It focuses on crop, agronomy and field-trial papers where raw data integrity,
replicate structure, statistical defensibility, figure traceability, manuscript
consistency and submission readiness matter.

## What It Covers

- project inventory and source-file audit;
- replicate-level data/design audit;
- model-aware statistical planning;
- manuscript-ready figure workflow;
- old-vs-new analysis comparison;
- evidence-based manuscript first draft;
- Nature-style argument polishing;
- writing quality lint gate;
- citation, data availability and submission QA.

## Quick Verification

Run the bundled regression checks:

```powershell
python -B scripts/test_agri_skill.py
```

Run the writing lint gate on the examples:

```powershell
python scripts/writing_lint.py examples/writing_lint_bad.tex --mode latex --lang en
python scripts/writing_lint.py examples/writing_lint_good.tex --mode latex --lang en
```

## Notes

This repository contains the reusable skill workflow, references, examples and
helper scripts. It does not include user project data, manuscripts or private
analysis outputs.
