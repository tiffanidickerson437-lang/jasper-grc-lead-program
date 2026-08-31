#!/usr/bin/env python3
"""Subprocessor consistency check (finding F3).

Jasper discloses subprocessors on two of its own public surfaces: the legal
sub-processors page and the trust center's subprocessor panel. On the LLM tier —
the tier the "never used to train third-party LLMs" commitment rides on — the two
lists did not agree when observed. This tool compares the committed observations in
subprocessors.yaml and reports every provider that appears on one surface and not
the other.

It reports divergence between Jasper's own disclosures. It does not, and cannot,
say which list is right; §3.3 of the public Information Security Requirements
(annual reassessment of every subprocessor, audit-report review included) is why
someone inside needs to.

Usage:
  python3 subprocessor_consistency.py            # report, exit 0
  python3 subprocessor_consistency.py --strict   # exit 2 on findings
  python3 subprocessor_consistency.py --check    # validate the data file only
  python3 subprocessor_consistency.py --data PATH

Exit codes: 0 clean/reported · 1 invalid data · 2 findings under --strict.
"""

import argparse
import datetime as _dt
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(HERE, "subprocessors.yaml")


class DataError(ValueError):
    pass


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    validate(data)
    return data


def validate(data):
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise DataError("schema_version must be 1")
    if not data.get("tier"):
        raise DataError("tier missing — a comparison without a scope is unfalsifiable")
    surfaces = data.get("surfaces")
    if not isinstance(surfaces, list) or len(surfaces) != 2:
        raise DataError("exactly two surfaces are compared; got %r"
                        % (len(surfaces) if isinstance(surfaces, list) else surfaces))
    ids = set()
    for s in surfaces:
        for field in ("id", "url", "checked", "note", "providers"):
            if not s.get(field):
                raise DataError("surface %r: %s missing" % (s.get("id", "?"), field))
        if s["id"] in ids:
            raise DataError("duplicate surface id %r" % s["id"])
        ids.add(s["id"])
        try:
            _dt.date.fromisoformat(str(s["checked"]))
        except ValueError:
            raise DataError("surface %r: checked is not an ISO date" % s["id"])
        if not isinstance(s["providers"], list) or not s["providers"]:
            raise DataError("surface %r: providers must be a non-empty list" % s["id"])
        for p in s["providers"]:
            if not isinstance(p, str) or not p.strip():
                raise DataError("surface %r: provider %r is not a name" % (s["id"], p))
        lowered = [p.strip().lower() for p in s["providers"]]
        if len(set(lowered)) != len(lowered):
            raise DataError("surface %r: duplicate provider entries" % s["id"])


def find(data):
    a, b = data["surfaces"]
    set_a = {p.strip().lower() for p in a["providers"]}
    set_b = {p.strip().lower() for p in b["providers"]}
    findings = []
    for p in sorted(set_a - set_b):
        findings.append({"provider": p, "present": a["id"], "absent": b["id"]})
    for p in sorted(set_b - set_a):
        findings.append({"provider": p, "present": b["id"], "absent": a["id"]})
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)

    try:
        data = load(args.data)
    except DataError as e:
        print("INVALID data: %s" % e)
        return 1

    if args.check:
        print("VALID — 2 surfaces, tier %r, every entry carries url/date/note."
              % data["tier"])
        return 0

    findings = find(data)
    a, b = data["surfaces"]
    print("Subprocessor consistency — tier %r" % data["tier"])
    print("  %s (%s): %s" % (a["id"], a["checked"],
                             ", ".join(sorted(a["providers"]))))
    print("  %s (%s): %s" % (b["id"], b["checked"],
                             ", ".join(sorted(b["providers"]))))
    if not findings:
        print("  no findings: both surfaces disclose the same set.")
        return 0
    for f in findings:
        print("  [DIVERGENT] %s listed on %s, absent from %s"
              % (f["provider"], f["present"], f["absent"]))
    print("%d finding(s). Which list is right is the claim owner's call — "
          "ISR §3.3 is why it has to be made." % len(findings))
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
