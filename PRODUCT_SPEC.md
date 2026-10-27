# Personal Intelligence v2 — Product Specification

## Objective
Build a continuously updated, evidence-grounded overview of a person and use it to improve career, relationships, family, financial, lifestyle, and personal-development decisions. This is a decision-support system, not a personality quiz or diagnostic product.

## User outcomes
1. Understand identity, history, motives, capabilities, behavior, relationships, resources, constraints, and environment.
2. Separate known facts from inference, uncertainty, contradictions, and missing evidence.
3. Identify strengths to compound, weaknesses to improve, risks to manage, and contexts to change.
4. Compare career and life options using explicit criteria and trade-offs.
5. Turn conclusions into prioritized actions with measures and review loops.
6. Track change without treating old conclusions as permanent truths.

## Lifecycle
Discover → structure evidence → build profile → diagnose → explore options → choose strategy → run experiments → review outcomes → update profile.

## Deliverables
- Personal Overview and current-state map.
- Deep Profile across 12 domains.
- Diagnostic Report: strengths, bottlenecks, hypotheses, blind spots, risks, leverage points.
- Career Strategy and Life Strategy with options and trade-offs.
- 90-Day Plan with ranked actions, experiments, and measures.
- Progress Review and machine-readable JSON records.

## Twelve domains
D01 identity and values; D02 life history; D03 cognitive style; D04 behavior and execution; D05 strengths and capabilities; D06 career and work; D07 family; D08 friends and social network; D09 finance and resources; D10 lifestyle and energy; D11 life strategy; D12 evolution and progress.

## Analytical standard
Classify material claims as fact, self-report, observation, inference, hypothesis, or unknown. Preserve source, context/date, confidence, and counterevidence where available. Avoid unsupported numeric personality scores.

## Recommendation standard
Each material recommendation states the opportunity/problem, evidence and confidence, expected benefit and trade-off, why now, first action, progress signal, and review condition.

## Safety and privacy
Do not diagnose mental or physical health conditions. Do not infer sensitive traits without explicit disclosure and relevance. Analyze third-party relationships through reported interactions, not confident labels. Do not promise financial or career outcomes. Users can challenge or correct interpretations. Keep populated personal data out of public Git history.

## Definition of done
A useful first synthesis exists when major domains contain enough evidence to identify priorities, high-impact unknowns are explicit, and each major conclusion is traceable to evidence or marked as a hypothesis.
