#!/usr/bin/env python3
"""Attack check_claims.py.

House rules for every checker in this repository:
  1. A CONTROL TEST: a clean input must produce zero findings, because a validator
     that fires on valid input gets muted by lunchtime and then guards nothing.
  2. A MUTATION GUARD: gut the comparator to always-pass and this suite turns red.
  3. The committed inventory's real findings are asserted BY NAME, so the repo cannot
     silently drift into claiming findings its own data no longer supports.
"""

import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_claims as cc  # noqa: E402


def clean_inventory():
    """Two surfaces in perfect agreement — the control input."""
    return {
        "schema_version": 1,
        "aliases": {"pci-dss": "pci"},
        "claims": {
            "soc2": {"kind": "certification", "label": "SOC 2"},
            "pci": {"kind": "certification", "label": "PCI DSS"},
            "gdpr": {"kind": "law", "label": "GDPR"},
        },
        "surfaces": [
            {"id": "a", "url": "https://example.com/a", "audience": "marketing",
             "checked": "2026-08-31", "quote": "q", "claims": ["soc2", "pci", "gdpr"]},
            {"id": "b", "url": "https://example.com/b", "audience": "assurance",
             "checked": "2026-08-31", "quote": "q", "claims": ["soc2", "pci-dss", "gdpr"]},
        ],
    }


class ControlTest(unittest.TestCase):
    def test_clean_inventory_yields_zero_findings(self):
        inv = clean_inventory()
        cc.validate_inventory(inv)
        self.assertEqual(cc.find(inv), [])

    def test_alias_agreement_is_agreement(self):
        # 'pci-dss' on one surface and 'pci' on another is the SAME claim.
        # If normalization breaks, this clean input starts producing findings.
        inv = clean_inventory()
        findings = [f for f in cc.find(inv) if f["claim"] == "pci"]
        self.assertEqual(findings, [])


class CommittedInventory(unittest.TestCase):
    """The real inventory, and the real findings this repository claims exist."""

    @classmethod
    def setUpClass(cls):
        cls.data = cc.load_inventory(cc.DEFAULT_INVENTORY)
        cls.findings = cc.find(cls.data)

    def test_inventory_is_valid(self):
        self.assertGreaterEqual(len(self.data["surfaces"]), 3)

    def test_iso27001_marketing_gap_is_detected(self):
        gaps = [f for f in self.findings
                if f["type"] == "MARKETING_GAP" and f["claim"] == "iso27001"]
        self.assertEqual(len(gaps), 1,
                         "ISO 27001 on the trust center and no marketing page is "
                         "finding F1's headline; if the pages changed, re-observe "
                         "the inventory rather than deleting this test")

    def test_pci_divergence_is_detected(self):
        div = [f for f in self.findings
               if f["type"] == "DIVERGENT" and f["claim"] == "pci"]
        self.assertEqual(len(div), 1)
        self.assertIn("trust-center", div[0]["detail"])  # the absent side

    def test_dpa_category_error_is_detected(self):
        cat = [f for f in self.findings
               if f["type"] == "CATEGORY" and f["claim"] == "dpa"]
        self.assertEqual(len(cat), 1)

    def test_mutation_guard(self):
        # If find() is gutted to return [], the committed inventory's known
        # divergences vanish — and this test is what turns red.
        self.assertGreaterEqual(len(self.findings), 3,
                                "find() appears to be returning nothing on an "
                                "inventory with known divergences — the comparator "
                                "has been neutered")


class Validation(unittest.TestCase):
    def _reject(self, mutate, msg):
        inv = clean_inventory()
        mutate(inv)
        with self.assertRaises(cc.InventoryError, msg=msg):
            cc.validate_inventory(inv)

    def test_unknown_claim_token_rejected(self):
        self._reject(lambda i: i["surfaces"][0]["claims"].append("iso9001"),
                     "unknown tokens must fail loudly, not compare as nothing")

    def test_boolean_claim_token_rejected(self):
        # YAML parses bare `on` as True, and bool is an int subclass; a claims
        # list containing True must be a validation error, not a claim.
        self._reject(lambda i: i["surfaces"][0]["claims"].append(True),
                     "a boolean wearing a claim's clothes must be rejected")

    def test_missing_quote_rejected(self):
        self._reject(lambda i: i["surfaces"][0].pop("quote"),
                     "an observation without its quote is not reproducible")

    def test_bad_date_rejected(self):
        self._reject(lambda i: i["surfaces"][0].update(checked="Aug 31"),
                     "non-ISO dates must be rejected")

    def test_single_surface_rejected(self):
        self._reject(lambda i: i["surfaces"].pop(),
                     "one surface cannot diverge from itself")

    def test_alias_to_unknown_claim_rejected(self):
        self._reject(lambda i: i["aliases"].update({"soc-2": "soc2-type2"}),
                     "an alias must resolve into the registry")

    def test_duplicate_surface_id_rejected(self):
        def dup(i):
            i["surfaces"].append(copy.deepcopy(i["surfaces"][0]))
        self._reject(dup, "duplicate surface ids silently merge observations")

    def test_non_https_url_rejected(self):
        self._reject(lambda i: i["surfaces"][0].update(url="http://example.com/a"),
                     "a checker whose observations ride plaintext HTTP invites "
                     "tampered observations; and the url lands in rendered markdown")

    def test_non_slug_surface_id_rejected(self):
        self._reject(lambda i: i["surfaces"][0].update(id="a|b](x"),
                     "ids land verbatim in rendered markdown tables")

    def test_bad_kind_rejected(self):
        self._reject(lambda i: i["claims"].update(
            {"x": {"kind": "vibe", "label": "X"}}),
            "unknown kinds must be rejected")


class Render(unittest.TestCase):
    def test_report_is_deterministic(self):
        data = cc.load_inventory(cc.DEFAULT_INVENTORY)
        f = cc.find(data)
        self.assertEqual(cc.render_report(data, f), cc.render_report(data, f))

    def test_committed_report_is_not_stale(self):
        data = cc.load_inventory(cc.DEFAULT_INVENTORY)
        rendered = cc.render_report(data, cc.find(data))
        with open(cc.REPORT, encoding="utf-8") as fh:
            committed = fh.read()
        self.assertEqual(committed, rendered,
                         "claims-findings.md is stale — run "
                         "`python3 check_claims.py --render` and commit the result")


if __name__ == "__main__":
    unittest.main(verbosity=1)
