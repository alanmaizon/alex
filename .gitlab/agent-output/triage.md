## Alex SDLC Triage
**Event:** `issue.opened`
**Title:** Checkout endpoint intermittently fails under peak traffic

### Summary
- Users report random 500s on /checkout between 9:00-10:00 UTC. We recently shipped promo stacking logic.
- Scope guess: **backend**

### Risk Evaluation
- Severity: **Critical**
- Labels detected: `backend, severity::1, customer-impact`
- Customer-facing behavior is affected.
- Recent change likely introduced regression risk.
- Needs explicit test coverage before release.

### Test Strategy
- Unit: add regression test around the failing logic path.
- Integration: validate end-to-end request flow under realistic load.
- Manual: execute a smoke test in staging with representative data.
- Rollback: verify previous version or feature-flag fallback can be restored quickly.

### Release Readiness Checklist
- [ ] Acceptance criteria are explicit and measurable.
- [ ] Observability (logs/metrics/alerts) updated for this change.
- [ ] Backward compatibility validated.
- [ ] Security and privacy implications reviewed.

### Open Questions
- What is the exact reproduction path and expected result?
- Are there logs/metrics that pinpoint failing component?
- Is there a known safe rollback or feature flag?
