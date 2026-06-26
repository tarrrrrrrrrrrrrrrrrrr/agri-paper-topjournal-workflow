# Publication Figure Rules

Use Python with matplotlib/seaborn and follow the `nature-figure` skill. Define the conclusion, evidence logic, export needs and reviewer risks before plotting.

## Style contract

- Times New Roman for all figure text where available.
- Use the supplied palette-reference image. Extract its colors once and reuse exact hexadecimal values. If colors are insufficient, extend within the same hue/lightness family and document the additions.
- Use black edges on scatter points, bars, boxplots and filled marks when it improves separation.
- Keep a coherent multi-hue palette; avoid a one-color figure set.
- Use real error bars from replicate-level data or model-estimated uncertainty.
- Add model-supported `a/b/c` compact-letter display labels in empty space above error bars.
- Horizontal tick labels are preferred when they fit. Wrap or abbreviate before rotating.

## Geometry and typography

- Choose standard single-column, 1.5-column or double-column dimensions before plotting.
- Keep panel labels bold and consistently positioned.
- Use stable axes, margins and panel ratios. Do not leave a large empty center between panels.
- Keep legends outside data-dense areas. Never cover bars, points or confidence intervals.
- Avoid nested decorative cards, excessive titles and explanatory text inside figures.
- Avoid repeating the same chart grammar across consecutive main figures. Prefer a mixed agronomy sequence such as raw plot-unit distribution with mean/CI, dose-response heatmap, effect-size forest plot, and response-fingerprint heatmap instead of four line-grid figures.
- When two panels are intended to be comparable, set equal grid width/height ratios and place colorbars in inset or dedicated axes so the colorbar does not shrink only one panel.
- Add small axis padding for response surfaces and dose grids when observed points lie on plot boundaries; exact `xlim`/`ylim` values often clip marker edges.
- Reserve whitespace for legends and colorbars. Do not let colorbars overlap neighboring panels or titles, and do not let legends cover confidence intervals.
- Move explanatory micro-notes such as "95% CIs shown" or "supported treatments = 0" to the caption/report unless they are essential for decoding a symbol inside the figure.
- In trade-off scatter plots, keep true x/y coordinates. Do not jitter scientifically meaningful coordinates to reduce overlap; fade non-decision points and label only decision-relevant treatments.

## Chart-specific checks

- Box/violin plots: use wider boxes when readable, show median/IQR clearly, and outline distributions.
- Bars: black edge, mean ± SE/CI, compact letters, and no redundant numerical labels unless requested.
- Heatmaps: cell borders and overlays must match the exact cell grid; top and side labels must have equal spacing.
- Networks/path diagrams: coefficients belong on their corresponding edge. Use a short accurate leader only when the label cannot sit on the edge. Never leave disconnected leaders.
- Response surfaces/3D: show all observed points with black outlines, keep points inside axes limits, and use different markers only for real grouping variables.
- Correlation panels: disclose pooled treatment structure and avoid causal titles.
- Forest/effect plots: place legends outside the confidence-interval area, usually above or below the panel with extra margin. Keep the zero line prominent and confidence intervals visually lighter than focal markers.
- Raw distribution panels: when replacing repetitive line plots, show raw plot units with jitter only along the categorical/dose axis, overlay mean and real 95% CI, and keep treatment coordinates interpretable.

## Export contract

For every figure:

1. Save each panel separately.
2. Save the combined figure.
3. Export vector PDF and 600 dpi PNG; add SVG when editors need editable vectors.
4. Preserve transparent backgrounds only when intended.
5. Record figure size, DPI, font, palette, error-bar source, significance method and source table in `figure_metadata.csv`.

## QA gate

Check file readability, blank canvases, DPI, dimensions, clipping, missing glyphs, overlapping labels, inconsistent palettes, unsupported significance labels, missing panels, duplicated filenames and manuscript-caption consistency. Inspect rendered output visually before replacing an existing figure.

## Reusable significance-bar implementation

Use [`scripts/plot_significance_bars.py`](../scripts/plot_significance_bars.py) for single-factor or combined main-effect bar panels. Input must be a validated model-summary CSV containing:

- `label`: x-axis category;
- `mean`: estimated or model-adjusted mean;
- `error`: real SE or symmetric confidence-interval half-width;
- `letter`: model-supported compact-letter display;
- optional `block`, `order`, and hexadecimal `color`.

The script deliberately does not calculate significance. Generate uncertainty and letters using the design-correct model, save them to CSV, then plot:

```powershell
python scripts/plot_significance_bars.py `
  --input examples/significance_bar_example.csv `
  --output-base output/figure_main_effects `
  --ylabel "Mean response" `
  --panel-label b
```

Defaults: Times New Roman, black bar borders, black capped error bars, bold letters above the uncertainty interval, shared y geometry, subtle separators between effect blocks, vector PDF and 600 dpi PNG. Numerical values are hidden unless `--show-values` is explicitly requested.

## Additional visual review

Also inspect for failure modes that automated checks often miss: boundary markers clipped by axes, colorbars touching panels, legends on error bars, panel labels detached from their panels, repeated chart grammar across main figures, small explanatory text that belongs in the caption, and stale old figure versions left in the delivery folder.

When the user asks to replace older figures, clear the delivery folder only after resolving and checking the exact target path; then copy only the intended image/result files and verify old base names are absent.
