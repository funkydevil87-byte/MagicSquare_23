"""D-LOC-01 — locate blank cells. Track B Entity."""

from __future__ import annotations

from magicsquare.entity.services.empty_cell_locator import EmptyCellLocator
from tests.entity.conftest import GRID_G1


class TestDLoc01:
    """FR-02 / I6 — row-major first and second blank on G1."""

    def test_d_loc_01_g1_row_major_blank_pair(self) -> None:
        # Arrange
        locator = EmptyCellLocator()

        # Act
        first_blank, second_blank = locator.locate(GRID_G1)

        # Assert
        assert first_blank == (2, 2)
        assert second_blank == (3, 3)
