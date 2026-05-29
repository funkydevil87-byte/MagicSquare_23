"""Approve-pattern utilities for Magic Square Golden Master tests (GM-1)."""

from __future__ import annotations

import difflib
from pathlib import Path

from boundary.schemas import FailureResponse, SuccessResponse
from boundary.ui_boundary import UIBoundary
from entity.exceptions.domain_errors import UnsolvableDomainError

from tests.golden_master_scenarios import GOLDEN_MASTER_SCENARIOS, GoldenMasterScenario

DEFAULT_GOLDEN_MASTER_PATH = (
    Path(__file__).resolve().parent / "golden_master_expected.txt"
)
SECTION_SEPARATOR = "________________________________________"


def format_grid(grid: list[list[int]]) -> str:
    """Render a 4×4 grid as space-separated rows for golden master files.

    Args:
        grid: 4×4 integer matrix.

    Returns:
        Multi-line string with one row per line.
    """
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def format_output_data(data: list[int]) -> str:
    """Serialize success ``int[6]`` in canonical comma-separated form.

    Args:
        data: Six-element result ``[r1, c1, n1, r2, c2, n2]``.

    Returns:
        Bracketed comma-separated values without spaces.
    """
    return "[" + ",".join(str(value) for value in data) + "]"


def capture_scenario_section(
    boundary: UIBoundary, scenario: GoldenMasterScenario
) -> str:
    """Capture one scenario's Input/Output or Input/Error block.

    Success and validation failures come from ``UIBoundary.solve`` DTOs.
    ``UnsolvableDomainError`` is serialized as ``E006`` per PRD §12.3 contract.

    Args:
        boundary: Boundary entry point under test.
        scenario: Scenario definition with grid input.

    Returns:
        Section body (without ``[name]`` header).
    """
    input_block = f"Input:\n{format_grid(scenario.grid)}"

    try:
        result = boundary.solve(scenario.grid)
    except UnsolvableDomainError:
        return f"{input_block}\nError:\nE006"

    if isinstance(result, SuccessResponse):
        return f"{input_block}\nOutput:\n{format_output_data(result.data)}"

    if isinstance(result, FailureResponse):
        return f"{input_block}\nError:\n{result.error.code}"

    raise TypeError(f"Unexpected result type: {type(result)!r}")


def build_golden_master_document(boundary: UIBoundary) -> str:
    """Build the full golden master expected file from all scenarios.

    Args:
        boundary: Boundary entry point used to capture live output.

    Returns:
        Complete golden master document text.
    """
    sections: list[str] = []
    for index, scenario in enumerate(GOLDEN_MASTER_SCENARIOS):
        body = capture_scenario_section(boundary, scenario)
        sections.append(f"[{scenario.name}]\n{body}")
        if index < len(GOLDEN_MASTER_SCENARIOS) - 1:
            sections.append(SECTION_SEPARATOR)
    return "\n\n".join(sections) + "\n"


def approve_golden_master(
    actual: str,
    expected_path: Path,
    *,
    auto_create: bool = True,
    force_update: bool = False,
) -> str:
    """Compare or create golden master baseline using the approve pattern.

    When ``expected_path`` is missing and ``auto_create`` is True, writes
    ``actual`` to disk and returns ``"created"``. When ``force_update`` is
    True, overwrites the baseline with ``actual`` and returns ``"updated"``.
    Otherwise compares byte-for-byte and raises ``AssertionError`` on mismatch
    with a unified diff.

    Args:
        actual: Newly captured golden master document.
        expected_path: Path to the baseline file.
        auto_create: Create baseline when the file does not exist.
        force_update: Overwrite baseline unconditionally (approve mode).

    Returns:
        ``"matched"``, ``"created"``, or ``"updated"``.

    Raises:
        AssertionError: When baseline exists, differs, and ``force_update`` is
            False.
        FileNotFoundError: When baseline is missing and ``auto_create`` is
            False.
    """
    existed = expected_path.exists()
    if force_update or (not existed and auto_create):
        expected_path.write_text(actual, encoding="utf-8")
        if force_update and existed:
            return "updated"
        return "created"

    if not expected_path.exists():
        raise FileNotFoundError(
            f"Golden master baseline not found: {expected_path}. "
            "Run with --approve-golden or scripts/generate_golden_master.py."
        )

    expected = expected_path.read_text(encoding="utf-8")
    if actual == expected:
        return "matched"

    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=str(expected_path),
        tofile="actual",
    )
    raise AssertionError(
        "Golden master mismatch — run approve to update baseline:\n"
        + "".join(diff)
    )
