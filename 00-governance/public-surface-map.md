# The public surface map

Every Jasper surface this repository draws from, what it asserts, and when it was
checked. This is the source-of-truth register for the whole repo: if a claim in any
file here cannot be traced to a row on this page, that claim is a defect.

Two check states:

- **FETCHED** — retrieved directly on the date shown (HTTP, or a browser session for
  client-rendered pages), with the relevant text preserved in the instruments' data files
- **RECORDED** — read and quoted on the date shown during research; not re-fetched into
  a committed fixture

| Surface | What it asserts (relevant here) | State | Checked |
|---|---|---|---|
| [/trust](https://www.jasper.ai/trust) | "Jasper is compliant with SOC 2, PCI, DPA, CCPA, and GDPR"; "your data is never used to train third-party LLMs" | FETCHED | 2026-08-31 |
| [/security](https://www.jasper.ai/security) | "SOC 2 Compliant", "GDPR Compliant" badges; "PCI DSS Compliant" badge; SSO/SCIM; Transcend-powered privacy; "limited customer PII (name and email)" by default | FETCHED | 2026-08-31 |
| [Trust center](https://security.jasper.ai/) (Vanta-hosted) | Compliance: SOC 2, ISO 27001:2022, CCPA, GDPR. Subprocessor panel: GCP, OpenAI, Google Gemini, Anthropic. Resources: 2025 CAIQ, 2025 pen-test letter, 26–27 COI, 2026 SIG Core, 2026 diagrams, SOC 2 Type II report, whitepapers. Migration notice dated 2026-08-14 | FETCHED (browser) | 2026-08-31 |
| [/legal/sub-processors](https://www.jasper.ai/legal/sub-processors) | LLM tier: Anthropic, Cohere, Google Gemini, OpenAI ("LLM (option agentic features)"). Also GCP, Datadog, Splunk, Transcend, Stripe, Google Workspace, others | FETCHED | 2026-08-31 |
| [/legal/security-requirements](https://www.jasper.ai/legal/security-requirements) (ISR exhibit) | §1.2 Director of Security approves policies annually; §3.3 annual reassessment of every subprocessor incl. audit/pen-test report review; §3.5 breach-notification content | RECORDED | 2026-08-31 |
| [/legal/ccpa](https://www.jasper.ai/legal/ccpa) | CCPA Notice to Candidates, v1.0, effective March 2024 | RECORDED | 2026-08-31 |
| [/llm-optimized](https://www.jasper.ai/llm-optimized) | Tasks route "to the best-performing model for the job"; "constantly integrating new models" | RECORDED | 2026-08-31 |
| [/governance](https://www.jasper.ai/governance) | Governance as a product surface: roles/permissions, usage analytics, API token control | RECORDED | 2026-08-31 |
| [Fair-use blog post](https://www.jasper.ai/blog/legal-rulings-ai-fair-use) (July 2025) | Public commitments: contractual IP protection and indemnities; "built-in safety … audit logs that block verbatim copying"; "continuous security, privacy, and compliance oversight — SOC 2 or ISO 27001" | RECORDED | 2026-08-31 |
| [Senior GRC Lead posting](https://jobs.ashbyhq.com/Jasper%20AI/d86a7821-b768-4f11-b540-3ee0fbc94c96) (Ashby) | The role: rebuild audit momentum; SOC 2 / ISO 27001 / path toward ISO 42001; rationalize overlapping requirements; questionnaires; risk register; vendor risk; policy management; automation; AI governance; GCP; Vanta/Drata/OneTrust familiarity | RECORDED | 2026-08-31 |

Ground rules, stated once and enforced everywhere:

1. **Public sources only.** No claim in this repository rests on anything else —
   including anything the author learned as a Jasper employee.
2. **Gaps are the work, never the criticism.** Every finding is framed as work to hand
   over, because that is what it is.
3. **Evidence is computed, never authored.** `evidence_in_repo: none` is load-bearing;
   the instruments run against committed observations of public surfaces, and no output
   should be read as if they touched a Jasper system.
4. **Live pages change without notice.** Every observation carries its date; the fix
   for a changed page is a re-observation, never a quiet edit.
