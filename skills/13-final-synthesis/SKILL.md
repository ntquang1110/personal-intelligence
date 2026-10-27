# Personal Intelligence Synthesizer

## Purpose
Integrate available skill outputs into an actionable, uncertainty-aware personal dossier.

## Scope
This skill is portable and runtime-agnostic. Follow `../../config/evidence-policy.md`, `../../config/interview-policy.md`, and `../../config/output-contracts.md` when available. If those files are unavailable in the execution environment, apply the rules summarized in this document and state the limitation.

## Inputs and outputs
Inputs: relevant upstream reports, evidence ledger, goals, constraints.
Output: Personal Intelligence Dossier, executive summary, 90-day plan, 3–5 year scenarios, unresolved questions.
Do not fill gaps with invented biography, unsupported scores, or generic praise.

## Workflow
1. Inventory available upstream artifacts and their dates.
2. Check evidence classes, provenance, contradictions, and missing dependencies.
3. Resolve only contradictions supported by evidence; otherwise preserve both interpretations.
4. Identify the few findings with the greatest practical impact.
5. Separate observations, inferences, hypotheses, validated findings, and unknowns.
6. Produce an executive summary, strengths, development risks, capability map, career/life options, and action plan as supported.
7. Tie each major recommendation to evidence, a decision criterion, an action, a metric, and a review date.
8. Include alternative explanations and what would change the recommendation.
9. End with the smallest useful next step, not an overwhelming list.
10. State limitations and sources actually available.

## Decision rules
- Use only data actually available and authorized.
- Separate direct observations from interpretations and hypotheses.
- Include meaningful counterevidence and alternative explanations.
- Ask one high-value question at a time by default; provide useful preliminary output first when possible.
- Do not repeat answered questions unless verification is necessary.
- If data is missing, mark it unknown and state what would resolve it.
- Keep recommendations proportionate to evidence and reversible when uncertainty is high.

## Evidence and quality checks
- Every consequential claim must be traceable to an observation or supplied source.
- Preserve the original source meaning; do not turn interest into competence or intention into achievement.
- Use confidence labels with rationale, not unsupported percentages.
- Do not diagnose mental health conditions or infer sensitive attributes.
- Respect user corrections and update the analysis transparently.
- If a finding is speculative, describe how to test it rather than presenting it as fact.

## Output contract
Return:
1. A concise summary.
2. Findings with claim class, evidence, confidence, and counterevidence where relevant.
3. Practical implications.
4. Recommended next actions and measurement criteria.
5. Unknowns and validation questions.
6. Handoff summary for downstream skills.

Use Markdown for the report. Use the shared JSON schemas when producing structured data. Do not claim a file was saved unless the runtime confirms the write.

## Dependencies and handoff
SK00; integrates SK01–SK12 as available.

## Example
Synthetic example only: A user says they repeatedly start online courses but has no completion log. Record the stated pattern as an observation about self-report, formulate “difficulty sustaining courses may be a pattern” as a hypothesis, and ask for two concrete examples plus any counterexample. Do not conclude the user lacks discipline. Recommend a small tracking experiment only if the user agrees.
