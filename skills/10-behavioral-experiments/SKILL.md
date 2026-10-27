# Behavioral Experiment Designer

## Purpose
Test personal-development hypotheses through small, measurable experiments.

## Scope
This skill is portable and runtime-agnostic. Follow `../../config/evidence-policy.md`, `../../config/interview-policy.md`, and `../../config/output-contracts.md` when available. If those files are unavailable in the execution environment, apply the rules summarized in this document and state the limitation.

## Inputs and outputs
Inputs: hypothesis, baseline data, constraints, user consent.
Output: experiment plan, metric definitions, tracking schedule, evaluation report.
Do not claim causality from a weak uncontrolled experiment.

## Workflow
1. Select one important hypothesis that could change a decision.
2. Write the hypothesis, alternative explanations, baseline, intervention, and measurable outcome.
3. Keep duration and burden proportionate; use 14–90 days when appropriate.
4. Define success, failure, stop conditions, and confounders before starting.
5. Prefer reversible experiments and avoid unnecessary risk.
6. Create a simple logging schedule.
7. At review, compare results to baseline and consider missing data or changing circumstances.
8. Classify the hypothesis as supported, contradicted, or unresolved; do not overgeneralize.

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
SK04, SK05, SK09, SK11, SK12, SK13.

## Example
Synthetic example only: A user says they repeatedly start online courses but has no completion log. Record the stated pattern as an observation about self-report, formulate “difficulty sustaining courses may be a pattern” as a hypothesis, and ask for two concrete examples plus any counterexample. Do not conclude the user lacks discipline. Recommend a small tracking experiment only if the user agrees.
