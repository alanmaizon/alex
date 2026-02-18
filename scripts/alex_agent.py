#!/usr/bin/env python3
"""Alex SDLC Copilot triage runner.

Consumes a GitLab event payload and writes a deterministic markdown triage report.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SEVERITY_ORDER = ["Low", "Medium", "High", "Critical"]


def infer_scope(labels: list[str], text: str) -> str:
    lowered = " ".join(labels).lower() + " " + text.lower()
    if any(k in lowered for k in ["frontend", "ui", "ux", "css"]):
        return "frontend"
    if any(k in lowered for k in ["infra", "k8s", "terraform", "deploy", "ops"]):
        return "infra"
    if any(k in lowered for k in ["security", "vuln", "auth", "privacy"]):
        return "security"
    if any(k in lowered for k in ["data", "etl", "db", "sql"]):
        return "data"
    return "backend"


def infer_severity(labels: list[str], text: str) -> str:
    lowered = " ".join(labels).lower() + " " + text.lower()
    if any(k in lowered for k in ["severity::1", "critical", "outage", "breach"]):
        return "Critical"
    if any(k in lowered for k in ["severity::2", "500", "customer-impact", "payment"]):
        return "High"
    if any(k in lowered for k in ["severity::3", "degraded", "slow", "latency"]):
        return "Medium"
    return "Low"


def build_report(payload: dict) -> str:
    title = payload.get("title", "Untitled event")
    description = payload.get("description", "No description provided.")
    labels = payload.get("labels", [])
    scope = infer_scope(labels, f"{title} {description}")
    severity = infer_severity(labels, f"{title} {description}")

    reasons = [
        "Customer-facing behavior is affected.",
        "Recent change likely introduced regression risk.",
        "Needs explicit test coverage before release.",
    ]

    questions = [
        "What is the exact reproduction path and expected result?",
        "Are there logs/metrics that pinpoint failing component?",
        "Is there a known safe rollback or feature flag?",
    ]

    label_text = ", ".join(labels) if labels else "none"

    lines = [
        "## Alex SDLC Triage",
        f"**Event:** `{payload.get('type', 'unknown')}`",
        f"**Title:** {title}",
        "",
        "### Summary",
        f"- {description}",
        f"- Scope guess: **{scope}**",
        "",
        "### Risk Evaluation",
        f"- Severity: **{severity}**",
        f"- Labels detected: `{label_text}`",
    ]

    lines.extend(f"- {reason}" for reason in reasons)

    lines.extend(
        [
            "",
            "### Test Strategy",
            "- Unit: add regression test around the failing logic path.",
            "- Integration: validate end-to-end request flow under realistic load.",
            "- Manual: execute a smoke test in staging with representative data.",
            "- Rollback: verify previous version or feature-flag fallback can be restored quickly.",
            "",
            "### Release Readiness Checklist",
            "- [ ] Acceptance criteria are explicit and measurable.",
            "- [ ] Observability (logs/metrics/alerts) updated for this change.",
            "- [ ] Backward compatibility validated.",
            "- [ ] Security and privacy implications reviewed.",
            "",
            "### Open Questions",
        ]
    )

    lines.extend(f"- {question}" for question in questions)

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Alex SDLC triage markdown")
    parser.add_argument("--event-file", required=True, help="Path to incoming event JSON")
    parser.add_argument("--output", required=True, help="Path to output markdown")
    args = parser.parse_args()

    with open(args.event_file, "r", encoding="utf-8") as f:
        payload = json.load(f)

    report = build_report(payload)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
