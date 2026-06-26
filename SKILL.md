---
name: agri-paper-topjournal-workflow
description: >-
  Use when the user is working on agricultural, crop, agronomy, field-trial,
  pot-experiment, rice, wheat, maize, yield, quality, aroma, canopy, fertilizer,
  irrigation, shading, cultivar, genotype, Excel, replicate, ANOVA, mixed-model,
  significance-letter, manuscript-draft, manuscript-figure, DOCX, supplement,
  citation, data-availability, or journal-submission tasks, especially when raw
  data, statistical defensibility, publication figures, manuscript consistency,
  or submission readiness matters.
---

# Agricultural Paper Top-Journal Workflow

Use this skill for agricultural experimental papers from raw files through submission. It is designed to prevent the common failure modes in agronomy manuscripts: pseudoreplication, copied significance letters, incomplete variable coverage, stale manuscript values, unsupported citations, figure residue, and submission folders that contain old versions.

The local `lwxg` project is only an example/template map. If the user does not provide a project path, ask for the active project directory before changing or analyzing files. Never treat `lwxg` as the implied active project.

## Coordinate the available skills

- Use `spreadsheets` for workbook inspection, structured spreadsheet edits, formulas, tables and charts.
- Use `nature-figure` for every scientific figure creation, revision or QA task. Default to Python unless the user explicitly chooses R.
- Use `documents` for DOCX editing and render/inspect QA.
- Use `nature-polishing` for publication English.
- Use `humanizer-zh-academic` for Chinese academic de-template revision.
- Use `nature-citation` for citation addition and claim-reference verification.
- Use `nature-data` for data-availability and repository planning.
- Use `systematic-debugging` when an audit, model, plot or document step fails.
- Use `verification-before-completion` before claiming readiness.

Read only the reference module needed for the current stage:

- Statistical design and model rules: [statistics.md](references/statistics.md)
- Analysis specification template: [analysis-spec-template.md](references/analysis-spec-template.md)
- Python mixed-model starting points: [mixed-model-python-templates.md](references/mixed-model-python-templates.md)
- Figure rules: [figures.md](references/figures.md)
- Writing and DOCX rules: [writing-docx.md](references/writing-docx.md)
- Writing quality gate: [writing-quality-gate.md](references/writing-quality-gate.md)
- Manuscript first-draft template: [manuscript-draft-template.md](references/manuscript-draft-template.md)
- Results and Discussion framework: [results-discussion-framework.md](references/results-discussion-framework.md)
- Nature-style argument and polishing flow: [nature-polishing-flow.md](references/nature-polishing-flow.md)
- Citation workflow: [citation-workflow.md](references/citation-workflow.md)
- Journal structure variants: [journal-variants.md](references/journal-variants.md)
- Submission QA: [submission-qa.md](references/submission-qa.md)
- `lwxg` template map: [lwxg-template.md](references/lwxg-template.md)

## Non-negotiable defaults

1. Use Python unless the user explicitly selects another backend.
2. Inspect source files before proposing or making changes.
3. Preserve sources. Write to a clean versioned output directory unless replacement is explicitly requested.
4. Infer statistics from replicate-level experimental units, never from treatment means alone.
5. Do not invent error bars, significance, methods, references, weather, sequences, dates or data.
6. Do not claim causality, optimization or mechanism beyond the experimental design and validation.
7. Keep confirmatory inference separate from exploratory analyses.
8. Verify outputs after every substantial stage.

## Stage 1: Inventory the project

If no path is supplied, ask the user for the project directory. Use the local `lwxg` template only as an example if the user explicitly asks to inspect it.

Run the project audit before reanalysis:

```powershell
python scripts/audit_project.py --project "C:\path\to\project" --output "C:\path\to\audit"
```

Identify the authoritative manuscript, raw dataset, current analysis code, figure set, palette reference and target-journal files. Report duplicate versions, stale journal names, backups and missing sources. Do not delete anything during an audit.

## Stage 2: Audit data and design

Extract factors, levels, seasons/years, cultivars/genotypes, blocks, experimental units, sampling hierarchy and timing from both manuscript and data.

```powershell
python scripts/audit_data.py --input "C:\path\to\data.xlsx" --output "C:\path\to\audit"
```

Confirm every sheet, variable, row, replicate and treatment combination was read. For a design with three field replicates, each inferential combination should normally have three plot-level units. Subsamples are not independent plots unless a hierarchical model explicitly represents the sampling structure.

Stop and report a blocker when the experimental unit cannot be determined, raw replicates are absent, or manuscript and data disagree materially.

## Stage 3: Design the statistical analysis

Read [statistics.md](references/statistics.md) and fill [analysis-spec-template.md](references/analysis-spec-template.md) before fitting models. Read [mixed-model-python-templates.md](references/mixed-model-python-templates.md) when implementing Python models or deciding that R is safer for degrees-of-freedom and compact-letter-display workflows.

The analysis specification must state:

- primary responses and hypotheses;
- fixed and random effects;
- experimental unit and exact `n`;
- interaction hierarchy;
- multiplicity method;
- estimated means, contrasts, effect sizes and uncertainty;
- exploratory analyses and their limitations;
- variables excluded from analysis and why.

Use a design-correct mixed model for blocked, split-plot, multi-season or repeated-measure experiments. Use compact-letter displays only from the corresponding fitted model and comparison family.

Save analysis-ready data and every result table as CSV. Save a formatted XLSX only when the manuscript needs a styled table.

