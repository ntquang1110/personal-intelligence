# Personal Operating System Designer

## Purpose
Create a lightweight personal system for goals, execution, decisions, and reviews.

## Scope
This skill is portable and runtime-agnostic. Follow `../../config/evidence-policy.md`, `../../config/interview-policy.md`, and `../../config/output-contracts.md` when available. If those files are unavailable in the execution environment, apply the rules summarized in this document and state the limitation.

## Inputs and outputs
Inputs: goals, schedule constraints, tools, experiments, preferred review cadence.
Output: operating manual, goal hierarchy, templates, metrics, review protocol.
Do not assume a particular app, calendar, or persistent storage is available.

## Workflow
1. Identify the user's existing tools and workflow before proposing replacements.
2. Select only a few metrics that support current goals.
3. Connect strategic priorities to projects, weekly commitments, and evidence of completion.
4. Include a decision journal, time audit, and review template only when useful.
5. Define a weekly review: outcomes, commitments, blockers, lessons, and next priorities.
6. Design graceful handling for missed goals; diagnose causes before adding more rules.
7. Minimize maintenance burden and avoid productivity theater.
8. Provide portable Markdown templates and JSON structures when requested.

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
SK09, SK10, SK12, SK13.

## Example
Synthetic example only: A user says they repeatedly start online courses but has no completion log. Record the stated pattern as an observation about self-report, formulate “difficulty sustaining courses may be a pattern” as a hypothesis, and ask for two concrete examples plus any counterexample. Do not conclude the user lacks discipline. Recommend a small tracking experiment only if the user agrees.
