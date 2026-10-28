# Personal Human Map workflow

## Stage 0 — Consent and scope
- Capture the decision/question this map should support.
- Confirm which sources can be used and whether third-party feedback is authorized.
- Treat date of birth and other sensitive personal data as optional; collect only if relevant and consented.

## Stage 1 — Inventory and baseline
- Inventory current evidence and source dates.
- Separate direct evidence from prior AI-generated summaries.
- Mark copied/repeated sources with the same independence group.
- Produce a baseline map with unknowns; do not delay all value until every assessment is complete.
- Store interview episodes with stable evidence IDs, date/round, source class, verbatim user report or faithful summary, context, outcome, and limitations. Do not promote AI synthesis to primary evidence.

## Stage 2 — Assessment plan
Select only modules that answer open questions:
- personality questionnaire(s), with instrument/version and scoring notes;
- cognitive/decision scenario(s);
- structured interview about concrete behavioral episodes;
- work sample or performance task where capability is at issue;
- observer feedback only with appropriate consent.
Do not assume a questionnaire is validated merely because it has a score or popular label.

## Stage 3 — Mechanism extraction
For each episode record: context, trigger, goal, constraints, attention, interpretation, options considered, decision rule, action, outcome, post-event learning, and counterexample. Mark internal steps as self-reported unless directly observable.

## Stage 4 — Constraint, capacity, and workload model
For every active goal/task, distinguish:
- **externally required**: obligation with a documented or user-reported consequence if delayed;
- **negotiable**: deadline/scope/ownership may be changed by a person or stakeholder;
- **discretionary**: can be postponed or paused without violating a binding obligation;
- **blocked/waiting**: progress depends on data, trial results, materials, collaborators, or another external condition;
- **unclear**: evidence does not yet support a classification.

For each item, capture (when known): estimated effort, actual time spent, next concrete milestone, due date, dependency/owner, cost of delay, and who can change the constraint. Compare total effort with real available capacity; do not invent estimates. Separate waiting time from active work time. Keep "total workload exceeds capacity" distinct from "too many tasks active at once."

## Stage 5 — Claim generation and challenge
- Create claims with stable IDs.
- Link evidence and counterevidence.
- Add at least two plausible competing mechanisms for consequential claims when the evidence supports multiple explanations.
- For each mechanism state: predicted observations, counterevidence that would weaken it, and a discriminating test.
- Consider at minimum: capacity overload, concurrent-goal/WIP overload, external dependencies, discretionary overcommitment, context-switching cost, and decision uncertainty when relevant.
- Check source independence and contextual variation.
- Keep interpretive systems in a separate lane; never let them support empirical claims.

## Stage 6 — Draft synthesis
Generate the provisional map with mechanism-first findings, capability evidence, context-specific trade-offs, contradictions, unknowns, and measurable development experiments. Separate observed evidence, self-report, inference, and hypotheses.

## Stage 7 — Adversarial review round 1
Use `prompts/RED_TEAM_PERSONAL_HUMAN_MAP.md` to attack the draft:
- find unsupported claims and generic statements;
- propose plausible rival mechanisms;
- identify missing counterexamples and source dependence;
- check if external constraints are incorrectly attributed to personal weakness, or if discretionary choices are incorrectly excused as external necessity;
- test whether recommendations could fail and produce useful evidence;
- inspect privacy, safety, and interpretive-lane violations.
Record exact claim IDs and proposed changes.

## Stage 8 — Revision
For each critique, record `accepted`, `partially_accepted`, or `rejected_with_reason`. Remove or downgrade unsupported claims. Do not silently ignore critiques or add caveats to preserve an otherwise unsupported thesis.

## Stage 9 — Adversarial review round 2
Review the revised map for unresolved blockers and regressions. Review round 2 must focus on whether the revision fixed the original problem, not repeat the first review mechanically. Explicitly ask:
- Did the revision distinguish constraint from choice?
- Does each proposed intervention match the mechanism actually supported?
- What evidence would falsify the preferred explanation?
- Did the revision mistake user agreement for independent validation?
A claim can remain only if its evidence and scope justify it.

## Stage 10 — User-fit and release gate
Compare the revised map against the user's stated goal and feedback. Score it with `evaluations/personal-human-map/QUALITY_RUBRIC.md`.
- Any zero for evidence traceability, calibration, or safety means fail.
- Total score below 16/24 means revise.
- Passing a numeric threshold does not override a critical unsupported claim, privacy problem, or evidence-lane breach.
- If independent review or tests were not run, disclose that fact and do not claim they passed.
- If the gate fails, deliver a provisional map and a prioritized evidence plan rather than false certainty.

## Stage 11 — Validation loop
Each experiment states a hypothesis, context, baseline, action, measure, success threshold, duration, and review date. Use reversible experiments. After review, mark supported, not supported, or inconclusive; retain the historical claim version. For workload questions, prefer low-cost measurement and small reversible changes (e.g. one-week workload inventory or limiting active work-in-progress) before prescribing broad productivity routines.

## Quality principles
Do not publish a high-confidence finding if evidence is thin, dependent, stale, contradicted, or only symbolic. Do not present personality as immutable. Keep recommendations traceable to claims and measurable outcomes. Distinguish independent review from self-critique.
