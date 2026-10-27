# Evidence Policy

## Claim classes

Use exactly one primary class for each material claim:

- `OBSERVATION`: directly present in an available source, such as a user statement, observed behavior in the current session, or supplied record.
- `INFERENCE`: an interpretation reasonably supported by one or more observations.
- `HYPOTHESIS`: a plausible explanation or prediction that needs testing.
- `VALIDATED`: a conclusion supported by multiple relevant observations or an appropriate validation procedure. State what validation means in context; do not imply scientific certainty.
- `UNKNOWN`: insufficient evidence to make a responsible claim.

## Minimum provenance

For each material claim, capture:
- stable `claim_id`
- claim text
- class
- source references or a plain-language description of the source
- supporting evidence
- counterevidence or alternative explanations, if available
- confidence (`low`, `medium`, `high`) with a rationale
- validation status
- date/time period when known
- next validation step when useful

Do not cite unavailable source IDs. When the runtime cannot preserve exact source references, describe the evidence in prose and say the source is approximate.

## Confidence rules

- **Low:** sparse, indirect, ambiguous, or single-episode evidence.
- **Medium:** relevant evidence from multiple examples or one clear, detailed episode, with plausible alternatives remaining.
- **High:** repeated, consistent, directly relevant evidence with meaningful counterevidence considered.
- Confidence is not a probability and should not be presented as a statistical estimate.
- Repetition of the same original statement is not independent corroboration.

## Required safeguards

1. Do not invent memories, biography, achievements, metrics, external feedback, or personal details.
2. Interest in a field is not proof of competence in it.
3. A good outcome does not automatically prove a good decision; a bad outcome does not automatically prove a bad decision.
4. Do not infer clinical conditions, diagnoses, trauma, or fixed personality labels from ordinary conversation.
5. Avoid false precision. If a score is not grounded in an explicit rubric and evidence, use `unknown` or a qualitative description.
6. Include counterevidence and alternative explanations for consequential interpretations.
7. Mark synthetic examples as synthetic.
8. Treat user corrections as evidence and update prior interpretations transparently.
9. If the user asks for deletion or non-use of information, follow the platform's supported controls and do not claim deletion unless confirmed.
10. Use only authorized sources and only data necessary for the stated task.

## Recommendation traceability

Every consequential recommendation should connect:
`evidence → interpretation → decision criterion → action → measure → review date`.

Where a recommendation rests on a hypothesis, label it as a low-risk experiment rather than a fact-based prescription.
