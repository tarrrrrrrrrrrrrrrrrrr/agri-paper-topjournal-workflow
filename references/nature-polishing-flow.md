# Nature-Polishing Flow for Agricultural Manuscripts

Use this module after the first evidence-based draft exists and before final language polishing. It imports the strengths of `nature-polishing` into the agricultural workflow while preserving the stricter agronomy safeguards: no invented data, no invented mechanism, no unsupported statistics and no hidden pseudoreplication.

## Core principle

Language serves argument. Do not polish sentences while the experimental unit, statistical claim, evidence chain or mechanism boundary is still broken.

The workflow order is:

`paper type -> reader path -> hourglass -> section job -> paragraph logic -> claim-evidence-boundary -> sentence control -> final polish`

## 1. Identify the paper type

Decide the paper type before rewriting:

- `Research article`: field or pot experiment testing treatment, cultivar, management or environment effects.
- `Methods/data article`: method, dataset, model or workflow is the main contribution.
- `Hypothesis-based article`: evidence tries to support or rule out a causal process.
- `Application-focused agronomy article`: practical treatment, cultivar or management recommendation is central.

Do not apply one narrative logic to all types. A routine field trial should not be inflated into a mechanism paper, and a mechanistic claim should not be made from correlation alone.

## 2. Build the reader path

For every section, help the reader answer these questions in order:

1. Is this relevant to my crop, system or question?
2. What is new compared with previous agronomy work?
3. Do I trust the design, replication and statistics?
4. Can I reuse the method, treatment insight or management implication?
5. What does the result mean, and where does it stop?

If a section does not answer the next reader question, restructure before polishing.

## 3. Use the hourglass

Use the hourglass pattern for the full manuscript:

- Introduction opens with the broader agronomic or quality problem, then narrows to the specific gap, hypothesis, design and measurable objectives.
- Results stay close to the evidence.
- Discussion widens back out to literature, mechanism, limits and practical implications.

Do not let the Introduction summarize the Results. Do not let the Discussion become a second Results section.

## 4. Diagnose the failure mode

Before rewriting any section, diagnose the failure mode:

- wrong paper type logic;
- missing gap or weak positioning;
- claim without evidence;
- evidence without a claim;
- missing boundary or limitation;
- Results and Discussion mixed together;
- weak title or abstract signal;
- sentence-level clutter only.

Fix the highest-level problem first. Sentence polish is last, not first.

## 5. Repair section jobs

### Title

Signal crop/system, treatment or factor, and central response. Avoid "mechanism", "optimization" and "regulation" unless the evidence directly supports them.

### Abstract

Use a mini-paper pattern:

`context/problem -> gap/objective -> approach -> key quantitative results -> bounded implication`

Every number must appear in saved result tables or figure source data.

### Introduction

Move from problem to gap to objective:

1. Why the agronomic or quality problem matters.
2. What prior work has shown.
3. What remains unresolved.
4. What this experiment tests and why the design can answer it.

### Results

Report what happened, under which treatment/cultivar/season context, and with what quantitative support. Results should not drift into mechanism unless the mechanism was directly tested.

### Discussion

Interpret the results, compare with literature, explain plausible processes cautiously, and state where the interpretation may fail.

### Conclusion

Use a three-part close:

1. central contribution;
2. key evidence;
3. implication with a boundary.

Do not introduce new data or new claims.

## 6. Enforce claim-evidence-boundary

Each important paragraph should have:

- `claim`: one clear scientific or agronomic statement;
- `evidence`: number, model term, uncertainty, figure/table, or verified citation;
- `boundary`: design, sample size, season, cultivar, site, or causality limit.

If any of the three is absent, revise the paragraph before polishing.

## 7. Apply paragraph logic

- One paragraph should have one controlling idea.
- Open with the point, not a vague transition.
- Put numbers close to the claim they support.
- Use transitions that show contrast, cause, limitation or implication.
- Split a paragraph when it mixes result reporting, mechanism and literature comparison.

Avoid repetitive openings such as "This suggests that" when the paragraph needs a stronger subject.

## 8. Apply sentence control

Use sentence control after the argument is sound:

- Aim for 10-30 words per sentence in polished English.
- Check sentences longer than 20 words for multiple propositions.
- Prefer one subject-verb proposition per sentence.
- Replace vague phrases such as "data were analyzed statistically" with the actual model and comparison method.
- Avoid em dashes by default. Prefer full stops, commas or parentheses.
- Keep technical terms stable across the manuscript.

## 9. Chinese-to-English reconstruction

When the draft is Chinese or Chinese-influenced English:

1. Extract the core propositions first.
2. Rebuild the logic instead of translating clause by clause.
3. Preserve treatment names, variables, units and statistical claims.
4. Add hedging where causal evidence is limited.
5. Polish only after the reconstructed paragraph is scientifically correct.

## 10. Final writing QA

Before declaring a section polished:

- The section's job is clear.
- Every main claim has evidence.
- Every causal or mechanism claim has a boundary.
- Results and Discussion sentence types are separated.
- No unsupported novelty, optimization or mechanism language remains.
- No AI-generated reference, data or method detail has been inserted.

Default output for a polishing pass:

1. Polished text.
2. `Revision notes:` with 3-5 bullets on structural and stylistic changes.
3. `Remaining risks:` for missing data, missing citations, overclaiming or journal-format issues.
