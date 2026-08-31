# 30 · 60 · 90

Sequenced around two fixed dates that are not the plan's to move: the Article 50(2)
marking date on **2 December 2026**, and the first ISO 27001 surveillance audit
(estimated ~August 2027 — [the clock](../00-governance/regulatory-clock.md) flags it
as an estimate and says why). Every task below maps to a bullet the posting itself
names, and every date derives from a published fact, so if the facts change, the plan
recomputes.

One structural advantage is stated once and then left alone: the author has worked
inside Jasper before. This plan starts at triage, not orientation — the discovery
phase assumes the stack and the owners are known quantities, not a quarter of
introductions. Nothing else in this plan draws on that history.

## Days 1–30 · Discover (triage, not tour)

| Task | Posting bullet it serves |
|---|---|
| Audit-state inventory in Vanta: SOC 2 observation-window health, evidence streams that went quiet, the ISO 27001 surveillance calendar as the certification body actually set it | "step in to rebuild and maintain momentum on audits" |
| Run the F1/F3 checkers against the live surfaces; triage findings with the Director of Security; agree claim owners | "single source of truth", SME during audits and RFPs |
| Meet the Sales and Legal owners of the questionnaire and RFP flow; **baseline questionnaire turnaround time** — the KPI this role should be judged on | "respond to customer security questionnaires" |
| Deliver the [Article 50 readiness assessment](../02-ai-governance/art50-readiness/): surfaces confirmed from inside, provider-vs-deployer split, marking options costed | "drive AI governance across the company and product" |
| Trust-center migration runbook: dead-link sweep of live RFP responses, document-vintage refresh queue (2025 CAIQ, 2025 pen-test letter), access re-grant backlog | audits, RFPs, enterprise sales engagements |

## Days 31–60 · Design

| Task | Posting bullet it serves |
|---|---|
| Stand up the single source of truth for control ownership — SCF-mapped control set rendered into the SOC 2 and ISO 27001 views Vanta already tracks; Vanta stays the system of record | "rationalize overlapping requirements" |
| Rebuild the risk register with FAIR quantification on the top ten scenarios — loss-exceedance curves, not color-coded vibes | "maintain and continuously improve the risk register … scoring" |
| Bring the [LLM provider tier](../01-tprm/llm-provider-tier.md) live against the ISR §3.3 commitment; contracts reviewed for no-training/retention terms | "vendor and third-party risk" |
| Policy lifecycle into version control with human-gated approval, honoring the ISR §1.2 annual-approval commitment | "own policy management" |
| [Model change management](../03-secure-development/model-change-management.md) agreed with Engineering as a governed change type with pre-flight checks | AI governance across the product |

## Days 61–90 · Operate

| Task | Posting bullet it serves |
|---|---|
| Automated evidence collection for the top twenty controls; drift opens tickets instead of filling trackers | "automate compliance workflows, including artifact collection … continuous monitoring" |
| Marking implementation plan landed with Product and Engineering ahead of 2 December | Article 50, on the calendar's terms |
| ISO 42001 scoping memo and certification business case to leadership — gap assessment rendered from the engine's existing 42001/AI-RMF crosswalks, competitive benchmark attached | "a path toward ISO 42001" |
| First questionnaire-turnaround number reported against the day-one baseline | the KPI, closing its first loop |
| Public-claims and subprocessor checkers scheduled against live surfaces from inside; findings route to owners automatically | continuous monitoring, applied to trust surfaces |

## What this plan refuses to do

Assert today what only the inventory can establish — which windows slipped, what the
certification body scheduled, what the questionnaire backlog looks like. A 90-day plan
that pre-announces its discoveries is a plan to confirm its own guesses.
