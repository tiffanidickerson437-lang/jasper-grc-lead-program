# Public claims — findings (F1)

Rendered by `check_claims.py --render` from [`claims-inventory.yaml`](claims-inventory.yaml). Do not edit by hand — re-run the tool.

Observations dated per surface; the inventory records what each page said when checked, with quotes. Findings describe disagreement between surfaces, never Jasper's actual posture.

## Surfaces compared

| Surface | Audience | Checked | Asserts |
|---|---|---|---|
| [trust-page](https://www.jasper.ai/trust) | marketing | 2026-08-31 | CCPA, DPA, GDPR, PCI DSS, SOC 2 |
| [security-page](https://www.jasper.ai/security) | marketing | 2026-08-31 | GDPR, PCI DSS, SOC 2 |
| [trust-center](https://security.jasper.ai/) | assurance | 2026-08-31 | CCPA, GDPR, ISO/IEC 27001:2022, SOC 2 |

## Findings

| # | Type | Claim | Detail |
|---|---|---|---|
| 1 | DIVERGENT | ccpa | CCPA asserted on trust-center, trust-page but absent from security-page |
| 2 | DIVERGENT | dpa | DPA asserted on trust-page but absent from security-page, trust-center |
| 3 | CATEGORY | dpa | DPA is a contract instrument, listed alongside certifications on trust-page |
| 4 | DIVERGENT | iso27001 | ISO/IEC 27001:2022 asserted on trust-center but absent from security-page, trust-page |
| 5 | MARKETING_GAP | iso27001 | ISO/IEC 27001:2022 appears on the assurance surface and on no marketing surface |
| 6 | DIVERGENT | pci | PCI DSS asserted on security-page, trust-page but absent from trust-center |

The fix for every row is a decision by the claim owner, then a monitor — never a silent edit by a checker.
