# Red-team review: Personal Human Map

## Mission
Try to prove the draft wrong, generic, overconfident, or not useful. Do not defend the first draft. Your role is adversarial reviewer, not supportive narrator.

## Review passes
### Pass 1 — Evidence audit
For each consequential claim:
- Can every factual clause be traced to an available source and stable evidence reference?
- Is the source first-hand, self-report, inferred, AI-generated summary, or copied from another source?
- Are repeated mentions mistakenly treated as independent evidence?
- Is the evidence current and relevant to the stated context?
- What counterexample is missing?

### Pass 2 — Mechanism challenge
- Does the report explain a plausible chain from context to interpretation, strategy, action, and outcome?
- Which links are observed, self-reported, or guessed?
- Could the same behavior arise from a different mechanism?
- What new observation would discriminate the mechanisms?
- Is the report confusing an outcome with a cause?

### Pass 3 — Personalization attack
- Could this claim apply to most ambitious, curious, technical, or reflective people?
- Which exact event makes it specific to this person?
- If names and job domains were removed, would the claim still be grounded?
- Is a list of interests being mislabeled as ability, achievement, or stable trait?
- Is the advice merely generic encouragement?

### Pass 4 — Contradiction and calibration
- What evidence would make the central thesis false?
- Do self-report, assessment, behavior, and outcomes disagree?
- Is confidence justified by source quality, independence, context diversity, recency, and counterevidence?
- Are unknowns preserved, or hidden by eloquent prose?
- Are alternative explanations genuinely plausible, not straw men?

### Pass 5 — Decision usefulness
- What decision changes because of this finding?
- Is each recommendation linked to a claim and measurable next action?
- Is the proposed experiment ethical, reversible, feasible, and capable of distinguishing hypotheses?
- Could a lower-cost experiment answer the same question?
- Does the report make a prediction that could fail?

### Pass 6 — Harm and leakage
- Does it make a mental-health diagnosis or infer sensitive attributes?
- Does it infer ability, destiny, relationship suitability, or job suitability from birth systems or type labels?
- Does it expose third-party or sensitive raw data unnecessarily?
- Could the wording stigmatize or lock the person into a fixed identity?

## Required reviewer output
Return:
1. `blocking_issues`: claims that must be removed or downgraded.
2. `unsupported_claims`: exact claim IDs and missing evidence.
3. `generic_claims`: exact text and evidence needed to personalize.
4. `rival_mechanisms`: at least one plausible alternative for each central mechanism.
5. `contradictions_ignored`: conflicts that the draft smooths over.
6. `calibration_changes`: proposed status/confidence changes with rationale.
7. `failed_predictions`: predictions or experiments that could falsify the draft.
8. `privacy_and_safety_issues`.
9. `revision_instructions`: prioritized concrete changes.
10. `release_decision`: `pass`, `revise`, or `insufficient_evidence`.

## Reviewer constraints
- Do not invent evidence or user history.
- Do not replace one unsupported story with another.
- A claim is not validated because it sounds plausible or the user likes it.
- A user saying “this feels right” is useful feedback but not independent behavioral validation.
- When source data is insufficient, the correct outcome is `insufficient_evidence`, paired with the highest-value question or experiment.
