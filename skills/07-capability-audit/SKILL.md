# Capability & Evidence Auditor

## Purpose
Audit demonstrated capability and achievements using explicit evidence.

## Scope
This skill is portable and runtime-agnostic. Follow `../../config/evidence-policy.md`, `../../config/interview-policy.md`, and `../../config/output-contracts.md` when available. If those files are unavailable in the execution environment, apply the rules summarized in this document and state the limitation.

## Inputs and outputs
Inputs: projects, work samples, results, feedback, role requirements.
Output: capability matrix, evidence-backed accomplishments, gaps, optional rubric-based estimates.
Interest in a field is not proof of competence; no unsupported IQ or employability scores.

## Workflow
1. Inventory claimed skills, projects, work samples, achievements, and measurable outcomes.
2. Classify each capability as exposure, conceptual understanding, guided execution, independent execution, or repeatedly demonstrated advanced performance.
3. Define criteria before scoring; do not invent a universal rubric.
4. Link claims to work samples, outcomes, or detailed examples.
5. Separate team outcomes from the user's individual contribution.
6. Identify missing evidence and contradictory examples.
7. Recommend a practical assessment or portfolio artifact for priority gaps.
8. Produce a capability matrix with confidence and next validation step.

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
SK03, SK06, SK08, SK09, SK13.

## Example
Synthetic example only: A user says they repeatedly start online courses but has no completion log. Record the stated pattern as an observation about self-report, formulate “difficulty sustaining courses may be a pattern” as a hypothesis, and ask for two concrete examples plus any counterexample. Do not conclude the user lacks discipline. Recommend a small tracking experiment only if the user agrees.
