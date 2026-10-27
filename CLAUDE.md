# Claude Code instructions for Personal Intelligence

When working in this repository:

1. Read `README.md`, `USAGE_GUIDE.md`, `config/evidence-policy.md`, `config/interview-policy.md`, and `config/output-contracts.md` before running the workflow.
2. Start from `skills/00-orchestrator/SKILL.md`. Read additional `skills/<id>/SKILL.md` files only as needed for the current stage.
3. Treat Markdown and JSON as the portable source of truth. Do not claim these files are automatically installed as native slash-command skills.
4. Separate observed evidence, user-reported information, inference, and unknowns. Never invent biography, outcomes, feedback, or scores. Do not diagnose the user.
5. Ask one high-value question at a time by default. Do not repeat answered questions; provide useful preliminary analysis when evidence supports it.
6. Save personal reports only under `outputs/` when the user asks for files to be saved. Do not put private personal records into public source files.
7. Do not modify source files, delete data, or commit/push changes unless explicitly asked. Show diffs for changes.
8. Never expose secrets. Encourage redaction of other people's private information.

For first-time setup, follow `USAGE_GUIDE.md`.
