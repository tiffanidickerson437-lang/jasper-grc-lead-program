# The engine bridge

How [`compliance-program`](https://github.com/tiffanidickerson437-lang/compliance-program),
my controls-as-code GRC engine, maps onto this role. The engine is public; this file
exists so the connection is explicit rather than implied.

## What the engine is, in one paragraph

A compliance program that lives in git and proves itself in CI: a 45-control library
mapped to SCF 2026.1 and expressed in OSCAL (catalog, 13 framework profiles — including
ISO 42001, NIST AI RMF, and the EU AI Act — and an SSP that all pass validation), FAIR
Monte Carlo risk quantification with loss-exceedance curves, framework crosswalks whose
coverage percentages are computed rather than asserted, policy-as-code with tested
allow/deny fixtures, and a drift monitor that opens timestamped issues as due-diligence
records. AI drafts narratives and remediations; a human approves everything that
becomes record; and evidence is the hard exception: computed from systems of record,
with `ai_generated: true` rejected at the schema, hook, and CI layers.

## Posting responsibility → engine capability

| The posting asks me to | The engine already demonstrates |
|---|---|
| Rebuild and maintain momentum on audits | An audit calendar computed from certificate dates ([instantiated here](../04-evidence-and-audit/)); drift monitors that open tickets when a control goes quiet |
| SOC 2, ISO 27001 readiness through certification, path toward ISO 42001 | All three ship as OSCAL profiles over one control set today; the 42001 gap assessment is a render against a scope, not a project |
| Rationalize overlapping requirements into a single source of truth | The engine's entire thesis: one SCF-mapped control set, 13 framework views, coverage computed by a resolver |
| SME on control mapping; respond to security questionnaires | STRM crosswalks in explicit set-theory relationship form; a questionnaire linter that routes polarity and vocabulary defects to a human |
| Maintain and continuously improve the risk register | FAIR Monte Carlo with p50/p90/p95 loss exceedance, CI-tested; risk acceptance modeled as a named human decision |
| Vendor and third-party risk | TPRM pillar with attestation-reuse register and continuous monitoring; the [LLM tier](../01-tprm/llm-provider-tier.md) is the Jasper-specific lane |
| Own policy management | Policy-as-code (Rego + fixtures), human-gated approvals — matching the ISR §1.2 annual-approval commitment |
| Automate compliance workflows and artifact collection | Evidence gateways reading systems of record; schema-validated evidence; scheduled drift monitors |
| Drive AI governance across company and product | The 04-ai-governance pillar; agent-authority controls; the one hard rule (AI never authors evidence) machine-enforced |

## What gets adapted for Jasper, specifically

1. **Vanta as the gateway, not a rip-out.** The trust center and compliance tracking
   are Vanta-hosted as of 14 August 2026. The engine's gateway pattern reads from the
   system of record, validates against schema, and records — pointed at Vanta exactly
   the way it points at any other source. Git holds the control definitions; Vanta
   holds the operational state; evidence flows one way.
2. **The claims checkers move inside.** [F1 and F3](../05-stakeholder-management/public-claims-consistency/)
   run here against committed observations; run from inside on a schedule against the
   live surfaces, they become the monitor that keeps marketing, the trust center, and
   the legal pages telling one story.
3. **Model change management as CHG-02's instantiation.** LLM-agnostic routing makes
   model swap the highest-frequency compliance-relevant change at Jasper;
   [the change type is designed](../03-secure-development/model-change-management.md)
   with pre-flight checks the engine already knows how to run.
4. **The AI-governance profiles land where the product already is.** Jasper sells
   governance; the engine operates it. ISO 42001, NIST AI RMF, and EU AI Act views
   render from the same control set the SOC 2 and ISO 27001 audits consume — one
   posture, every audience.

## The short version

The engine proves the method in public, and this repo aims that method at one company's
actual calendar, obligations, and surfaces. Two prior instances —
[Mattermost](https://github.com/tiffanidickerson437-lang/mattermost-grc-manager-program)
and [Plaid](https://github.com/tiffanidickerson437-lang/plaid-grc-engineering-program) —
show the portability: adding a company is a config file, and adding a framework is a
mapping, not a project.
