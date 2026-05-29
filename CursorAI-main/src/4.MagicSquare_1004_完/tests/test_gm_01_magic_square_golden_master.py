"""GM-1 — Magic Square Solver Golden Master regression test."""

from __future__ import annotations

from pathlib import Path

import pytest

from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare

from tests.golden_master_support import (
    DEFAULT_GOLDEN_MASTER_PATH,
    approve_golden_master,
    build_golden_master_document,
)


@pytest.fixture
def golden_master_boundary() -> UIBoundary:
    """Real UIBoundary stack for end-to-end output capture."""
    return UIBoundary(solve_use_case=SolvePartialMagicSquare())


class TestGoldenMasterMagicSquare:
    """GM-1 — approve-pattern regression against ``golden_master_expected.txt``."""

    def test_gm_01_solver_output_matches_golden_master(
        self,
        golden_master_boundary: UIBoundary,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """GM-1 — capture UIBoundary DTO output and compare to baseline."""
        # Arrange
        actual = build_golden_master_document(golden_master_boundary)

        # Act / Assert — approve pattern
        status = approve_golden_master(
            actual,
            golden_master_path,
            auto_create=True,
            force_update=approve_golden,
        )

        assert status in {"matched", "created", "updated"}
