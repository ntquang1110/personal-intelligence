# Skill Dependency Graph

```mermaid
flowchart TD
  S00[SK00 Orchestrator] --> S01[SK01 Life Timeline]
  S00 --> S02[SK02 Identity & Values]
  S00 --> S03[SK03 Cognitive Style]
  S01 --> S04[SK04 Behavioral Patterns]
  S03 --> S07[SK07 Capability Audit]
  S04 --> S05[SK05 Decision Intelligence]
  S02 --> S06[SK06 Feedback 360]
  S06 --> S07
  S07 --> S08[SK08 Career Strategy]
  S02 --> S09[SK09 Life Strategy]
  S08 --> S09
  S04 --> S10[SK10 Behavioral Experiments]
  S09 --> S10
  S09 --> S11[SK11 Personal Operating System]
  S10 --> S12[SK12 Evolution Tracker]
  S11 --> S12
  S01 --> S13[SK13 Final Synthesis]
  S02 --> S13
  S03 --> S13
  S04 --> S13
  S05 --> S13
  S06 --> S13
  S07 --> S13
  S08 --> S13
  S09 --> S13
  S10 --> S13
  S11 --> S13
  S12 --> S13
```

Dependencies are recommendations, not mandatory blockers. A skill may run independently with reduced scope when upstream data is absent. The report must disclose missing inputs rather than fabricate them.
