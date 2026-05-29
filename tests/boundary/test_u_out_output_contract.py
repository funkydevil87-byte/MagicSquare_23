"""U-OUT-01~03 — success output contract via Boundary E2E."""

from __future__ import annotations

from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary
from tests.conftest import GRID_G1


class TestUOutOutputContract:
    """FR-05-B — success int[6] shape with G1."""

    def test_u_out_01_g1_success_vector_length_six(self) -> None:
        boundary = MagicSquareBoundary()
        result = boundary.solve(GRID_G1)
        assert isinstance(result, list)
        assert len(result) == 6

    def test_u_out_02_g1_coordinates_one_indexed(self) -> None:
        boundary = MagicSquareBoundary()
        result = boundary.solve(GRID_G1)
        assert isinstance(result, list)
        r1, c1, _n1, r2, c2, _n2 = result
        for value in (r1, c1, r2, c2):
            assert 1 <= value <= 4

    def test_u_out_03_g1_missing_values_in_range(self) -> None:
        boundary = MagicSquareBoundary()
        result = boundary.solve(GRID_G1)
        assert isinstance(result, list)
        _r1, _c1, n1, _r2, _c2, n2 = result
        assert 1 <= n1 <= 16
        assert 1 <= n2 <= 16
        assert n1 != n2
