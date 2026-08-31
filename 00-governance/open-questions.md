# Open questions

Everything in the findings and deliverables rests on public sources. These are the
questions the public record cannot answer. Each one states what is visible from outside
and where the public trail ends, so the boundary between observed fact and internal
knowledge stays explicit. None of them is an assumption dressed as a finding; they are
the things a first conversation with the team would settle.

A note this repository owes the reader: the author previously worked at Jasper. Some of
these questions may have had answers then. They are listed as open anyway, because a
stale answer asserted as current is worse than a question — and because nothing learned
inside Jasper is used anywhere in this repository.

---

## 1. Which SOC 2 observation period is running right now, and what has slipped?

**Public record:** the trust center catalogs "Jasper AI - SOC2 Type2.pdf". The posting
says the hire will "step in to rebuild and maintain momentum on audits."

**Unresolvable from outside:** the report period, the auditor, what the current
observation window looks like after an ownership gap, and which evidence streams went
quiet. "Momentum" cannot be maintained before it is measured, which is why the audit-state
inventory is the first 30-day task.

## 2. What is the PCI claim's actual scope?

**Public record:** `/trust` says "compliant with SOC 2, PCI, DPA, CCPA, and GDPR";
`/security` shows a "PCI DSS Compliant" badge; the trust center's compliance list omits
PCI entirely (all checked 2026-08-31). Stripe appears on the sub-processors page.

**Unresolvable from outside:** whether this is full PCI DSS, a payment-provider SAQ, or
a claim that outlived its scope. The divergence itself is finding F1 either way; the
right fix depends on the answer.

## 3. Is ISO 42001 a certification target with a date, or a positioning statement?

**Public record:** the posting says "with a path toward ISO 42001." No public AIMS
artifacts exist. The closest enterprise competitor is certified, on the same compliance
platform Jasper migrated to on 14 August 2026.

**Unresolvable from outside:** whether leadership has scoped, budgeted, or calendared
it. The gap assessment renders from existing crosswalks either way; the business case
changes shape depending on the answer.

## 4. What did the SafeBase → Vanta migration leave behind?

**Public record:** the migration notice (14 August 2026) says all prior access must be
re-requested. Resource vintages on the new trust center are mixed: a 2025 CAIQ and 2025
pen-test letter beside 2026 SIG Core, data-flow, and network-architecture documents.

**Unresolvable from outside:** how many live RFP responses and customer bookmarks point
at dead SafeBase links, which documents are queued for refresh, and who owns the
re-grant backlog.

## 5. Who owns questionnaire answers today, and what is the turnaround?

**Public record:** the posting makes this seat the SME "during customer and external
audits, RFPs, and enterprise sales engagements."

**Unresolvable from outside:** the current owner, the tooling, the answer library's
state, and the baseline turnaround time — the KPI this role should be judged on.

## 6. How are model-routing changes reviewed before they ship?

**Public record:** `/llm-optimized` says tasks route "to the best-performing model for
the job" and that Jasper is "constantly integrating new models." Four LLM subprocessors
are disclosed. The no-training commitment is flagship marketing.

**Unresolvable from outside:** whether a model swap is a governed change type — who
approves, what subprocessor-notice and contract checks run, and what evaluation evidence
is kept. See [model change management](../03-secure-development/model-change-management.md).

## 7. What is the EU hosting and data-residency posture?

**Public record:** a French entity exists via the Clipdrop acquisition; EU customers are
served; the DPA ships SCCs. A third-party profile describes US data centers — a claim
this repository treats as unverified.

**Unresolvable from outside:** whether any EU processing or residency option exists or
is planned, and how that shapes Art. 50 provider-versus-deployer analysis and enterprise
EU deals.

## 8. Does any AI-assisted screening touch the hiring pipeline?

**Public record:** the CCPA Notice to Candidates is v1.0, effective March 2024 —
written before the CPPA's ADMT regulations reached hiring workflows. Applications run
through Ashby.

**Unresolvable from outside:** whether any automated decision-making applies to
candidates, which decides whether the notice needs an ADMT refresh. A question for
Legal, with the applicability memo drafted to support it — the posting is explicit that
this seat supports privacy "without owning the legal interpretation."
