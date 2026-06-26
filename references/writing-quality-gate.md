# Writing Quality Gate

Use this module whenever drafting, translating, polishing or humanizing manuscript text. It adapts the strongest parts of the SciPilot writing workflow to agricultural manuscripts while keeping the stricter agronomy rules: do not alter data, treatment direction, significance, citations, methods or conclusions unless the audited evidence requires it.

## Stage 0: writing task intake

Before changing text, identify the minimum information needed for the task. If missing information would change the output, ask; otherwise state the assumption and proceed.

Required fields:

- `task type`: draft, polish, translate, condense, expand, humanize, logic check, caption, cover letter or reviewer response.
- `medium`: LaTeX, Word/DOCX, Markdown or plain text.
- `target journal`: target journal, journal family or generic academic style.
- `language direction`: zh-to-en, en-to-zh, en-to-en or zh-to-zh.
- `discipline`: crop/agronomy/plant physiology/omics/soil/engineering or another field.
- `revision conservativeness`: proofreading only, moderate polish or deep rewrite.
- `processing scope`: title, abstract, introduction, methods, results, discussion, conclusion, caption, cover letter, response letter or selected paragraph.

For full manuscript drafting after data analysis, combine this intake with the analysis specification and manuscript draft template.

## Medium-specific rules

### LaTeX

- Preserve `\cite{}`, `\ref{}`, `\label{}`, equations and custom commands.
- Escape prose `%`, `&` and `#` as `\%`, `\&` and `\#` unless already escaped or inside math.
- Do not introduce Markdown markers such as `**bold**`.
- Run `writing_lint.py --mode latex --lang en` before delivery.

### Word/DOCX

- Output clean prose, not Markdown.
- Avoid `#`, `**bold**`, bullet clutter and code-style formatting unless explicitly requested.
- For Chinese Word text, prefer full-width Chinese punctuation.
- Run `writing_lint.py --mode word --lang zh` or `--lang en` as appropriate.

### Markdown or plain text

- Keep Markdown only when the final medium is Markdown.
- If the Markdown will later be pasted into Word, treat it as Word/plain text and remove markup.

## Three-part delivery

For polishing, translation and rewriting tasks, deliver three parts unless the user asks for a different format:

1. `Revised text`: the edited text only.
2. `back-translation/check`: a literal Chinese check for English output, or a concise meaning check for Chinese output, so the author can verify that facts did not drift.
3. `Change log`: what changed and why, including preserved numbers, treatment names, significance claims and any author-confirmation items.

For first-draft generation, apply the same idea at section level: draft text, evidence check, change/assumption log.

## Machine lint gate

Before calling writing polished or ready, run:

```powershell
python scripts/writing_lint.py "C:\path\to\text.tex" --mode latex --lang en --report "C:\path\to\lint_report.json"
python scripts/writing_lint.py "C:\path\to\text.txt" --mode word --lang zh --report "C:\path\to\lint_report.json"
```

Exit-code meaning:

- `0`: PASS. No FAIL/WARN items.
- `1`: WARN. Review warnings and either revise or report why they are acceptable.
- `2`: FAIL. Fix before delivery or report the blocker plainly.

The linter checks deterministic issues: AI-tell words, formulaic phrases, mechanical connectives, comma-ing endings, LaTeX escaping, Markdown residue in Word/plain text, Chinese half-width punctuation, sentence-length rhythm and passive ratio. It is a gate, not a substitute for scientific judgment.

## AI read-back review

After the machine gate, reread the revised text as a reviewer:

- Does the paragraph have a claim, evidence and boundary?
- Did any number, unit, treatment name, direction or conclusion change?
- Is hedging/boosting matched to the evidence strength?
- Did Results drift into Discussion, or Discussion become a second Results section?
- Does the prose still sound like the author's field rather than generic AI text?

If a problem appears, revise, rerun `writing_lint.py`, and update the change log. Do not pretend a section passed if WARN/FAIL items remain.

## Section playbook integration

- Introduction: use CARS. Establish territory, establish the exact agronomic gap, then occupy the gap with objectives or hypotheses.
- Abstract: include the research problem, design, key quantitative result, direction of response and bounded implication.
- Results: direction, magnitude, uncertainty/statistics and figure/table pointer.
- Discussion: use an inverted funnel. Start from the result, compare literature, explain plausible processes cautiously, then state limitations and implications.
- Conclusion: central contribution, key evidence and boundary. No new numbers or citations.

## Red flags

- A polished sentence changes a number, direction, significance or treatment name.
- A generic phrase hides missing evidence.
- A mechanism verb appears without direct validation.
- LaTeX contains raw `%`, `&` or `#`.
- Word output contains Markdown.
- The change log does not explain substantive restructuring.
