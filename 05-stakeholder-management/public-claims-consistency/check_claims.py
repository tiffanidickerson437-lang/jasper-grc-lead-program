#!/usr/bin/env python3
"""Public claims consistency checker (finding F1).

Compares what Jasper's public surfaces assert about certifications and compliance,
as recorded in claims-inventory.yaml, and reports every place the surfaces disagree.
It never decides what Jasper actually holds — that is a question for the claim owner,
not a set comparison. It routes a human; it does not gate a deploy.

Three defect classes, each of which was live on 2026-08-31:

  DIVERGENT     a claim asserted on at least one surface and absent from at least one
                other (PCI: on both marketing pages, absent from the trust center)
  MARKETING_GAP a claim the assurance surface carries that no marketing surface does
                (ISO 27001:2022 — certified 14 August 2026, invisible on jasper.ai)
  CATEGORY      a non-certification listed as if it were one ("DPA" in a compliance
                list is a contract instrument wearing a credential's clothes)

Usage:
  python3 check_claims.py             # report findings, exit 0 (routes a human)
  python3 check_claims.py --strict    # exit 2 when there are findings (for CI gating)
  python3 check_claims.py --check     # validate the inventory only; exit 1 on invalid
  python3 check_claims.py --render    # rewrite claims-findings.md from the inventory
  python3 check_claims.py --inventory PATH   # run against a different inventory

Exit codes: 0 clean/reported · 1 invalid inventory · 2 findings under --strict.
No network call, no API key, no model in any code path.
"""

import argparse
import datetime as _dt
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INVENTORY = os.path.join(HERE, "claims-inventory.yaml")
REPORT = os.path.join(HERE, "claims-findings.md")

VALID_KINDS = {"certification", "law", "contract-instrument"}


class InventoryError(ValueError):
    """The inventory is malformed. A checker that guesses past bad input is a
    checker whose findings cannot be trusted, so this always stops the run."""


def load_inventory(path):
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    validate_inventory(data)
    return data


def validate_inventory(data):
    if not isinstance(data, dict):
        raise InventoryError("inventory root must be a mapping")
    if data.get("schema_version") != 1:
        raise InventoryError("schema_version must be 1")

    aliases = data.get("aliases") or {}
    claims = data.get("claims")
    if not isinstance(claims, dict) or not claims:
        raise InventoryError("claims registry missing or empty")
    for cid, meta in claims.items():
        if not isinstance(meta, dict):
            raise InventoryError("claim %r: metadata must be a mapping" % cid)
        if meta.get("kind") not in VALID_KINDS:
            raise InventoryError("claim %r: kind must be one of %s"
                                 % (cid, sorted(VALID_KINDS)))
        if not isinstance(meta.get("label"), str) or not meta["label"].strip():
            raise InventoryError("claim %r: label missing" % cid)
    for alias, target in aliases.items():
        if target not in claims:
            raise InventoryError("alias %r points at unknown claim %r" % (alias, target))

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, list) or len(surfaces) < 2:
        raise InventoryError("need at least two surfaces to compare")
    seen_ids = set()
    for s in surfaces:
        if not isinstance(s, dict):
            raise InventoryError("surface entries must be mappings")
        for field in ("id", "url", "audience", "checked", "quote", "claims"):
            if not s.get(field):
                raise InventoryError("surface %r: %s missing"
                                     % (s.get("id", "?"), field))
        if not re.fullmatch(r"[a-z0-9-]+", str(s["id"])):
            raise InventoryError("surface id %r must be a lowercase slug — ids land "
                                 "verbatim in rendered markdown" % s["id"])
        if not str(s["url"]).startswith("https://"):
            raise InventoryError("surface %r: url must be https:// — an observation "
                                 "of a non-TLS page is not the observation this "
                                 "inventory claims, and the url lands in a rendered "
                                 "markdown link" % s["id"])
        if s["id"] in seen_ids:
            raise InventoryError("duplicate surface id %r" % s["id"])
        seen_ids.add(s["id"])
        if s["audience"] not in ("marketing", "assurance"):
            raise InventoryError("surface %r: audience must be marketing|assurance"
                                 % s["id"])
        try:
            _dt.date.fromisoformat(str(s["checked"]))
        except ValueError:
            raise InventoryError("surface %r: checked is not an ISO date" % s["id"])
        if not isinstance(s["claims"], list) or not s["claims"]:
            raise InventoryError("surface %r: claims must be a non-empty list" % s["id"])
        for token in s["claims"]:
            # bool is an int subclass and YAML turns bare `on`/`yes` into booleans;
            # a claim list is only ever strings, so anything else is a data defect.
            if not isinstance(token, str):
                raise InventoryError("surface %r: claim token %r is not a string"
                                     % (s["id"], token))
            if canonical(token, data) is None:
                raise InventoryError("surface %r: unknown claim token %r "
                                     "(add it to claims or aliases)" % (s["id"], token))


