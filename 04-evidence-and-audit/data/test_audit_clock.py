#!/usr/bin/env python3
"""Attack audit_clock.py — control test, mutation guard, date math, staleness."""

import datetime as _dt
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_clock as ac  # noqa: E402


def clean_data():
    return {
        "schema_version": 1,
        "dates": [
            {"id": "a", "date": "2026-08-02", "kind": "applied",
             "label": "A applied", "source": "https://example.com/a"},
            {"id": "b", "date": "2026-12-02", "kind": "deadline",
             "label": "B lands", "source": "https://example.com/b"},
            {"id": "c", "date": "2027-08-14", "kind": "estimate", "estimated": True,
             "label": "C window (ESTIMATE)", "source": "https://example.com/c"},
        ],
    }


class ControlTest(unittest.TestCase):
    def test_clean_data_validates(self):
        ac.validate(clean_data())  # must not raise


class DateMath(unittest.TestCase):
    def test_days_since_and_until_are_correct(self):
        # Fixed as-of makes the arithmetic assertable: 2026-08-02 -> 2026-08-31
        # is 29 days; 2026-08-31 -> 2026-12-02 is 93 days. These are the two
        # numbers the walkthrough page shows, so they must be right here.
        lines = "\n".join(ac.report_lines(clean_data(),
                                          _dt.date(2026, 8, 31)))
        self.assertIn("  29 days ago", lines)
        self.assertIn("in   93 days", lines)

    def test_estimates_are_labelled_on_the_report(self):
        lines = "\n".join(ac.report_lines(clean_data(),
                                          _dt.date(2026, 8, 31)))
        self.assertIn("[ESTIMATE]", lines)


class CommittedData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = ac.load(ac.DEFAULT_DATA)

    def test_art50_rows_present(self):
        ids = {r["id"] for r in self.data["dates"]}
        self.assertIn("eu-ai-act-art50-disclosure", ids)
        self.assertIn("eu-ai-act-art50-marking", ids)

    def test_surveillance_row_is_an_estimate(self):
        row = next(r for r in self.data["dates"]
                   if r["id"] == "iso27001-surveillance")
        self.assertEqual(row["kind"], "estimate",
                         "the surveillance date is derived, not published; "
                         "presenting it as fixed is the stale-timeline failure "
                         "this repo exists to prevent")

    def test_mutation_guard(self):
        # If validate() is gutted to accept anything, this junk passing is what
        # turns the suite red.
        with self.assertRaises(ac.DataError):
            ac.validate({"schema_version": 1,
                         "dates": [{"id": "x", "date": "soon", "kind": "vibes",
                                    "label": "", "source": "trust me"}]})


class Validation(unittest.TestCase):
    def _reject(self, mutate, msg):
        data = clean_data()
        mutate(data)
        with self.assertRaises(ac.DataError, msg=msg):
            ac.validate(data)

    def test_unsourced_date_rejected(self):
        self._reject(lambda d: d["dates"][0].update(source="ask around"),
                     "a date without an https source is an assertion")

    def test_estimate_without_flag_rejected(self):
        self._reject(lambda d: d["dates"][2].pop("estimated"),
                     "kind: estimate must carry estimated: true")

    def test_flag_without_estimate_kind_rejected(self):
        self._reject(lambda d: d["dates"][0].update(estimated=True),
                     "estimated: true on an applied row is a category error")

    def test_bad_date_rejected(self):
        self._reject(lambda d: d["dates"][0].update(date="Q3 2026"),
                     "quarters are not dates")

    def test_duplicate_id_rejected(self):
        self._reject(lambda d: d["dates"][1].update(id="a"),
                     "duplicate ids make rows unaddressable")


class RenderedCalendar(unittest.TestCase):
    def test_calendar_contains_no_day_counts(self):
        # The rendered file must be stable day to day, or the CI staleness check
        # fails every morning and gets deleted by Friday. Any "N days" phrasing
        # in the render is a defect.
        text = ac.render_calendar(ac.load(ac.DEFAULT_DATA))
        self.assertIsNone(re.search(r"\b\d+\s+days\b", text),
                          "day counts belong to stdout, never the rendered file")

    def test_committed_calendar_is_not_stale(self):
        rendered = ac.render_calendar(ac.load(ac.DEFAULT_DATA))
        with open(ac.CALENDAR, encoding="utf-8") as fh:
            committed = fh.read()
        self.assertEqual(committed, rendered,
                         "audit-calendar.md is stale — run "
                         "`python3 audit_clock.py --render` and commit the result")

    def test_render_is_deterministic(self):
        data = ac.load(ac.DEFAULT_DATA)
        self.assertEqual(ac.render_calendar(data), ac.render_calendar(data))


if __name__ == "__main__":
    unittest.main(verbosity=1)
