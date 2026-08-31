# 01 · Third-party risk

One artifact, deliberately: [the LLM provider tier](llm-provider-tier.md).

Jasper discloses twenty-plus subprocessors; four of them are frontier-model providers
carrying the flagship no-training promise and a public commitment (ISR §3.3) to annual
reassessment with audit-report review. The generic TPRM machinery lives in the
[engine](https://github.com/tiffanidickerson437-lang/compliance-program) and ports
unchanged; what is Jasper-specific is the lane where a standard SaaS questionnaire
fails — so that lane is what is designed here.

Precondition, machine-checked: the two disclosure surfaces have to agree on who is in
the tier. As of 2026-08-31 they did not — [finding F3](../05-stakeholder-management/public-claims-consistency/).