## Stage 4: Produce figures

Read [figures.md](references/figures.md) and invoke `nature-figure`.

Before plotting, state the figure's conclusion, evidence logic, source table, error-bar source, significance method, export dimensions and reviewer risk.

Historical defaults to preserve unless the user overrides them:

- Times New Roman;
- user-provided palette image, with documented same-family extensions only when necessary;
- black-edged points, bars, boxes and filled marks;
- real uncertainty bars;
- model-supported `a/b/c` labels in clear whitespace;
- separate panels plus combined figures;
- vector PDF and 600 dpi PNG, with SVG where useful.

Audit figures after export:

```powershell
python scripts/audit_figures.py --directory "C:\path\to\figures" --output "C:\path\to\audit"
```

Visually inspect every figure. Automated checks cannot prove that labels, legends, leaders or panel spacing are correct.

For journal-style bar charts with real uncertainty and `a/b/c` labels, use the bundled [`plot_significance_bars.py`](scripts/plot_significance_bars.py). Pass a validated model-summary CSV; never let plotting code invent significance.

## Stage 5: Compare old and new analyses

Create a comparison table with original method, new method, assumptions, changed values/significance, conclusion impact, advantage, limitation and manuscript action. When a previous plot used incomplete data, identify exactly which variables/rows were omitted and whether the corrected result changes the scientific conclusion.

Do not preserve an old result merely to match the paper. Preserve the original method only when the user explicitly requires it and it remains scientifically defensible.

## Stage 6: Write and assemble the manuscript

Read [writing-docx.md](references/writing-docx.md), [writing-quality-gate.md](references/writing-quality-gate.md), [manuscript-draft-template.md](references/manuscript-draft-template.md), [results-discussion-framework.md](references/results-discussion-framework.md), [nature-polishing-flow.md](references/nature-polishing-flow.md) and [citation-workflow.md](references/citation-workflow.md) as needed. Keep the main story efficient: yield-quality trade-off, canopy/light-use evidence, quality-related metabolism, multivariate synthesis and bounded model interpretation.

For every writing, translation, polishing or humanizing task, confirm or infer with explicit assumptions: task type, medium, target journal, language direction, discipline, revision conservativeness and processing scope. Do not silently change facts to make prose smoother.

Write in two passes:

1. Evidence draft: build Methods, Results, captions and Discussion from audited data, model outputs and figures.
2. Nature-style argument polish: diagnose paper type, reader path, hourglass structure, section job, paragraph logic, claim-evidence-boundary and sentence control before sentence-level polishing.
3. Writing quality gate: deliver revised text, back-translation/check and change log; then run `scripts/writing_lint.py` with the correct `--mode` and `--lang`.

Remove internal revision language, filenames, worksheet names, local paths and journal-quartile commentary. Use conservative mechanism language. Keep all values synchronized across abstract, Results, Discussion, Conclusions, tables and captions.

For DOCX work, edit a copy, maintain one authoritative submission version and run the document render gate when available.

Before polishing language, audit numeric consistency between result tables and manuscript text:

```powershell
python scripts/audit_numeric_consistency.py --results "C:\path\to\results.csv" --manuscripts "C:\path\to\manuscript.docx" --output "C:\path\to\audit"
```

Before delivering polished writing, run the medium-specific writing lint gate:

```powershell
python scripts/writing_lint.py "C:\path\to\text.tex" --mode latex --lang en --report "C:\path\to\lint_report.json"
python scripts/writing_lint.py "C:\path\to\text.txt" --mode word --lang zh --report "C:\path\to\lint_report.json"
```

Audit the manuscript:

```powershell
python scripts/audit_manuscript.py --input "C:\path\to\manuscript.docx" --figures "C:\path\to\figures" --output "C:\path\to\audit"
```

AI declarations are author-controlled. Never insert, remove or rewrite one without explicit instruction.

## Stage 7: Prepare the submission package

Read [journal-variants.md](references/journal-variants.md) and [submission-qa.md](references/submission-qa.md). Browse the target journal's current official Guide for Authors before finalization.

Build a clean folder containing only intended upload files. Verify manuscript, highlights, graphical abstract, separate figures, supplementary material, declarations, cover letter, data/code and README as applicable. Generate a manifest, QA report and upload checklist. Validate ZIP entries after compression.

Keep journal-scope risk separate from file completeness. Never promise acceptance or a CAS quartile outcome.

## Output contract

Prefer this structure:

```text
<project>_topjournal_output/
|-- analysis_ready_data.csv
|-- results/
|-- figures/
|   |-- panels/
|   `-- combined/
|-- tables/
|-- manuscript/
|-- supplementary/
|-- submission_package/
`-- reports/
```

Reports should include project inventory, data/design audit, statistical audit, figure QA, writing lint report, manuscript QA, numeric consistency QA and submission QA.

## Completion gate

Before calling the work complete, verify:

- source files are unchanged unless replacement was requested;
- replicate structure and model terms are documented;
- all requested variables were analyzed or explicitly excluded with reasons;
- error bars and significance labels are traceable to saved result tables;
- figure files open and match manuscript references;
- manuscript contains no internal residue, corrupted symbols or unsupported numeric claims;
- polished text has a change log and writing-lint result, with remaining WARN/FAIL items reported plainly;
- citations support the exact claims they are attached to;
- submission package contains one authoritative manuscript and no backup files;
- unresolved scientific, scope or visual-render risks are stated plainly.
