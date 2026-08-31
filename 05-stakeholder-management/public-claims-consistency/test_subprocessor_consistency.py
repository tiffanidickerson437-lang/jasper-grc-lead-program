#!/usr/bin/env python3
"""Attack subprocessor_consistency.py — control test, mutation guard, validation."""

import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subprocessor_consistency as sc  # noqa: E402


def clean_data():
    """Two surfaces in agreement — the control input."""
    return {
        "schema_version": 1,
        "tier": "llm-providers",
        "surfaces": [
            {"id": "a", "url": "https://example.com/a", "checked": "2026-08-31",
             "note": "n", "providers": ["openai", "anthropic"]},
            {"id": "b", "url": "https://example.com/b", "checked": "2026-08-31",
             "note": "n", "providers": ["Anthropic", "OpenAI"]},
        ],
    }


class ControlTest(unittest.TestCase):
    def test_agreeing_surfaces_yield_zero_findings(self):
        data = clean_data()
        sc.validate(data)
        self.assertEqual(sc.find(data), [])

    def test_case_and_order_do_not_manufacture_findings(self):
        # "OpenAI" vs "openai" is the same provider; a checker that fires on
        # capitalization gets muted, and then guards nothing.
        self.assertEqual(sc.find(clean_data()), [])


class CommittedData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sc.load(sc.DEFAULT_DATA)
        cls.findings = sc.find(cls.data)

    def test_cohere_divergence_is_detected(self):
        hits = [f for f in self.findings if f["provider"] == "cohere"]
        self.assertEqual(len(hits), 1,
                         "Cohere on the legal page and absent from the trust-center "
                         "panel is finding F3; if the surfaces changed, re-observe "
                         "subprocessors.yaml rather than deleting this test")
        self.assertEqual(hits[0]["present"], "legal-page")
        self.assertEqual(hits[0]["absent"], "trust-center-panel")

    def test_mutation_guard(self):
        self.assertGreaterEqual(
            len(self.findings), 1,
            "find() returned nothing on data with a known divergence — "
            "the comparator has been neutered")


class Validation(unittest.TestCase):
    def _reject(self, mutate, msg):
        data = clean_data()
        mutate(data)
        with self.assertRaises(sc.DataError, msg=msg):
            sc.validate(data)

    def test_three_surfaces_rejected(self):
        def add(d):
            d["surfaces"].append(copy.deepcopy(d["surfaces"][0]) | {"id": "c"})
        self._reject(add, "the comparison is pairwise by design")

    def test_missing_note_rejected(self):
        self._reject(lambda d: d["surfaces"][0].pop("note"),
                     "an observation without its note is not reproducible")

    def test_empty_providers_rejected(self):
        self._reject(lambda d: d["surfaces"][0].update(providers=[]),
                     "an empty list is an unmade observation, not agreement")

    def test_duplicate_provider_rejected(self):
        self._reject(lambda d: d["surfaces"][0].update(
            providers=["openai", "OpenAI"]),
            "duplicates inflate a surface's apparent disclosure")

    def test_non_string_provider_rejected(self):
        self._reject(lambda d: d["surfaces"][0].update(providers=["openai", True]),
                     "a boolean is not a vendor")

    def test_bad_date_rejected(self):
        self._reject(lambda d: d["surfaces"][0].update(checked="yesterday"),
                     "non-ISO dates must be rejected")

    def test_non_https_url_rejected(self):
        self._reject(lambda d: d["surfaces"][0].update(url="http://example.com/a"),
                     "observations must cite TLS-served pages")

    def test_non_slug_surface_id_rejected(self):
        self._reject(lambda d: d["surfaces"][0].update(id="A B"),
                     "ids are referenced in findings output")

    def test_missing_tier_rejected(self):
        self._reject(lambda d: d.pop("tier"),
                     "a comparison without a scope is unfalsifiable")


if __name__ == "__main__":
    unittest.main(verbosity=1)
