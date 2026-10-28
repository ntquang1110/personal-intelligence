# Red-team review: Personal Human Map

## Mission
Try to prove the draft wrong, generic, overconfident, or not useful. Do not defend the first draft. Your role is adversarial reviewer, not supportive narrator.

## Review passes
### Pass 1 — Evidence audit
- Trace every consequential factual clause to a stable evidence ID and identify whether it is self-report, observed, inferred, AI-generated, or copied.
- Check source lineage; repeated statements from the same interview/chat are not independent corroboration.
- Identify missing counterexamples and evidence that could reverse the conclusion.

### Pass 2 — Mechanism challenge
- Test the chain from context to attention, interpretation, decision, action, and outcome.
- Separate observed links from self-reported links and hypotheses.
- For each central claim, provide at least two plausible competing mechanisms when possible, with predicted observations and discriminating tests.
- Check whether outcome is being confused with cause.

### Pass 3 — Constraint-versus-choice audit
For workload, productivity, delay, and execution claims, explicitly challenge:
- total demand exceeding actual available capacity;
- too many simultaneously active goals/tasks (work-in-progress overload);
- external obligations, dependencies, waiting time, or coordination;
- discretionary goals that could be paused but remain active;
- context-switching costs;
- decision uncertainty or unclear completion criteria.
Do not assume a constraint is immovable because it is described as required; ask who controls it and what the consequence of changing it would be. Do not assume a delay is a personal failure when external evidence is missing. Equally, do not use external constraints to excuse choices without evidence.

### Pass 4 — Personalization attack
- Could the claim apply to most ambitious, curious, technical, or reflective people?
- Which exact event makes it specific to this person?
- Is interest mislabeled as capability, or a single episode generalized into a stable trait?
- Is advice generic rather than tied to evidence?

### Pass 5 — Contradiction and calibration
- What evidence would make the central thesis false?
- Do self-report, assessments, behavior, and outcomes disagree?
- Is confidence justified by source quality, independence, context diversity, recency, and counterevidence?
- Are unknowns preserved rather than hidden by eloquent prose?
- Is the preferred mechanism ranked because of evidence, or merely because it sounds plausible?

### Pass 6 — Decision usefulness
- What decision changes because of this finding?
- Is each recommendation linked to a claim and measurable next action?
- Does the intervention target the mechanism supported by evidence?
- Could a reversible, lower-cost test discriminate between mechanisms?
- Is there a baseline, metric, threshold, duration, and review date?

### Pass 7 — Harm and leakage
- Does it make a mental-health diagnosis or infer sensitive attributes?
- Does it infer ability, destiny, relationship suitability, or job suitability from birth systems or type labels?
- Does it expose third-party or sensitive raw data unnecessarily?
- Could wording stigmatize or lock the person into a fixed identity?
- Does it encourage unsafe shortcuts, including relaxing scientific, animal-health, or product-safety standards to meet a deadline?

## Required reviewer output
Return:
1. `blocking_issues`: claims that must be removed or downgraded.
2. `unsupported_claims`: exact claim IDs and missing evidence.
3. `generic_claims`: exact text and evidence needed to personalize.
4. `rival_mechanisms`: competing explanations and predicted observations.
5. `constraint_choice_errors`: cases where outside constraints and personal choice are confused.
6. `contradictions_ignored`: conflicts that the draft smooths over.
7. `calibration_changes`: proposed status/confidence changes with rationale.
8. `failed_predictions`: predictions or experiments that could falsify the draft.
9. `privacy_and_safety_issues`.
10. `revision_instructions`: prioritized concrete changes.
11. `release_decision`: `pass`, `revise`, or `insufficient_evidence`.

## Reviewer constraints
- Do not invent evidence or user history.
- Do not replace one unsupported story with another.
- A claim is not validated because it sounds plausible or the user likes it.
- A user saying “this feels right” is subjective feedback, not independent behavioral validation.
- When source data is insufficient, the correct outcome is `insufficient_evidence`, paired with the highest-value question or experiment.
