# Critical Review: Gaps and Roadmap

## Honest assessment
The current v2 is a strong instruction-and-schema framework, but it is not yet a functioning application or a validated matching product. It does not provide a database, authenticated sharing, access control, expiring links, revocation enforcement, a matching algorithm, a real interview workflow, or a production test suite.

## Critical gaps found
1. **The system is mainly descriptive.** It explains domains and engines but has few operational flows connecting inputs to consistent outputs.
2. **Matching is one-sided.** Career strategy assesses the user against roles, but not whether the role, manager, employer, or relationship context fits the user.
3. **No sharing boundary.** A single profile model does not yet define a purpose-specific export or explicit recipient consent.
4. **No mutual review.** There is no structured way for two participants to independently submit needs, review the same criteria, correct findings, and make separate decisions.
5. **Weak test coverage.** Repository contract tests check existence and JSON parsing, not full JSON Schema validity, compatibility, privacy rules, or end-to-end workflows. The v2 tests also replaced some v1-specific assertions; future tests should preserve both sets of invariants.
6. **Versioning mismatch risk.** The main profile uses schema version 2.0 while new matching artifacts are 2.1; migrations and compatibility rules need to be explicit.
7. **Evidence provenance is incomplete in some schemas.** Shared records should consistently capture source, date/context, confidence rationale, and counterevidence where appropriate.
8. **No real access-control guarantee.** Markdown instructions cannot enforce private links, expiry, revocation, or prevent copying.
9. **No user research.** We have not tested whether the questions are understandable, fair, culturally appropriate, or useful to candidates and couples.

## Proposed roadmap
### P0 — Trust and safety
- Separate private profile from audience-specific share profiles.
- Add explicit consent, minimum disclosure, correction, review date, and withdrawal guidance.
- Add job-related fairness constraints and prohibit automatic rejection.
- Add mutual and partner compatibility rules that avoid diagnosis and universal scores.

### P1 — Usable workflows
- Add job-fit review, partner compatibility review, and shareable-profile prompts.
- Add structured schemas for shareable profiles and mutual review.
- Provide examples using synthetic data only.
- Add schema-validation tests and preserve v1 invariants.

### P2 — Actual product
- If desired, build an application with authentication, access control, encrypted storage, revocable share links, audit logs, and export/delete controls.
- Validate matching outputs with real users and monitor for bias, misunderstanding, and overconfidence.
- Only then consider scoring; start with explainable criterion-by-criterion comparison instead of one opaque score.

## Release gate
Do not describe sharing as secure or revocable until the implementation enforces those properties. Do not use this framework as an automated hiring or partner-selection decision system.
