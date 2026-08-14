#!/usr/bin/env python3

import csv
import json
import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.stats import wasserstein_distance


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "04_SRC"))
import run_obrc as obrc  # noqa: E402


class TestOBRC(unittest.TestCase):
    def test_corrected_s90_uses_asymmetric_error_widths(self):
        a = {"median": 10.0, "lower": 2.0, "upper": 3.0}
        b = {"median": 12.0, "lower": 1.0, "upper": 2.0}
        self.assertAlmostEqual(obrc.corrected_s90(a, b), 1.0)

    def test_reconstructed_endpoints(self):
        median, lower, upper = 5.0, 1.5, 2.5
        self.assertEqual(median - lower, 3.5)
        self.assertEqual(median + upper, 7.5)

    def test_ecdf_wasserstein_matches_scipy_unequal_samples(self):
        a = np.asarray([-2.0, 0.0, 0.5, 4.0])
        b = np.asarray([-1.0, 1.0, 2.0, 2.0, 8.0])
        self.assertAlmostEqual(obrc.ecdf_wasserstein(a, b), wasserstein_distance(a, b), places=14)

    def test_normalized_w1_dual_implementation(self):
        rng = np.random.Generator(np.random.PCG64DXSM(9))
        a = rng.normal(0.0, 1.0, 137)
        b = rng.normal(0.4, 1.2, 211)
        normalized, raw, scale, difference = obrc.normalized_w1(a, b)
        self.assertGreater(normalized, 0.0)
        self.assertGreater(raw, 0.0)
        self.assertGreater(scale, 0.0)
        self.assertLessEqual(difference, 1e-10 * max(1.0, abs(raw)))

    def test_scale_floor_for_constant_equal_samples(self):
        scale = obrc.pair_scale(np.ones(30), np.ones(40))
        self.assertEqual(scale, 1e-12)

    def test_cell_seed_is_deterministic_and_keyed(self):
        first = obrc.cell_seed("GW1", "A", "B", "p")
        self.assertEqual(first, obrc.cell_seed("GW1", "A", "B", "p"))
        self.assertNotEqual(first, obrc.cell_seed("GW2", "A", "B", "p"))

    def test_balanced_values_are_deterministic(self):
        old_repetitions = obrc.BALANCED_REPETITIONS
        old_maximum = obrc.BALANCED_MAXIMUM
        try:
            obrc.BALANCED_REPETITIONS = 7
            obrc.BALANCED_MAXIMUM = 30
            a = np.arange(100, dtype=float)
            b = np.arange(80, dtype=float) + 0.5
            first, n1 = obrc.balanced_values(a, b, 123)
            second, n2 = obrc.balanced_values(a, b, 123)
            np.testing.assert_array_equal(first, second)
            self.assertEqual(n1, 30)
            self.assertEqual(n2, 30)
        finally:
            obrc.BALANCED_REPETITIONS = old_repetitions
            obrc.BALANCED_MAXIMUM = old_maximum

    def test_ranked_correlation_allows_ties(self):
        rho, rank_x, rank_y = obrc.ranked_correlation([1, 1, 2, 3], [0, 2, 1, 4])
        self.assertIsNotNone(rho)
        self.assertEqual(rank_x.tolist(), [1.5, 1.5, 3.0, 4.0])
        self.assertEqual(len(rank_y), 4)

    def test_constant_vector_is_frozen_non_support(self):
        old_permutations = obrc.PERMUTATIONS
        try:
            obrc.PERMUTATIONS = 100
            result = obrc.monte_carlo_test(np.ones(5), np.arange(5.0))
            self.assertEqual(result["verdict"], "NOT_SUPPORTED_CONSTANT_VECTOR")
        finally:
            obrc.PERMUTATIONS = old_permutations

    def test_monte_carlo_replay_is_exact_for_fixed_seed(self):
        old_permutations = obrc.PERMUTATIONS
        try:
            obrc.PERMUTATIONS = 5000
            x = np.arange(8.0)
            y = np.asarray([0.0, 1.0, 3.0, 2.0, 5.0, 4.0, 7.0, 6.0])
            first = obrc.monte_carlo_test(x, y, batch_size=777)
            second = obrc.monte_carlo_test(x, y, batch_size=777)
            self.assertEqual(first, second)
            self.assertEqual(first["permutations"], 5000)
        finally:
            obrc.PERMUTATIONS = old_permutations

    def test_candidate_frame_and_protocol_shape(self):
        with (ROOT / "03_INPUT/CANDIDATE_EVENT_FREEZE.csv").open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        protocol = json.loads((ROOT / "02_ANALYSIS_LOCK/OUTCOME_BLIND_ANALYSIS_PROTOCOL.json").read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 22)
        self.assertEqual(len({row["event"] for row in rows}), 22)
        self.assertEqual(protocol["primary_test"]["n"], 22)
        self.assertTrue(protocol["frozen_candidate_frame"]["include_all_events"])
        self.assertFalse(protocol["historical_parent_effect"]["b07_scientific_closure_modified"])


if __name__ == "__main__":
    unittest.main()
