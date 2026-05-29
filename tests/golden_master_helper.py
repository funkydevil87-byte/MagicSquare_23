"""Golden Master capture, serialization, and approve-pattern utilities."""

from __future__ import annotations

import ast
import difflib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

import pytest

from magicsquare.boundary.exceptions import UNSOLVABLE_CODE, BoundaryValidationError, UnsolvableError
from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary
from magicsquare.boundary.schemas import (
    DUPLICATE_VALUE_CODE,
    DUPLICATE_VALUE_MESSAGE,
    FailureResult,
    INVALID_EMPTY_COUNT_CODE,
    INVALID_EMPTY_COUNT_MESSAGE,
)
from magicsquare.entity.services.empty_cell_locator import EmptyCellLocator
from magicsquare.entity.services.missing_number_finder import MissingNumberFinder
from tests.boundary.conftest import GRID_DUPLICATE, GRID_THREE_BLANKS
from tests.conftest import GRID_G1, GRID_G3, GRID_TD01

GOLDEN_MASTER_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"
APPROVE_ENV_VAR = "GOLDEN_MASTER_APPROVE"
SECTION_SEPARATOR = "________________________________________"

OutcomeKind = Literal["success", "error"]
AttemptStrategy = Literal["small_first", "reverse"]
ErrorScenarioKind = Literal[
    "invalid_blank_count",
    "duplicate_number",
    "no_valid_solution",
]


@dataclass(frozen=True)
class GoldenScenario:
    """Single Golden Master scenario definition."""

    test_id: str
    key: str
    grid: list[list[int]]
    strategy: AttemptStrategy | ErrorScenarioKind


@dataclass(frozen=True)
class GoldenCapture:
    """Serialized solver outcome for one scenario."""

    kind: OutcomeKind
    input_text: str
    body: str


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario("GM-TC-01", "normal_success", GRID_TD01, "small_first"),
    GoldenScenario("GM-TC-02", "reverse_success", GRID_G1, "reverse"),
    GoldenScenario(
        "GM-TC-03",
        "invalid_blank_count",
        GRID_THREE_BLANKS,
        "invalid_blank_count",
    ),
    GoldenScenario("GM-TC-04", "duplicate_number", GRID_DUPLICATE, "duplicate_number"),
    GoldenScenario("GM-TC-05", "no_valid_solution", GRID_G3, "no_valid_solution"),
)

SCENARIO_BY_KEY: dict[str, GoldenScenario] = {
    scenario.key: scenario for scenario in GOLDEN_SCENARIOS
}

ERROR_CONTRACTS: dict[str, tuple[str, str]] = {
    "invalid_blank_count": (INVALID_EMPTY_COUNT_CODE, INVALID_EMPTY_COUNT_MESSAGE),
    "duplicate_number": (DUPLICATE_VALUE_CODE, DUPLICATE_VALUE_MESSAGE),
    "no_valid_solution": (UNSOLVABLE_CODE, UnsolvableError().message),
}


def parse_success_vector(body: str) -> list[int]:
    """Parse a serialized success vector from Golden Master text."""
    parsed = ast.literal_eval(body.strip())
    if not isinstance(parsed, list):
        raise ValueError("Success output must serialize to list[int].")
    return [int(value) for value in parsed]


def validate_success_contract(
    grid: list[list[int]],
    vector: list[int],
    strategy: AttemptStrategy,
) -> None:
    """Validate int[6] output, row-major blanks, 1-index, and attempt ordering."""
    if len(vector) != 6:
        raise AssertionError(f"Expected int[6], got length {len(vector)}: {vector}")

    r1, c1, n1, r2, c2, n2 = vector
    for label, value in (("r1", r1), ("c1", c1), ("r2", r2), ("c2", c2)):
        if not 1 <= value <= 4:
            raise AssertionError(f"{label} must be 1-indexed in 1..4, got {value}")

    for label, value in (("n1", n1), ("n2", n2)):
        if not 1 <= value <= 16:
            raise AssertionError(f"{label} must be in 1..16, got {value}")
    if n1 == n2:
        raise AssertionError(f"n1 and n2 must differ, got {vector}")

    locator = EmptyCellLocator()
    (expected_r1, expected_c1), (expected_r2, expected_c2) = locator.locate(grid)
    if (r1, c1, r2, c2) != (expected_r1, expected_c1, expected_r2, expected_c2):
        raise AssertionError(
            "Coordinates must follow row-major blank order "
            f"(expected {(expected_r1, expected_c1, expected_r2, expected_c2)}, "
            f"got {(r1, c1, r2, c2)})"
        )

    small, large = MissingNumberFinder().find_missing(grid)
    if strategy == "small_first":
        if (n1, n2) != (small, large):
            raise AssertionError(
                "Attempt 1 must use small-first ordering "
                f"(expected {(small, large)}, got {(n1, n2)})"
            )
    elif (n1, n2) != (large, small):
        raise AssertionError(
            "Attempt 2 must use reverse ordering "
            f"(expected {(large, small)}, got {(n1, n2)})"
        )


