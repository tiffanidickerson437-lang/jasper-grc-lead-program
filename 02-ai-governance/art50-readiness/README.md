# EU AI Act Article 50 — readiness assessment

The 30-day deliverable. Article 50(1)/(3)/(4) — disclosure duties for AI interaction
and synthetic content — applied on **2 August 2026**. Article 50(2) — machine-readable
marking of synthetic output — applies on **2 December 2026** for systems on the EU
market before 2 August. Jasper generates synthetic text and image at enterprise scale,
has a French entity, and serves EU customers. The May 2026 omnibus moved the high-risk
deadlines; **it did not move Article 50** ([the clock](../../00-governance/regulatory-clock.md)).

Marking cannot be fixed retroactively: it has to be in the generation pipeline before
output leaves it. That makes this the most time-boxed item available to the role, and
the reason it is scoped here rather than gestured at.

## Method

1. **Inventory every generative surface** — [`surface-inventory.yaml`](surface-inventory.yaml)
   seeds it from public product pages. Each surface records output modality and
   delivery path, because marking duty follows the output, not the brand name.
2. **Split provider duties from deployer duties, per surface.** Jasper is a provider of
   a generative system; its customers are deployers with their own Art. 50 duties.
   Which disclosures Jasper must make versus enable-and-pass-through is a per-surface
   answer, and conflating the two either over-commits Jasper or strands customers.
3. **Assess marking options against the Commission's expectations** — the May 2026
   draft guidance expects multi-layered, machine-readable marking (C2PA-class
   provenance for media; detectability measures for text). API and MCP outputs need
   the marking to survive the delivery path, which is a harder constraint than the UI.
4. **Land the plan with Product and Engineering** ahead of 2 December, with the
   evaluation evidence designed in — evidence as a byproduct of shipping, not a
   reconstruction at audit time.

## Status

The inventory below is seeded from public sources and deliberately incomplete: which
surfaces actually reach the EU market, and through which entities, is internal
knowledge. The columns are built; filling them is week one. No output of this
assessment asserts today that any Jasper surface is or is not compliant — that is the
assessment's job to determine, from inside.
