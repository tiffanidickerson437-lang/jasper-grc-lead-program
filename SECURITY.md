# Security policy

This repository ships compliance tooling. A defect in a checker here is not a normal
bug — a validator that silently stops validating reports "clean" forever after, and
anyone relying on it inherits that silence. Please report problems rather than filing
them as feature requests.

## Reporting a vulnerability

**Use GitHub's private vulnerability reporting** — the *Report a vulnerability* button
under the repository's Security tab. That opens a private advisory only maintainers can
see.

Please do not open a public issue for a security defect until it has been fixed.

If private reporting is unavailable to you, email **tiffanidickerson437@gmail.com**
with `SECURITY` in the subject line.

**What to expect:** an acknowledgement within 5 business days, an assessment within 10,
and credit in the advisory unless you ask otherwise. This is a personal project, not a
funded program — these are best-effort targets, stated as such rather than dressed up
as an SLA.

## What counts as a security issue here

Beyond the usual, these are specifically in scope because of what this repository is:

| Class | Why it matters |
|---|---|
| **A checker that passes invalid input** | The repository's claim rests on the checkers failing closed. A false negative is the highest-severity defect class here. |
| **A checker that can be neutered without turning its own suite red** | Every checker carries a mutation guard for exactly this reason. A gap in that guard is a real finding. |
| **A path where an observation can drift without its date changing** | The inventories record what a page said, when. Any route to editing an observation while keeping its `checked` date is a data-integrity defect. |
| **An estimate presented as a published date** | `regulatory-dates.yaml` flags estimates at the schema level and the validator enforces it. A bypass turns derived planning dates into citable "facts". |
| **Dependency or workflow supply-chain issues** | Actions are pinned to full commit SHAs; a tag-based reference slipping in is a finding. |

## What is out of scope

- **Anything about Jasper's actual security posture.** This repository contains no
  Jasper evidence, no credentials, and no non-public information — the author is a
  former Jasper employee and that boundary is load-bearing, documented, and deliberate.
  If you believe something here discloses non-public Jasper information, that is very
  much in scope: report it and it will be removed immediately.
- Findings in the upstream engine, which has its own policy.
- Whether Jasper's public pages *should* say what they say — the checkers report
  disagreement between surfaces; the claims belong to Jasper.

## Hardening in place

- Every GitHub Action pinned to a full commit SHA, never a mutable tag
- Workflow `permissions:` scoped to `contents: read`, and repository default workflow
  permissions set to read with workflow PR-approval disabled
- No workflow step may swallow a failure — no `|| true`, no `continue-on-error`
- Dependabot alerts, automated security fixes, and weekly version updates enabled
- Private vulnerability reporting enabled
- Secret scanning with push protection enabled
- Merge surface reduced to squash-only with automatic branch deletion; wiki and
  projects disabled
- `main` protected: the `test` status check is required and strict, force-push and
  deletion are blocked, conversation resolution is required, and the rules apply to
  administrators too — which means every change to `main`, including the maintainer's
  own, arrives by pull request with green CI
- CodeQL code scanning via GitHub's default setup
- Data files consumed by the checkers are validated fail-closed before comparison:
  schema version, ISO dates, https-only source and surface URLs, slug-constrained ids
- One runtime dependency, pinned
