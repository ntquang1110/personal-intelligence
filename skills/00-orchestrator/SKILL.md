# Personal Intelligence Orchestrator

## Purpose
Coordinate a staged, evidence-aware assessment and integrate independent skill outputs. For deep personal diagnostics, build an evolving Personal Human Map rather than a static personality verdict.

## Scope
This skill is portable and runtime-agnostic. Follow `../../config/evidence-policy.md`, `../../config/interview-policy.md`, `../../config/output-contracts.md`, and `../../docs/PERSONAL_HUMAN_MAP.md` when available. If those files are unavailable in the execution environment, apply the rules summarized here and state the limitation.

## Inputs and outputs
Inputs: user goal, available conversation/files, existing skill outputs, runtime capabilities.
Output: execution plan, source inventory, dependency graph, status manifest, integrated report manifest, and when requested a structured human map.
Failure handling: if history or files are unavailable, state that and proceed with current evidence. Never claim persistence without confirmed file writes.

## Workflow
1. Read shared evidence, interview, output, privacy, and human-map policies.
2. Inventory only sources actually available and authorized; classify source type, access, date range, context, and limitations.
3. Identify the decision the user wants to improve. If unclear, ask one high-value question.
4. Reuse reliable existing artifacts and mark stale, repeated, or missing data. Treat copied summaries as the same evidence lineage, not independent corroboration.
5. Produce a useful provisional summary before requesting more information.
6. Select modules by open question, not by a default full battery: assessment interpretation, cognitive/decision tasks, structured interview, capability/work sample, behavioral episodes, observer feedback, or longitudinal review.
7. For useful episodes, capture context, trigger, goal, constraints, attention, interpretation, options, decision rule, action, outcome, and post-event learning. Mark unobservable mental steps as self-report or hypothesis.
8. Generate claims with evidence, counterevidence, alternatives, scope conditions, confidence rationale, and a validation test.
9. Preserve contradictions across instruments, self-report, observed behavior, and contexts. Do not average disagreement away.
10. Keep astrology, numerology, zodiac, and similar systems in a separate interpretive-only appendix. Never use them to support empirical claims or infer competence, diagnosis, destiny, or suitability.
11. Distinguish interest, knowledge, skill, demonstrated capability, and potential hypothesis.
12. Synthesize when enough relevant evidence exists; track completed, blocked, skipped, and pending modules.
13. State which files were actually created and which were only proposed.

## Decision rules
- Use only data actually available and authorized.
- Separate direct observations from interpretations and hypotheses.
- Include meaningful counterevidence and alternative explanations.
- Ask one high-value question at a time by default; do not repeat answered questions without a reason.
- If data is missing, mark it unknown and state what would resolve it.
- Keep recommendations proportionate to evidence and reversible when uncertainty is high.
- Never infer a stable trait from a single episode without explicit qualification.
- Repeated examples from the same source or copied AI summaries do not count as independent corroboration.

## Evidence and quality checks
- Every consequential claim must be traceable to an observation or supplied source.
- Preserve source type, date, context, and limitations.
- Do not turn interest into competence or intention into achievement.
- Use qualitative confidence labels with rationale, not unsupported percentages.
- Do not diagnose mental health conditions or infer sensitive attributes.
- Respect user corrections and update the analysis transparently.
- For every important inference, ask what else could explain the same behavior and what evidence would distinguish the explanations.
- Do not let symbolic/interpretive systems alter empirical confidence.
- A report fails if it sounds personalized but could fit almost anyone.

## Output contract
Return:
1. Concise summary and scope.
2. Evidence inventory and gaps.
3. Mechanism-first findings with claim class, evidence, confidence, counterevidence, and rival explanations.
4. Context-specific strengths, costs, and failure conditions.
5. Capability map with demonstrated versus untested abilities separated.
6. Practical implications and linked validation experiments.
7. Unknowns and next high-value question.
8. Separate interpretive appendix only when requested.
9. Handoff summary for downstream skills.

Use Markdown for reports and shared JSON schemas for structured artifacts. Do not claim a file was saved unless the runtime confirms the write.

## Dependencies and handoff
Use SK01–SK12 as needed and SK13 for synthesis. For Personal Human Map, follow `workflows/personal-human-map.md`.

## Example
Synthetic example only: A user says they repeatedly start online courses but has no completion log. Record the statement as self-report, formulate “difficulty sustaining courses may be a pattern” as a hypothesis, and ask for concrete examples plus counterexamples. Alternative explanations could include low relevance, external interruptions, or a mismatch between course format and learning needs. Do not conclude the user lacks discipline.
