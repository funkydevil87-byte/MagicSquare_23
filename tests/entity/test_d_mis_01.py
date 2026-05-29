"""D-MIS-01 — find missing numbers. Track B Entity RED skeleton (no Domain mock)."""

from __future__ import annotations

import pytest


class TestDMis01:
    """FR-03 / I7, I11 — missing pair sorted ascending on G1."""

    def test_d_mis_01_g1_missing_seven_and_ten(self) -> None:
        # D-MIS-01
        # from magicsquare.entity.services.missing_number_finder import MissingNumberFinder
        # Given: G1 partial grid
        # finder = MissingNumberFinder()
        # When: finder.find_missing(grid_g1)
        pytest.fail("RED: D-MIS-01 — G1 missing numbers {7, 10} ascending")
