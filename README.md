# Jasper's Senior GRC Lead Program, as Code

**Describes Jasper in one config file, aims a working GRC engine at Jasper's actual
calendar and public surfaces, and ships seven findings observed on Jasper's own pages —
two of them machine-checked by instruments in this repository, with tests that attack
their own checkers.**

[![tests](https://github.com/tiffanidickerson437-lang/jasper-grc-lead-program/actions/workflows/tests.yml/badge.svg)](../../actions/workflows/tests.yml)
[![sources](https://img.shields.io/badge/sources-public%20only%20%C2%B7%20checked%2031%20Aug%202026-1b1d22)](00-governance/public-surface-map.md)
[![engine](https://img.shields.io/badge/engine-compliance--program-2b5cff)](https://github.com/tiffanidickerson437-lang/compliance-program)
[![evidence](https://img.shields.io/badge/evidence__in__repo-none-6b7280)](#ground-rules)

**▶ [The walkthrough](https://tiffanidickerson437-lang.github.io/jasper-fd6543/)** — the
same argument in one page, matched to the posting line by line and addressed to the
hiring manager.

## Run it — 30 seconds, no key, no network

```bash
git clone https://github.com/tiffanidickerson437-lang/jasper-grc-lead-program
cd jasper-grc-lead-program && pip install pyyaml

python3 05-stakeholder-management/public-claims-consistency/check_claims.py
python3 05-stakeholder-management/public-claims-consistency/subprocessor_consistency.py
python3 04-evidence-and-audit/data/audit_clock.py
```

```
Public claims consistency — 3 surfaces compared
  [DIVERGENT]     PCI DSS asserted on security-page, trust-page but absent from trust-center
  [MARKETING_GAP] ISO/IEC 27001:2022 appears on the assurance surface and on no marketing surface
  [CATEGORY]      DPA is a contract instrument, listed alongside certifications on trust-page
  ...
6 finding(s). Each routes to the claim owner — nothing here edits a page.
```

Then attack the checkers themselves — 42 tests across three suites. Every checker
carries a **control test** (clean input must produce zero findings) and a **mutation
guard** (gut a comparator to always-pass and its own suite turns red). Same inputs,
same output, every run. No model in the pass/fail path.

---

This is how I'd start the Senior GRC Lead role, built entirely from what Jasper already
publishes. Jasper sells governance — a Governance product page, an AI policy template
for customers, trust in the top nav. The posting is candid that internally the work is
to "rebuild and maintain momentum." The distance between governance sold and governance
operated is the role — so this repository is the operated version, not a document about
one.

### The short version, in four lines

- **Three of Jasper's own surfaces give three different certification answers**, and
  the ISO 27001 certification announced 14 August 2026 appears on none of the marketing
  pages. [Machine-checked (F1).](05-stakeholder-management/public-claims-consistency/)
- **Two of Jasper's own subprocessor disclosures diverge on the LLM tier** — the tier
  the no-training promise rides on, under a public annual-reassessment commitment.
  [Machine-checked (F3).](05-stakeholder-management/public-claims-consistency/)
- **Article 50 is live and the marking date lands 2 December 2026.** The omnibus moved
  the high-risk deadlines and not this one. [The clock is computed, with estimates
  flagged at the schema level.](04-evidence-and-audit/)
- **Model routing is Jasper's least-named control surface.** Continuous model swaps
  touch the no-training promise, subprocessor notices, eval evidence, and contract reps
  at once. [The change type is designed.](03-secure-development/model-change-management.md)

## The findings

| # | Finding | Where |
|---|---|---|
| F1 | Certification claims disagree across /trust, /security, and the trust center; ISO 27001 missing from marketing | [checker + report](05-stakeholder-management/public-claims-consistency/) |
| F2 | Trust-center migration debt: mixed document vintages (2025 CAIQ, 2025 pen-test letter beside 2026 SIG/diagrams); all customer access reset 14 Aug 2026 | [runbook slot, days 1–30](30-60-90/) |
| F3 | Subprocessor disclosures diverge on the LLM tier (Cohere on the legal page, absent from the trust-center panel) against ISR §3.3 | [checker](05-stakeholder-management/public-claims-consistency/) |
| F4 | No public marking/provenance statement for generative output, 93 days from Art. 50(2) at time of writing | [readiness assessment](02-ai-governance/art50-readiness/) |
| F5 | Candidate-facing CCPA notice is v1.0 (March 2024), predating the CPPA's ADMT rulemaking | [open question 8](00-governance/open-questions.md) |
| F6 | July 2025 fair-use post makes auditable public promises with no visible promise→control→evidence mapping | [surface map](00-governance/public-surface-map.md) |
| F7 | ISO 42001 named as "a path" with no public AIMS artifacts; the closest competitor is certified on the same platform Jasper just adopted | [engine bridge](generated/engine-bridge.md) |

## The pillars

| | Pillar | What is in it |
|---|---|---|
| 00 | [Governance](00-governance/) | Surface map, open questions, the regulatory clock — the research position, auditable |
| 01 | [TPRM](01-tprm/) | The LLM provider tier: where a standard SaaS questionnaire fails |
| 02 | [AI governance](02-ai-governance/) | Article 50 readiness, scoped; the sold-vs-operated gap |
| 03 | [Secure development](03-secure-development/) | Model change management as a governed change type |
| 04 | [Evidence & audit](04-evidence-and-audit/) | The audit clock: dates as validated data, calendar rendered, `evidence_in_repo: none` |
| 05 | [Stakeholder management](05-stakeholder-management/) | F1 + F3 checkers; claims hygiene as a revenue control |
| — | [30 · 60 · 90](30-60-90/) | Task-level, mapped to the posting's own bullets, sequenced by the calendar |
| — | [The config](generated/companies/jasper/jasper.config.yaml) | One file, every value marked verified / named-in-posting / inferred / deliberately unset |
| — | [Engine bridge](generated/engine-bridge.md) | How the [engine](https://github.com/tiffanidickerson437-lang/compliance-program) maps onto the role, and what gets adapted |

## Ground rules

1. **Public sources only** — every claim traces to the
   [surface map](00-governance/public-surface-map.md) with a check date. The author is
   a former Jasper employee, disclosed [in the config](generated/companies/jasper/jasper.config.yaml)
   precisely because **no non-public information from that employment is used anywhere
   in this repository.**
2. **Gaps are the work, never the criticism.**
3. **Evidence is computed, never authored.** `evidence_in_repo: none` — the instruments
   run against committed, dated observations of public surfaces, and no output should
   be read as if they touched a Jasper system.
4. **Live pages change without notice.** A finding that was true in August and asserted
   in September is not a finding; the checkers exist so the observation can be re-run,
   not remembered.

Prior instances of the same method:
[mattermost-grc-manager-program](https://github.com/tiffanidickerson437-lang/mattermost-grc-manager-program) ·
[plaid-grc-engineering-program](https://github.com/tiffanidickerson437-lang/plaid-grc-engineering-program)

---

Not affiliated with, endorsed by, or sponsored by Jasper AI, Inc. No Jasper trademark
or logo is used. This is a candidate's independent work product. See
[`docs/deliverables.md`](docs/deliverables.md) for the deliverables index and
[`SECURITY.md`](SECURITY.md) for the security policy.
