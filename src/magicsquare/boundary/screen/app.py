"""Tkinter GUI for manual Magic Square Boundary verification.

Run from the project root (after ``pip install -e .``)::

    python -m magicsquare.boundary.screen.app

Or with PYTHONPATH::

    $env:PYTHONPATH = "src"   # PowerShell
    python -m magicsquare.boundary.screen.app
"""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from typing import Any

from magicsquare.boundary.exceptions import BoundaryValidationError, UnsolvableError
from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary
from magicsquare.boundary.schemas import GRID_SIZE, FailureResult

SAMPLE_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

SAMPLE_COMPLETE: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


class MagicSquareApp:
    """4x4 grid editor that calls ``MagicSquareBoundary.solve``."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._boundary = MagicSquareBoundary()
        self._cell_vars: list[list[tk.StringVar]] = []

        root.title("Magic Square 4×4")
        root.minsize(520, 560)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self._build_layout()
        self.load_grid(SAMPLE_G1)

    def _build_layout(self) -> None:
        container = ttk.Frame(self._root, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        title = ttk.Label(
            container,
            text="Partial Magic Square Solver",
            font=tkfont.Font(size=14, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 4))

        hint = ttk.Label(
            container,
            text="Enter 1–16 or leave blank / 0 for empty cells. Magic constant = 34.",
            wraplength=480,
        )
        hint.grid(row=1, column=0, sticky="w", pady=(0, 12))

        grid_frame = ttk.LabelFrame(container, text="4×4 Grid", padding=12)
        grid_frame.grid(row=2, column=0, sticky="n")
        for col in range(GRID_SIZE + 1):
            grid_frame.columnconfigure(col, weight=1)

        entry_font = tkfont.Font(size=13)
        for row in range(GRID_SIZE):
            ttk.Label(grid_frame, text=str(row + 1), width=2).grid(
                row=row + 1, column=0, padx=(0, 6)
            )
            row_vars: list[tk.StringVar] = []
            for col in range(GRID_SIZE):
                var = tk.StringVar()
                entry = ttk.Entry(
                    grid_frame,
                    textvariable=var,
                    width=4,
                    justify="center",
                    font=entry_font,
                )
                entry.grid(row=row + 1, column=col + 1, padx=4, pady=4)
                row_vars.append(var)
            self._cell_vars.append(row_vars)

        col_headers = ttk.Frame(grid_frame)
        col_headers.grid(row=0, column=1, columnspan=GRID_SIZE)
        for col in range(GRID_SIZE):
            ttk.Label(col_headers, text=str(col + 1), width=4).grid(
                row=0, column=col, padx=4
            )

        button_row = ttk.Frame(container)
        button_row.grid(row=3, column=0, pady=16, sticky="w")

        ttk.Button(button_row, text="Solve", command=self.on_solve).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(button_row, text="Clear", command=self.on_clear).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(
            button_row,
            text="Load G1 (2 blanks)",
            command=lambda: self.load_grid(SAMPLE_G1),
        ).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(
            button_row,
            text="Load complete square",
            command=lambda: self.load_grid(SAMPLE_COMPLETE),
        ).grid(row=0, column=3)

        result_frame = ttk.LabelFrame(container, text="Result", padding=12)
        result_frame.grid(row=4, column=0, sticky="ew")
        result_frame.columnconfigure(0, weight=1)

        self._result_var = tk.StringVar(value="Press Solve to call Boundary API.")
        self._result_label = ttk.Label(
            result_frame,
            textvariable=self._result_var,
            wraplength=480,
            justify="left",
        )
        self._result_label.grid(row=0, column=0, sticky="w")

    def load_grid(self, grid: list[list[int]]) -> None:
        """Fill entry widgets from a 4×4 integer grid."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = grid[row][col]
                self._cell_vars[row][col].set("" if value == 0 else str(value))
        self._set_result("Sample grid loaded. Press Solve.", "info")

    def on_clear(self) -> None:
        """Clear all cells and reset the result panel."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self._cell_vars[row][col].set("")
        self._set_result("Grid cleared.", "info")

    def on_solve(self) -> None:
        """Read grid, call Boundary, and display outcome."""
        try:
            grid = self._read_grid()
        except ValueError as exc:
            self._set_result(str(exc), "error")
            return

        try:
            result = self._boundary.solve(grid)
        except BoundaryValidationError as exc:
            self._set_result(
                f"Boundary validation failed\n"
                f"  code: {exc.code}\n"
                f"  message: {exc.message}",
                "error",
            )
            return
        except UnsolvableError as exc:
            self._set_result(
                f"Boundary solve failed\n"
                f"  code: {exc.code}\n"
                f"  message: {exc.message}",
                "error",
            )
            return
        except Exception as exc:  # noqa: BLE001 — screen must surface unexpected faults
            self._set_result(f"Unexpected error: {exc}", "error")
            return

        self._display_result(result)

    def _read_grid(self) -> list[list[int]]:
        grid: list[list[int]] = []
        for row in range(GRID_SIZE):
            row_values: list[int] = []
            for col in range(GRID_SIZE):
                raw = self._cell_vars[row][col].get().strip()
                if raw == "":
                    row_values.append(0)
                    continue
                if not raw.lstrip("-").isdigit():
                    raise ValueError(
                        f"Cell ({row + 1},{col + 1}): enter an integer, blank, or 0."
                    )
                value = int(raw)
                if value < 0 or value > 16:
                    raise ValueError(
                        f"Cell ({row + 1},{col + 1}): value must be 0–16."
                    )
                row_values.append(value)
            grid.append(row_values)
        return grid

    def _display_result(self, result: Any) -> None:
        if isinstance(result, FailureResult) or (
            hasattr(result, "code") and hasattr(result, "message")
        ):
            self._set_result(
                f"Boundary validation failed\n"
                f"  code: {result.code}\n"
                f"  message: {result.message}",
                "error",
            )
            return

        if isinstance(result, (list, tuple)) and len(result) == 6:
            r1, c1, n1, r2, c2, n2 = result
            self._set_result(
                "Solve succeeded\n"
                f"  blank ({r1},{c1}) ← {n1}\n"
                f"  blank ({r2},{c2}) ← {n2}\n"
                f"  vector: {list(result)}",
                "success",
            )
            return

        self._set_result(f"Unknown result type: {result!r}", "warning")

    def _set_result(self, text: str, tone: str) -> None:
        self._result_var.set(text)
        styles = {
            "info": {"foreground": "#1f2937"},
            "success": {"foreground": "#166534"},
            "warning": {"foreground": "#92400e"},
            "error": {"foreground": "#b91c1c"},
        }
        self._result_label.configure(style="")
        self._result_label.configure(foreground=styles.get(tone, styles["info"])["foreground"])


def main() -> None:
    """Launch the Magic Square tkinter application."""
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except tk.TclError:
        pass
    MagicSquareApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
