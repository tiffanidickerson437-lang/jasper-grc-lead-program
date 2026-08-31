#!/usr/bin/env python3
"""The audit clock, computed — "momentum is a computed state".

Reads regulatory-dates.yaml, validates it, and reports every governing date as
days-since (applied) or days-until (deadline), so the plan's urgency is arithmetic
rather than adjective. Estimates are labelled ESTIMATE on every output path — a
derived date that prints like a published one is how stale timelines get cited.

Usage:
  python3 audit_clock.py                     # report against today (UTC)
  python3 audit_clock.py --as-of 2026-08-31  # report against a fixed date (reproducible)
  python3 audit_clock.py --check             # validate the data file only
  python3 audit_clock.py --render            # rewrite ../frameworks/audit-calendar.md

The rendered calendar contains FIXED DATES ONLY — no day counts — so it is stable
day to day and CI can assert it is not stale. Day counts belong to stdout, where
"today" is explicit.

Exit codes: 0 ok · 1 invalid data.
"""

import argparse
import datetime as _dt
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(HERE, "regulatory-dates.yaml")
CALENDAR = os.path.normpath(os.path.join(HERE, "..", "frameworks",
                                         "audit-calendar.md"))

VALID_KINDS = {"applied", "deadline", "estimate"}


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
    rows = data.get("dates")
    if not isinstance(rows, list) or not rows:
        raise DataError("dates missing or empty")
    seen = set()
    for r in rows:
        if not isinstance(r, dict):
            raise DataError("date rows must be mappings")
        for field in ("id", "date", "kind", "label", "source"):
            if not r.get(field):
                raise DataError("row %r: %s missing" % (r.get("id", "?"), field))
        if r["id"] in seen:
            raise DataError("duplicate id %r" % r["id"])
        seen.add(r["id"])
        if r["kind"] not in VALID_KINDS:
            raise DataError("row %r: kind must be one of %s"
                            % (r["id"], sorted(VALID_KINDS)))
        try:
            _dt.date.fromisoformat(str(r["date"]))
        except ValueError:
            raise DataError("row %r: date is not ISO format" % r["id"])
        if not str(r["source"]).startswith("https://"):
            raise DataError("row %r: source must be an https URL — a date without "
                            "a source is an assertion, not a fact" % r["id"])
        if r["kind"] == "estimate" and not r.get("estimated"):
            raise DataError("row %r: kind estimate requires estimated: true, so the "
                            "flag survives into machine consumers" % r["id"])
        if r.get("estimated") and r["kind"] != "estimate":
            raise DataError("row %r: estimated: true requires kind estimate" % r["id"])


def rows_sorted(data):
    return sorted(data["dates"], key=lambda r: (str(r["date"]), r["id"]))


def report_lines(data, as_of):
    lines = ["The audit clock — as of %s" % as_of.isoformat()]
    for r in rows_sorted(data):
        d = _dt.date.fromisoformat(str(r["date"]))
        delta = (as_of - d).days
        tag = " [ESTIMATE]" if r["kind"] == "estimate" else ""
        if delta >= 0:
            when = "%4d days ago " % delta
        else:
            when = "in %4d days  " % -delta
        lines.append("  %s %s %s%s" % (d.isoformat(), when, r["label"], tag))
    return lines


def render_calendar(data):
    lines = [
        "# The audit calendar",
        "",
        "Rendered by `audit_clock.py --render` from"
        " [`regulatory-dates.yaml`](../data/regulatory-dates.yaml)."
        " Do not edit by hand — re-run the tool.",
        "",
        "Fixed dates only, so this file is stable and CI can prove it is not stale."
        " For live day counts, run `python3 audit_clock.py`.",
        "",
        "| Date | Kind | What | Source |",
        "|---|---|---|---|",
    ]
    for r in rows_sorted(data):
        kind = "ESTIMATE" if r["kind"] == "estimate" else r["kind"]
        lines.append("| %s | %s | %s | [source](%s) |"
                     % (r["date"], kind, r["label"], r["source"]))
    lines += [
        "",
        "Every estimate row states its derivation in the data file and is never"
        " cited as a hard date.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--as-of", default=None,
                    help="ISO date to compute against (default: today, UTC)")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--render", action="store_true")
    args = ap.parse_args(argv)

    try:
        data = load(args.data)
    except DataError as e:
        print("INVALID data: %s" % e)
        return 1

    if args.check:
        est = sum(1 for r in data["dates"] if r["kind"] == "estimate")
        print("VALID — %d dated rows, %d flagged ESTIMATE, every row sourced."
              % (len(data["dates"]), est))
        return 0

    if args.render:
        with open(CALENDAR, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_calendar(data))
        print("rendered %s (%d rows)" % (os.path.basename(CALENDAR),
                                         len(data["dates"])))
        return 0

    if args.as_of:
        try:
            as_of = _dt.date.fromisoformat(args.as_of)
        except ValueError:
            print("INVALID --as-of: not an ISO date")
            return 1
    else:
        as_of = _dt.datetime.now(_dt.timezone.utc).date()

    for line in report_lines(data, as_of):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
