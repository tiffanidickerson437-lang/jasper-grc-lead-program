# Model change management — the control surface nobody has named

Jasper's public differentiation is LLM-agnostic routing: each task goes "to the
best-performing model for the job," across four disclosed providers, "constantly
integrating new models" ([/llm-optimized](https://www.jasper.ai/llm-optimized), checked
2026-08-31). That is a genuine product strength — and it means the model layer changes
continuously, in production, as a matter of design.

Every one of those changes touches four compliance commitments at once:

| A model swap touches | Because |
|---|---|
| **The no-training promise** | "Your data is never used to train third-party LLMs" must hold for the *new* provider and the *new* terms, before traffic moves |
| **Subprocessor disclosure and notice duties** | The DPA and the sub-processor advisory promise notice of changes; a new provider or endpoint is a change |
| **Evaluation evidence** | Enterprise customers buy routing on the claim it picks the *best-performing* model; the evidence for that claim has a shelf life of exactly one swap |
| **Customer contract representations** | Security exhibits and questionnaires answered under the old provider set do not answer themselves under the new one |

## The control, stated as a change type

Treat a production model-routing change as a **governed change type** — the same move
mature shops made for infrastructure changes a decade ago:

1. **Trigger:** any change to the provider set, model version pinning, or routing
   policy serving customer traffic.
2. **Pre-flight checks (deterministic, blocking):** provider present on both disclosure
   surfaces (the [F3 checker](../05-stakeholder-management/public-claims-consistency/)
   is this check, pointed forward); no-training/retention terms confirmed current for
   the target model; notice obligations evaluated (does this swap trip the DPA's
   subprocessor-notice clock?).
3. **Evidence as a byproduct:** the routing change record itself — what moved, when,
   why, approved by whom, with the eval delta attached — becomes the audit artifact.
   Nothing is reconstructed later, because nothing needs to be.
4. **Human gate:** a person approves the change; the checks brief the person. Code
   decides pass/fail on the checkable parts; it never signs.

## Why this file exists in a public repo

None of this asserts how Jasper handles model changes today — that is not public, and
open question 6 asks it directly. What this file shows is that the control is designed
and cheap: the pre-flight checks are the same class of instrument already running in
this repository against public surfaces, moved inside the pipeline where they belong.
