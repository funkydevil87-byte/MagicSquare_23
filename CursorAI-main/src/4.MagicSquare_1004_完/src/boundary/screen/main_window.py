"""PyQt main window for Magic Square 4×4 partial grid solver."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.schemas import FailureResponse, SuccessResponse
from boundary.ui_boundary import UIBoundary

_GRID_SIZE = 4
_SPIN_MIN = 0
_SPIN_MAX = 16

G1_DEFAULT_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class MagicSquareMainWindow(QMainWindow):
    """4×4 spinbox grid with solve action wired to ``UIBoundary``."""

    def __init__(self, boundary: UIBoundary) -> None:
        """Initialize the window with an injected boundary entry point.

        Args:
            boundary: Orchestrates validation and control for ``solve()``.
        """
        super().__init__()
        self._boundary = boundary
        self._spinboxes: list[list[QSpinBox]] = []
        self._result_label = QLabel("")
        self._init_ui()

    def _init_ui(self) -> None:
        """Build grid spinboxes, solve button, and result label."""
        self.setWindowTitle("Magic Square 4x4")

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        grid_layout = QGridLayout()
        for row in range(_GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col in range(_GRID_SIZE):
                spinbox = QSpinBox()
                spinbox.setRange(_SPIN_MIN, _SPIN_MAX)
                spinbox.setValue(G1_DEFAULT_GRID[row][col])
                grid_layout.addWidget(spinbox, row, col)
                row_boxes.append(spinbox)
            self._spinboxes.append(row_boxes)

        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve)

        root_layout.addLayout(grid_layout)
        root_layout.addWidget(solve_button)
        root_layout.addWidget(self._result_label)

    def _read_grid(self) -> list[list[int]]:
        """Read current spinbox values as a 4×4 integer matrix."""
        return [
            [spinbox.value() for spinbox in row_boxes]
            for row_boxes in self._spinboxes
        ]

    def _on_solve(self) -> None:
        """Invoke ``UIBoundary.solve`` and render success or error message."""
        grid = self._read_grid()
        result = self._boundary.solve(grid)

        if isinstance(result, SuccessResponse):
            values = ", ".join(str(value) for value in result.data)
            self._result_label.setText(
                f"결과 (r1, c1, n1, r2, c2, n2): {values}"
            )
            return

        if isinstance(result, FailureResponse):
            self._result_label.setText(f"오류: {result.error.message}")
