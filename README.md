# Alex SDLC Copilot Agent

![](zapato1.jpg) ![](zapato2.jpg) ![](zapato3.jpg)

Alex is a **GitLab Duo Agent Platform** project for the GitLab AI Hackathon. It automates a real SDLC workflow: when a new issue or merge request event is received, Alex produces a structured engineering triage report with severity, test strategy, and release readiness checklist.

## Why this fits the hackathon requirements

- **Working AI agent/flow (not chat-only):** Alex reacts to a trigger payload and writes a concrete artifact (`triage.md`) that teams can immediately use in planning/review.
- **SDLC impact:** Reduces manual toil in issue triage, QA planning, and release gate preparation.
- **GitLab Duo Agent Platform-ready:** Includes a Duo-style agent configuration file (`duo-agent.yml`) with trigger/context/tool wiring.
- **Installable and reproducible:** Includes local run instructions, example payload, and deterministic output structure.

## Project structure

- `duo-agent.yml` – Agent configuration (trigger, context, workflow steps).
- `scripts/alex_agent.py` – Action runner that processes an event payload and produces triage output.
- `prompts/triage_prompt.md` – Prompt contract for quality and consistency.
- `examples/sample_event.json` – Sample issue/MR payload.
- `index.html` – Lightweight landing page for demo and submission support.

## Quick start

### 1) Requirements

- Python 3.10+

### 2) Run locally

```bash
python3 scripts/alex_agent.py \
  --event-file examples/sample_event.json \
  --output .gitlab/agent-output/triage.md
```

### 3) Inspect output

Open `.gitlab/agent-output/triage.md`.

## Example workflow

1. Trigger: GitLab issue opened (or MR opened).
2. Context: title, description, labels, changed files (for MR).
3. Agent action:
   - infer area + risk level,
   - propose validation test matrix,
   - generate release-readiness checklist,
   - suggest missing acceptance criteria.
4. Output artifact: markdown triage file for maintainers.

## Demo video script (<= 3 min)

1. Show repo + `duo-agent.yml`.
2. Run the command in **Quick start**.
3. Open generated `triage.md` and highlight: risk score, tests, checklist.
4. Show how this can be posted as an issue note or MR comment.

## License

This project is licensed under MIT for original work. See `LICENSE`.
