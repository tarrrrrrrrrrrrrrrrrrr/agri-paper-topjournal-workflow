# Agricultural Paper Top-Journal Workflow

A reusable Codex skill for agricultural experimental papers, covering:

- project, spreadsheet, figure and manuscript audits;
- design-aware statistical analysis and mixed-model guidance;
- Python publication figures with traceable uncertainty and significance;
- academic writing, DOCX assembly and reference checks;
- clean journal submission packages and final QA.

The workflow uses `lwxg` as its default worked example, while discovering factors, variables, replicates and conclusions independently for every new project.

## Install

Copy this repository into your personal Codex skills directory:

```text
~/.codex/skills/agri-paper-topjournal-workflow/
```

The required entry point is [SKILL.md](SKILL.md). Deterministic audit tools are under [`scripts/`](scripts/), and detailed rules are under [`references/`](references/).

## Significance bar charts

The repository includes a reusable publication-style bar-chart implementation:

```powershell
python scripts/plot_significance_bars.py `
  --input examples/significance_bar_example.csv `
  --output-base output/figure_main_effects `
  --ylabel "Mean response"
```

It exports PDF and 600 dpi PNG with Times New Roman, black outlines, real error
bars and model-supplied `a/b/c` compact-letter labels.
