# Mixed-Model Python Templates

Use this module when planning or implementing Python statistical analysis. These templates are starting points; adapt them to the audited experimental design and document every assumption.

## Required inputs

Before fitting any model, confirm:

- One row per inferential experimental unit unless a hierarchical model is planned.
- Explicit columns for season/year, cultivar/genotype, treatment and block/replicate where applicable.
- No treatment means substituted for raw plot-level observations.
- Missing combinations are documented.
- The analysis specification has fixed effects, random effects and comparison families.

## Factorial randomized complete block design

```python
import statsmodels.formula.api as smf

model = smf.mixedlm(
    "response ~ cultivar * treatment",
    data=df,
    groups=df["block"],
)
fit = model.fit(reml=True)
print(fit.summary())
```

Use this only when block is the main random grouping factor and each treatment combination is represented within blocks.

## Multi-season factorial design

```python
model = smf.mixedlm(
    "response ~ season * cultivar * treatment",
    data=df,
    groups=df["block"],
)
fit = model.fit(reml=True)
```

Treat season as fixed when inference is limited to the observed seasons. Treating season as random requires a defensible population-of-seasons argument and enough levels.

## Repeated measurements

For repeated measurements, keep plot identity in the data. If using `statsmodels`, consider GEE or a mixed model with plot-level grouping depending on the design. Do not fit independent ANOVA at each time point without multiplicity control and a clear reason.

## Estimated means and letters

Python does not have one universally accepted equivalent of R `emmeans` plus compact-letter displays. If exact CLD output is required:

- Save the fitted-model summary and contrast table.
- Use R via a documented script when `emmeans` is necessary, or implement pairwise contrasts transparently in Python.
- Never copy letters from an old figure or spreadsheet.

## Diagnostics to save

- Model formula and software versions.
- Convergence status and warnings.
- Residual plot or residual summary.
- Estimated marginal means or model-adjusted means.
- Pairwise contrasts with adjusted P values.
- Effect sizes and uncertainty.

## When Python is not enough

Use R for inference if the design needs Kenward-Roger/Satterthwaite degrees of freedom, `emmeans`, split-plot error strata, or mature CLD tooling that would be fragile to reimplement in Python. The manuscript may still use Python for data audit and figures.