def validate_error_contract(
    scenario: GoldenScenario,
    boundary: MagicSquareBoundary,
) -> None:
    """Validate FailureResult or UnsolvableError contract for error scenarios."""
    expected_code, expected_message = ERROR_CONTRACTS[scenario.strategy]

    if scenario.strategy == "no_valid_solution":
        try:
            boundary.solve(scenario.grid)
        except UnsolvableError as exc:
            assert exc.code == expected_code
            assert exc.message == expected_message
            return
        raise AssertionError("Expected UnsolvableError for no_valid_solution scenario.")

    with pytest.raises(BoundaryValidationError) as exc_info:
        boundary.solve(scenario.grid)
    assert exc_info.value.code == expected_code
    assert exc_info.value.message == expected_message


def assert_scenario_contract(
    scenario: GoldenScenario,
    capture: GoldenCapture,
    boundary: MagicSquareBoundary,
) -> None:
    """Validate solver contract rules for one Golden Master scenario."""
    if capture.kind == "success":
        vector = parse_success_vector(capture.body)
        assert scenario.strategy in {"small_first", "reverse"}
        validate_success_contract(scenario.grid, vector, scenario.strategy)
        return

    validate_error_contract(scenario, boundary)


def read_expected_section(path: Path, scenario_key: str) -> str | None:
    """Return rendered expected section text from the baseline file."""
    if not path.exists():
        return None
    sections = parse_golden_master(path.read_text(encoding="utf-8"))
    capture = sections.get(scenario_key)
    if capture is None:
        return None
    return render_section(scenario_key, capture)


def assert_golden_scenario(
    scenario: GoldenScenario,
    boundary: MagicSquareBoundary,
    path: Path | None = None,
) -> None:
    """Approve-pattern compare for one scenario section (read vs actual)."""
    target = path or GOLDEN_MASTER_PATH
    actual_capture = capture_scenario(boundary, scenario)
    assert_scenario_contract(scenario, actual_capture, boundary)

    actual_text = render_section(scenario.key, actual_capture)
    expected_text = read_expected_section(target, scenario.key)

    if expected_text is None or not target.exists():
        _upsert_section(target, scenario.key, actual_capture)
        return

    if approve_enabled():
        _upsert_section(target, scenario.key, actual_capture)
        return

    if expected_text != actual_text:
        diff = difflib.unified_diff(
            expected_text.splitlines(),
            actual_text.splitlines(),
            fromfile=f"expected [{scenario.test_id}]",
            tofile=f"actual [{scenario.test_id}]",
            lineterm="",
        )
        joined = "\n".join(diff)
        raise AssertionError(
            f"Golden Master mismatch for {scenario.test_id}.\n"
            f"Set {APPROVE_ENV_VAR}=1 to regenerate {target.name}.\n\n"
            f"{joined}"
        )


def _upsert_section(path: Path, scenario_key: str, capture: GoldenCapture) -> None:
    """Insert or replace one scenario section in the baseline file."""
    if path.exists():
        sections = parse_golden_master(path.read_text(encoding="utf-8"))
    else:
        sections = {}
    sections[scenario_key] = capture
    ordered = {
        scenario.key: sections[scenario.key]
        for scenario in GOLDEN_SCENARIOS
        if scenario.key in sections
    }
    path.write_text(render_golden_master(ordered), encoding="utf-8")


