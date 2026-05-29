"""Magic Square 4×4 PyQt screen entry point.

Run from project root after ``pip install -e ".[gui]"``:

    python -m boundary.screen.app

Optional AC-FR-01-01 grid=None verification (CLI):

    python -m boundary.screen.app --verify
"""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from boundary.schemas import FailureResponse, SuccessResponse
from boundary.screen.main_window import MagicSquareMainWindow
from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare


def create_boundary() -> UIBoundary:
    """Composition root — wire Control into ``UIBoundary``."""
    return UIBoundary(solve_use_case=SolvePartialMagicSquare())


def run_verify_none_grid() -> None:
    """Print ``UIBoundary.solve(None)`` envelope for manual AC verification."""
    result = create_boundary().solve(None)
    if isinstance(result, FailureResponse):
        print(f"type={result.type}")
        print(f"code={result.error.code}")
        print(f"message={result.error.message}")
        return
    if isinstance(result, SuccessResponse):
        print(f"type={result.type}")
        print(f"data={result.data}")


def main() -> int:
    """Launch the main window or ``--verify`` CLI check.

    Returns:
        Process exit code (0 on success).
    """
    if "--verify" in sys.argv:
        run_verify_none_grid()
        return 0

    app = QApplication(sys.argv)
    window = MagicSquareMainWindow(create_boundary())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
