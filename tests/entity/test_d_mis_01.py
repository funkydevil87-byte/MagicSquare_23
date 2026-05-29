"""D-MIS-01 — find missing numbers. Track B Entity."""

from __future__ import annotations

from magicsquare.entity.services.missing_number_finder import MissingNumberFinder
from tests.entity.conftest import GRID_G1


class TestDMis01:
    """FR-03 / I7, I11 — missing pair sorted ascending on G1."""

    def test_d_mis_01_g1_missing_seven_and_ten(self) -> None:
        # Arrange
        finder = MissingNumberFinder()

        # Act
        small, large = finder.find_missing(GRID_G1)

        # Assert
        assert small == 7
        assert large == 10
        assert small < large