def format_grid(grid: list[list[int]]) -> str:
    """Render a 4x4 grid as space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def capture_scenario(
    boundary: MagicSquareBoundary, scenario: GoldenScenario
) -> GoldenCapture:
    """Run the solver and serialize stdout-style output for one scenario."""
    input_text = format_grid(scenario.grid)
    try:
        result = boundary.solve(scenario.grid)
    except BoundaryValidationError as exc:
        return GoldenCapture(
            kind="error",
            input_text=input_text,
            body=exc.code,
        )
    except UnsolvableError as exc:
        return GoldenCapture(
            kind="error",
            input_text=input_text,
            body=exc.code,
        )

    return GoldenCapture(
        kind="success",
        input_text=input_text,
        body=str(result),
    )


def render_section(scenario_key: str, capture: GoldenCapture) -> str:
    """Render one Golden Master section block."""
    lines = [
        f"[{scenario_key}]",
        "Input:",
        capture.input_text,
    ]
    if capture.kind == "success":
        lines.extend(["Output:", capture.body])
    else:
        lines.extend(["Error:", capture.body])
    return "\n".join(lines)


def render_golden_master(captures: dict[str, GoldenCapture]) -> str:
    """Render the full Golden Master baseline file."""
    blocks = [
        render_section(key, captures[key])
        for key in (scenario.key for scenario in GOLDEN_SCENARIOS)
    ]
    return f"\n{SECTION_SEPARATOR}\n\n".join(blocks) + "\n"


def parse_golden_master(text: str) -> dict[str, GoldenCapture]:
    """Parse Golden Master baseline text into scenario captures."""
    sections: dict[str, GoldenCapture] = {}
    blocks = [
        block.strip()
        for block in text.split(SECTION_SEPARATOR)
        if block.strip()
    ]
    for block in blocks:
        header_match = re.match(r"^\[(?P<key>[a-z_]+)\]\s*\n", block)
        if header_match is None:
            raise ValueError(f"Invalid Golden Master section header: {block[:40]!r}")
        key = header_match.group("key")
        body = block[header_match.end() :]
        sections[key] = _parse_section_body(body)
    return sections


def _parse_section_body(body: str) -> GoldenCapture:
    normalized = body.strip()
    input_match = re.search(
        r"Input:\s*\n(?P<input>(?:\d+(?: \d+)*\n?)+)",
        normalized,
        re.MULTILINE,
    )
    if input_match is None:
        raise ValueError("Golden Master section is missing Input block.")

    input_text = input_match.group("input").strip()
    output_match = re.search(
        r"Output:\s*\n(?P<output>.+?)(?:\nError:|\Z)",
        normalized,
        re.DOTALL,
    )
    if output_match is not None:
        return GoldenCapture(
            kind="success",
            input_text=input_text,
            body=output_match.group("output").strip(),
        )

    error_match = re.search(r"Error:\s*\n(?P<error>.+)\Z", normalized, re.DOTALL)
    if error_match is None:
        raise ValueError("Golden Master section must contain Output or Error block.")

    return GoldenCapture(
        kind="error",
        input_text=input_text,
        body=error_match.group("error").strip(),
    )


def capture_all_scenarios(
    boundary: MagicSquareBoundary | None = None,
) -> dict[str, GoldenCapture]:
    """Capture all registered scenarios from the live solver."""
    solver = boundary or MagicSquareBoundary()
    return {
        scenario.key: capture_scenario(solver, scenario)
        for scenario in GOLDEN_SCENARIOS
    }


def write_golden_master(path: Path | None = None) -> Path:
    """Generate and write the Golden Master baseline file."""
    target = path or GOLDEN_MASTER_PATH
    content = render_golden_master(capture_all_scenarios())
    target.write_text(content, encoding="utf-8")
    return target


def approve_enabled() -> bool:
    """Return True when explicit approve mode is requested."""
    return os.environ.get(APPROVE_ENV_VAR, "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def unified_section_diff(
    scenario_key: str,
    expected: GoldenCapture,
    actual: GoldenCapture,
) -> str:
    """Build a unified diff for one scenario section."""
    expected_block = render_section(scenario_key, expected)
    actual_block = render_section(scenario_key, actual)
    diff_lines = difflib.unified_diff(
        expected_block.splitlines(),
        actual_block.splitlines(),
        fromfile=f"expected [{scenario_key}]",
        tofile=f"actual [{scenario_key}]",
        lineterm="",
    )
    return "\n".join(diff_lines)


def assert_golden_master(
    path: Path | None = None,
    boundary: MagicSquareBoundary | None = None,
    on_missing: Callable[[Path], None] | None = None,
) -> None:
    """Compare live solver output against Golden Master with approve semantics."""
    target = path or GOLDEN_MASTER_PATH
    actual_captures = capture_all_scenarios(boundary)

    if not target.exists():
        write_golden_master(target)
        if on_missing is not None:
            on_missing(target)
        return

    expected_text = target.read_text(encoding="utf-8")
    expected_captures = parse_golden_master(expected_text)

    if approve_enabled():
        write_golden_master(target)
        return

    failures: list[str] = []
    for scenario in GOLDEN_SCENARIOS:
        expected = expected_captures.get(scenario.key)
        actual = actual_captures[scenario.key]
        if expected is None:
            failures.append(f"Missing section [{scenario.key}] in {target.name}")
            continue
        if expected != actual:
            failures.append(
                unified_section_diff(scenario.key, expected, actual),
            )

    if failures:
        joined = "\n\n".join(failures)
        raise AssertionError(
            "Golden Master mismatch.\n"
            f"Set {APPROVE_ENV_VAR}=1 to regenerate {target.name}.\n\n"
            f"{joined}"
        )