def canonical(token, data):
    """Resolve a surface's claim token to its canonical id, or None if unknown."""
    token = token.strip().lower()
    aliases = {str(k).lower(): v for k, v in (data.get("aliases") or {}).items()}
    if token in aliases:
        return aliases[token]
    if token in data["claims"]:
        return token
    return None


def find(data):
    """Return the list of findings. Deterministic: same inventory, same output."""
    surfaces = data["surfaces"]
    findings = []

    asserted = {}  # canonical claim -> set of surface ids
    for s in surfaces:
        for token in s["claims"]:
            asserted.setdefault(canonical(token, data), set()).add(s["id"])

    all_ids = [s["id"] for s in surfaces]
    marketing = [s["id"] for s in surfaces if s["audience"] == "marketing"]
    assurance = [s["id"] for s in surfaces if s["audience"] == "assurance"]

    for claim in sorted(asserted):
        meta = data["claims"][claim]
        present = asserted[claim]
        absent = [i for i in all_ids if i not in present]

        if absent:
            findings.append({
                "type": "DIVERGENT",
                "claim": claim,
                "detail": "%s asserted on %s but absent from %s"
                          % (meta["label"],
                             ", ".join(sorted(present)),
                             ", ".join(sorted(absent))),
            })

        if meta["kind"] == "contract-instrument":
            findings.append({
                "type": "CATEGORY",
                "claim": claim,
                "detail": "%s is a contract instrument, listed alongside "
                          "certifications on %s"
                          % (meta["label"], ", ".join(sorted(present))),
            })

        if (meta["kind"] == "certification"
                and any(i in present for i in assurance)
                and not any(i in present for i in marketing)):
            findings.append({
                "type": "MARKETING_GAP",
                "claim": claim,
                "detail": "%s appears on the assurance surface and on no "
                          "marketing surface" % meta["label"],
            })

    return findings


def render_report(data, findings):
    lines = [
        "# Public claims — findings (F1)",
        "",
        "Rendered by `check_claims.py --render` from"
        " [`claims-inventory.yaml`](claims-inventory.yaml)."
        " Do not edit by hand — re-run the tool.",
        "",
        "Observations dated per surface; the inventory records what each page said"
        " when checked, with quotes. Findings describe disagreement between surfaces,"
        " never Jasper's actual posture.",
        "",
        "## Surfaces compared",
        "",
        "| Surface | Audience | Checked | Asserts |",
        "|---|---|---|---|",
    ]
    for s in data["surfaces"]:
        tokens = sorted({canonical(t, data) for t in s["claims"]})
        labels = ", ".join(data["claims"][t]["label"] for t in tokens)
        lines.append("| [%s](%s) | %s | %s | %s |"
                     % (s["id"], s["url"], s["audience"], s["checked"], labels))
    lines += ["", "## Findings", ""]
    if not findings:
        lines.append("None. Every surface asserts the same set, in the right category.")
    else:
        lines.append("| # | Type | Claim | Detail |")
        lines.append("|---|---|---|---|")
        for n, f in enumerate(findings, 1):
            lines.append("| %d | %s | %s | %s |"
                         % (n, f["type"], f["claim"], f["detail"]))
    lines += [
        "",
        "The fix for every row is a decision by the claim owner, then a monitor —"
        " never a silent edit by a checker.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--inventory", default=DEFAULT_INVENTORY)
    ap.add_argument("--check", action="store_true",
                    help="validate the inventory and exit")
    ap.add_argument("--strict", action="store_true",
                    help="exit 2 when there are findings")
    ap.add_argument("--render", action="store_true",
                    help="rewrite claims-findings.md")
    args = ap.parse_args(argv)

    try:
        data = load_inventory(args.inventory)
    except InventoryError as e:
        print("INVALID inventory: %s" % e)
        return 1

    if args.check:
        print("VALID — %d surfaces, %d canonical claims, every token resolves."
              % (len(data["surfaces"]), len(data["claims"])))
        return 0

    findings = find(data)

    if args.render:
        with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_report(data, findings))
        print("rendered %s (%d findings)" % (os.path.basename(REPORT), len(findings)))
        return 0

    print("Public claims consistency — %d surfaces compared" % len(data["surfaces"]))
    if not findings:
        print("  no findings: every surface asserts the same set, in the right category.")
        return 0
    for f in findings:
        print("  [%s] %s" % (f["type"], f["detail"]))
    print("%d finding(s). Each routes to the claim owner — nothing here edits a page."
          % len(findings))
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
