# Personal Human Map quality rubric

Score each dimension 0–3. Scores are reviewer aids, not psychometric scores or a measure of the person.

- **Evidence traceability**: 0 unsupported; 1 vague sources; 2 most material claims traceable; 3 all material claims have provenance and counterevidence.
- **Mechanism depth**: 0 labels only; 1 generic cause; 2 context-specific chain; 3 chain separates observed links from hypotheses and tests alternatives.
- **Personalization**: 0 generic; 1 some domain details; 2 multiple concrete episodes; 3 claims depend on specific evidence and include disconfirming cases.
- **Calibration**: 0 certainty without support; 1 some caveats; 2 confidence matches evidence; 3 uncertainty, source dependence, scope and contradictions handled explicitly.
- **Alternative explanations**: 0 none; 1 token alternatives; 2 plausible alternatives; 3 alternatives have discriminating tests.
- **Capability validity**: 0 interests treated as skills; 1 self-report only; 2 some performance evidence; 3 repeated relevant performance and transfer evidence distinguished from potential.
- **Actionability**: 0 generic advice; 1 broad recommendations; 2 linked actions; 3 low-cost experiments have baseline, metric, threshold, duration and review date.
- **Safety and separation**: 0 unsafe mixing/leakage; 1 weak disclaimers; 2 lanes separated; 3 access, consent and inference boundaries are explicit.

## Release gates
- Any 0 in evidence traceability, calibration, or safety means **fail**.
- A total below 16/24 means **revise**.
- A total of 16+ is not enough by itself: no critical unsupported claim, privacy issue, or interpretive/empirical lane breach may remain.
- A score of 3 requires concrete examples from the draft; reviewer must cite the exact claim/section.
- Do not average away a failed critical dimension.

## Review rounds
1. Draft generation.
2. Independent red-team critique.
3. Revision based on critique.
4. Second red-team review focused on regressions and unresolved blockers.
5. User-fit review: compare against explicit goal and prior feedback.
6. Release only after gates pass; otherwise deliver a provisional map and a data-collection plan.
