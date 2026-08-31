# The audit calendar

Rendered by `audit_clock.py --render` from [`regulatory-dates.yaml`](../data/regulatory-dates.yaml). Do not edit by hand — re-run the tool.

Fixed dates only, so this file is stable and CI can prove it is not stale. For live day counts, run `python3 audit_clock.py`.

| Date | Kind | What | Source |
|---|---|---|---|
| 2026-01-01 | applied | Texas TRAIGA in force (Jasper's founding state) | [source](https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=HB149) |
| 2026-05-07 | applied | EU digital-omnibus grandfathering — high-risk AI Act deadlines moved to Dec 2027 / Aug 2028; Art. 50 unmoved | [source](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) |
| 2026-08-02 | applied | EU AI Act Art. 50(1)/(3)/(4) — AI-interaction and synthetic-content disclosure duties apply | [source](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) |
| 2026-08-14 | applied | Jasper ISO/IEC 27001:2022 certification announced on the trust center | [source](https://security.jasper.ai/) |
| 2026-08-14 | applied | Trust center migrated SafeBase -> Vanta; all prior customer access must be re-requested | [source](https://security.jasper.ai/) |
| 2026-12-02 | deadline | EU AI Act Art. 50(2) — machine-readable marking of synthetic content applies (systems on the EU market before 2026-08-02) | [source](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) |
| 2027-01-01 | deadline | Colorado AI Act effective (as amended and delayed by SB 189, signed 2026-05-14) | [source](https://www.hunton.com/privacy-and-cybersecurity-law-blog/colorado-ai-act-amended-and-effective-date-delayed) |
| 2027-01-01 | deadline | CPPA automated decision-making technology obligations begin phasing in | [source](https://cppa.ca.gov/regulations/) |
| 2027-08-14 | ESTIMATE | First ISO 27001 surveillance audit window (ESTIMATE: certification date + 12 months) | [source](https://security.jasper.ai/) |

Every estimate row states its derivation in the data file and is never cited as a hard date.
