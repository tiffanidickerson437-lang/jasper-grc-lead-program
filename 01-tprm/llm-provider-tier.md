# The LLM provider tier

Jasper's public sub-processors page discloses four frontier-model providers — Anthropic,
Cohere, Google Gemini, OpenAI — each carrying the purpose "LLM (option agentic
features)" (checked 2026-08-31). §3.3 of the public Information Security Requirements
commits Jasper to **annual reassessment of every subprocessor, including audit and
penetration-test report review**. And the flagship trust-page promise — *"your data is
never used to train third-party LLMs"* — rides entirely on this tier.

A frontier lab does not fit the standard SaaS vendor questionnaire, and pretending it
does produces an annual checkbox over the company's single largest third-party risk
surface. This tier gets its own lane.

## What the lane assesses, per provider, per year

| Assessment item | Why it is tier-specific |
|---|---|
| **No-training / zero-retention contractual terms** | The public promise must be evidenced contract by contract, not asserted. A provider default is not a term; an addendum is |
| **Model-deprecation notice SLA** | Providers retire snapshots on their own calendar. Routing built on a retired model is an availability and evaluation-evidence event, not just an engineering one |
| **Subprocessor-of-subprocessor disclosure** | Where does the provider run, and on whose cloud — the answer flows into Jasper's own DPA notice duties |
| **Audit report review** (SOC 2 / ISO) | Required verbatim by ISR §3.3; the reports exist for all four named providers |
| **Regional processing and data-residency options** | Feeds the EU posture question (open question 7) and enterprise EU deals |
| **Incident-notification terms** | §3.5 breach-notification commitments are only meetable if the provider's clock is shorter than Jasper's |

## The consistency precondition

Before the lane can run, the disclosure surfaces have to agree on who is in it. As
observed on 2026-08-31 they did not: the legal page lists four LLM providers; the trust
center panel surfaces three (no Cohere). That divergence is
[finding F3, machine-checked](../05-stakeholder-management/public-claims-consistency/) —
and it is a one-line fix once someone inside decides which list is right.

## What this file is not

Not an assessment of any provider, and not a claim about what Jasper's contracts
contain — both sit behind NDAs. This is the lane design, ready to run the day the
contracts are on the desk.
