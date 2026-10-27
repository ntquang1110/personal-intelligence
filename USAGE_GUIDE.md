# Using Personal Intelligence with ChatGPT or Claude

This repository is a set of Markdown instructions and JSON schemas. It is **not** a hosted app, and uploading it does not create automatic long-term memory. You choose what material to provide, review the analysis, and save any outputs you want to keep.

Repository: <https://github.com/ntquang1110/personal-intelligence>

## Choose a setup

| Where you use the model | Recommended method | What persists? |
|---|---|---|
| ChatGPT in a normal chat | Upload the ZIP or the relevant Markdown files, then paste the starter prompt below | Treat files produced in the chat as downloadable artifacts; do not assume they are written back to GitHub or available in a new chat |
| ChatGPT Project | Add the project instructions and relevant repository files to the Project's instructions/files, then start a chat with the starter prompt | Project context/files may be available in that Project; still explicitly save/export updated reports |
| Claude web chat / Project | Upload the ZIP or relevant files; add the starter prompt to Project instructions if using a Project | Do not assume a conversation writes files back to your repository |
| Claude Code | Clone the repo locally and ask Claude Code to read `CLAUDE.md` and the orchestrator | Local files can be edited if you grant Claude Code access; review diffs before committing |

Product UI and file-upload limits can change. If a client cannot inspect a ZIP, extract it locally and upload the required files or smaller groups of files instead.

## Fast start: ChatGPT or Claude web

1. Download the repository ZIP from GitHub, or use **Code → Download ZIP** on the repository page.
2. Open ChatGPT or Claude and start a new chat. For ongoing work, create a Project and add the files there.
3. Upload the ZIP. If the model cannot inspect the archive, extract it and upload these first:
   - `README.md`
   - `config/evidence-policy.md`
   - `config/interview-policy.md`
   - `config/output-contracts.md`
   - `skills/00-orchestrator/SKILL.md`
4. Ask the model to list the files it can actually read. Have it request additional skill files only when needed.
5. Paste the starter prompt below. Begin with the orchestrator rather than asking for a definitive personality label immediately.
6. Review each claim, correct inaccuracies, and ask the model to distinguish observed evidence from hypotheses.
7. When you want to keep results, request Markdown and JSON outputs. Download them yourself and store them in a private copy of the repository, for example under `outputs/`. Never assume the model saved files unless it provides an actual file or confirms a supported write operation.

### Starter prompt (copy and paste)

> You are operating the Personal Intelligence system from the repository `https://github.com/ntquang1110/personal-intelligence`.
>
> First, inspect the files that are actually available to you. Read `README.md`, the three policies in `config/`, and `skills/00-orchestrator/SKILL.md`. Do not claim to have read files you cannot access. Follow the repository's evidence policy, interview policy, and output contracts.
>
> Start with a short evidence inventory: what you know from material I explicitly provided, what is only a hypothesis, and what is unknown. Then propose a staged self-understanding plan. Ask one high-value question at a time, avoid repeating questions I have already answered, and provide useful preliminary observations when evidence supports them. Do not invent personal history, motives, feedback, scores, or facts. Do not diagnose me. Let me correct your interpretations.
>
> When a skill is needed, read its `skills/<id>/SKILL.md` file before using it. At the end of a meaningful stage, offer a concise Markdown report and, when appropriate, JSON conforming to the repository schemas. Do not claim persistent memory or file writes unless this environment actually supports them. Begin with the evidence inventory and proposed first stage; do not try to run all 14 skills at once.

## ChatGPT-specific notes

### Normal chat

- Attach the repository ZIP or the relevant extracted files directly to the conversation.
- If only some files are accessible, work only from those files and say what is missing.
- For a new conversation, upload the needed files again unless you are using a Project or another supported feature that makes them available.
- Ask for downloadable `.md` or `.json` files when you want to preserve results. The model does not push changes to GitHub just because the repository URL was mentioned.

### Project

- Create a ChatGPT Project for this work if you want a stable place for the instructions and files.
- Add the starter prompt (or a shorter version of it) to Project instructions, and upload the repository files to the Project.
- Keep the source repository separate from personal outputs. Add only the files needed for the current stage to reduce noise and protect privacy.

If your ChatGPT account offers a GitHub connector, you may use it to access supported repository content after connecting it. Do not assume it is enabled, and do not assume read access means write/commit access. The upload workflow above works without a connector.

## Claude-specific notes

### Claude web chat / Project

- Upload the ZIP or the relevant Markdown files to a conversation or Project.
- Add the starter prompt to Project instructions for repeated use.
- Ask Claude to confirm which files it can read before relying on a skill or schema. Upload additional files when needed.
- Export/download the resulting reports and put them into your own local repository if you want version history.

### Claude Code (local repository workflow)

From a terminal, clone the repository and open Claude Code in the repository directory:

```bash
git clone https://github.com/ntquang1110/personal-intelligence.git
cd personal-intelligence
claude
```

Then ask Claude Code:

```text
Read CLAUDE.md, README.md, config/evidence-policy.md,
config/interview-policy.md, config/output-contracts.md, and
skills/00-orchestrator/SKILL.md. Follow them as the project workflow.
Start by inventorying available evidence and proposing a staged plan.
Do not modify source files unless I ask. Save personal reports only under
outputs/ and show me the diff before any commit.
```

Claude Code may be able to read and edit local files because it runs in your working directory. Review file changes before accepting them. This repository's `skills/*/SKILL.md` files are portable instruction documents; they are **not guaranteed to auto-register as native slash-command skills** in every client. The root `CLAUDE.md` tells Claude Code how to discover and use them in this repository.

## A sensible first session

1. **Evidence inventory** — list available sources and their limitations.
2. **Life timeline** — capture major events only when useful and at the precision the user can support.
3. **Identity and values** — compare stated values with concrete examples.
4. **Cognitive and behavioral patterns** — label interpretations as hypotheses until supported by repeated examples.
5. **Capability and decision audit** — use evidence, counterexamples, and uncertainty rather than invented scores.
6. **Experiments** — choose one small, measurable behavior experiment and define a review date.
7. **Synthesis** — create a versioned Markdown report and relevant JSON records.

This is a suggested route, not a requirement. Skip modules that do not fit your goal.

## Privacy and quality checklist

- Do not upload passwords, API keys, authentication cookies, identity documents, or other secrets.
- Remove or anonymize other people's private conversations unless you have permission and a clear need.
- Do not treat the model's interpretation as an objective or clinical truth.
- For important conclusions, ask: **What evidence supports this? What might disprove it? How confident are you?**
- Keep private reports out of a public GitHub repository. Check `.gitignore` and repository visibility before committing anything under `outputs/`.
- Use synthetic or redacted examples when testing or sharing the project.

## Troubleshooting

- **The model says it cannot open the GitHub URL:** download the ZIP and upload it, or extract and upload the relevant files.
- **The model cannot read the ZIP:** extract it locally and upload the files individually or in smaller batches.
- **The model gives generic advice without following the workflow:** ask it to quote the filenames it inspected, reread the orchestrator and policies, and restart with an evidence inventory.
- **The model invents facts:** ask it to mark each claim as `observed`, `reported`, `inferred`, or `unknown`, with source evidence where available.
- **You want to continue in a later chat:** bring forward the latest report and relevant JSON records; do not rely on undocumented cross-chat memory.
