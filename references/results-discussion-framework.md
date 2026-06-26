# Results and Discussion Framework

Use this module when turning statistical outputs and figures into manuscript text.

## Results paragraph pattern

For each result paragraph, use this sequence:

1. Claim: the biological or agronomic change.
2. Evidence: model term, adjusted comparison, estimate, uncertainty and exact `n` where relevant.
3. Figure/table pointer.
4. Interaction or exception, if present.

Example pattern:

```text
[Treatment] changed [response] in [season/cultivar/context]. The model showed [main effect/interaction] with [estimate or percent change] and [SE/CI/P value or letters], based on [n] plot-level units (Fig. X; Table Sx).
```

Do not write a paragraph that only says "there was a significant difference" without stating direction and magnitude.

## Recommended agronomy story order

1. Establish treatment implementation and environmental/canopy context if measured.
2. Report yield, biomass or primary growth response.
3. Report quality, aroma, nutrient or grain/fruit traits.
4. Connect physiological evidence such as photosynthesis, SPAD, RUE or IPAR.
5. Present multivariate synthesis as a summary, not as proof of mechanism.

## Discussion paragraph pattern

For each Discussion paragraph:

1. Name the result being interpreted.
2. Explain a plausible process.
3. Compare with accepted literature using verified citations.
4. State the boundary of inference.
5. Transition to the next evidence block.

Use "consistent with", "associated with", "may reflect" and "suggests possible involvement" for observational associations. Use stronger causal wording only for directly manipulated factors with appropriate validation.

## Handling non-significant or mixed results

Non-significant results still matter when they constrain interpretation. Report them when they affect the main story, for example when yield is unchanged but quality improves, or when a cultivar x treatment interaction means the average effect is misleading.

Avoid burying inconvenient results in the supplement if they contradict the main conclusion.

## Interaction writing

When an interaction is present, do not overemphasize main effects. State which factor levels differ, where the effect is absent or reversed, and whether the manuscript conclusion depends on a specific cultivar, season or treatment level.

## Exploratory analysis wording

For PCA, correlation, networks, response surfaces and machine-learning models:

- Report them after primary model-based inference.
- Label them as exploratory or descriptive unless independently validated.
- Avoid causal titles and arrow language.
- State sample size and pooling structure.

## Red flags

- Results paragraph has no number.
- Discussion paragraph has no result anchor.
- Figure has significance letters but no saved comparison family.
- PCA or correlation is written as mechanism.
- Conclusion says "optimal" without validation.
- Abstract includes a number that is absent from result tables.
