# Public claims consistency — findings F1 and F3

Three public Jasper surfaces describe the company's certifications in ways that do not
line up, and two of Jasper's own subprocessor disclosures diverge on the LLM tier. All
of it was observed on Jasper's published pages on **31 August 2026**; none of it needs
any knowledge of Jasper's internal posture, because none of it is about internal
posture. This is claims-consistency work, which is squarely what the Senior GRC Lead
role owns. It is framed as work to hand over, not as criticism.

## F1 — certification claims disagree across surfaces

| Surface | Asserts (as checked 2026-08-31) |
|---|---|
| [/trust](https://www.jasper.ai/trust) | "Jasper is compliant with SOC 2, PCI, DPA, CCPA, and GDPR" |
| [/security](https://www.jasper.ai/security) | "SOC 2 Compliant", "GDPR Compliant" badges; a "PCI DSS Compliant" badge |
| [Trust center](https://security.jasper.ai/) | SOC 2, ISO 27001:2022, CCPA, GDPR |

Three of the resulting six findings are the ones that matter:

1. **ISO 27001:2022 — certified 14 August 2026 — appears on no marketing surface**
   two-plus weeks later. The company's newest, hardest-won trust asset is invisible
   exactly where buyers look first.
2. **PCI is asserted by both marketing pages and absent from the trust center.**
   Whether the claim is full DSS or a payment-provider SAQ is
   [open question 2](../../00-governance/open-questions.md) — the divergence is a
   defect either way.
3. **"DPA" sits in a certifications list.** A data processing addendum is a contract
   instrument, not a credential; listing it beside SOC 2 invites a category confusion
   a diligence reviewer will notice.

Run it: `python3 check_claims.py` · rendered report:
[`claims-findings.md`](claims-findings.md) (CI fails if stale).

## F3 — subprocessor disclosures diverge on the LLM tier

The [legal sub-processors page](https://www.jasper.ai/legal/sub-processors) lists four
LLM providers (Anthropic, **Cohere**, Google Gemini, OpenAI). The trust center's
subprocessor panel surfaces three — no Cohere (both checked 2026-08-31). Against ISR
§3.3's public commitment to annual reassessment of *every* subprocessor, the two
sources of truth need to be one.

Run it: `python3 subprocessor_consistency.py`.

## What the checkers are, and are not

Both tools compare **committed observations** — dated, quoted, re-observable — and
report disagreement between Jasper's own surfaces. They never fetch a live page in CI
(a portfolio artifact whose tests depend on someone else's uptime is not a working
artifact), they never edit anything, and they never decide which surface is right.
That decision belongs to the claim owner; pointed at the live pages on a schedule from
inside, the same comparison becomes the monitor that keeps the answer true.

Both suites carry the house guarantees: a **control test** (agreeing surfaces produce
zero findings — a checker that fires on valid input gets muted, and then guards
nothing) and a **mutation guard** (gut a comparator to always-pass and its own suite
turns red).
