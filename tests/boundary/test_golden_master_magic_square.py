"""GM-2 Golden Master regression tests for MagicSquareBoundary.solve()."""

from __future__ import annotations

from pathlib import Path

import pytest

from magicsquare.boundary.magic_square_boundary import MagicSquareBoundary
from tests.golden_master_helper import (
    GOLDEN_MASTER_PATH,
    GOLDEN_SCENARIOS,
    GoldenCapture,
    GoldenScenario,
    SCENARIO_BY_KEY,
    assert_golden_master,
    assert_golden_scenario,
    capture_all_scenarios,
    capture_scenario,
    parse_golden_master,
    render_golden_master,
    unified_section_diff,
    write_golden_master,
)

pytestmark = pytest.mark.golden_master


def _scenario(test_id: str) -> GoldenScenario:
    return next(item for item in GOLDEN_SCENARIOS if item.test_id == test_id)


class TestGoldenMasterMagicSquare:
    """[TAG][GoldenMaster] GM-2 scenario regression suite."""

    def test_gm_tc_01_normal_success(self, boundary: MagicSquareBoundary) -> None:
        """[TAG][GoldenMaster] GM-TC-01 정상 조합 성공 (small-first)."""
        assert_golden_scenario(_scenario("GM-TC-01"), boundary)

    def test_gm_tc_02_reverse_success(self, boundary: MagicSquareBoundary) -> None:
        """[TAG][GoldenMaster] GM-TC-02 reverse 조합 성공."""
        assert_golden_scenario(_scenario("GM-TC-02"), boundary)

    def test_gm_tc_03_invalid_blank_count(self, boundary: MagicSquareBoundary) -> None:
        """[TAG][GoldenMaster] GM-TC-03 INVALID_BLANK_COUNT."""
        assert_golden_scenario(_scenario("GM-TC-03"), boundary)

    def test_gm_tc_04_duplicate_number(self, boundary: MagicSquareBoundary) -> None:
        """[TAG][GoldenMaster] GM-TC-04 DUPLICATE_NUMBER."""
        assert_golden_scenario(_scenario("GM-TC-04"), boundary)

    def test_gm_tc_05_no_valid_magic_square(
        self, boundary: MagicSquareBoundary
    ) -> None:
        """[TAG][GoldenMaster] GM-TC-05 NO_VALID_MAGIC_SQUARE."""
        assert_golden_scenario(_scenario("GM-TC-05"), boundary)

    def test_gm_all_scenarios_baseline_file(self, boundary: MagicSquareBoundary) -> None:
        """[TAG][GoldenMaster] Full baseline file approve compare."""
        assert_golden_master(boundary=boundary)


class TestGoldenMasterApprovePattern:
    """Approve-pattern infrastructure checks."""

    def test_auto_generate_when_baseline_missing(
        self,
        boundary: MagicSquareBoundary,
        tmp_path: Path,
    ) -> None:
        target = tmp_path / "golden_master_expected.txt"
        generated: Path | None = None

        def record_generated(path: Path) -> None:
            nonlocal generated
            generated = path

        assert_golden_master(path=target, boundary=boundary, on_missing=record_generated)
        assert generated == target
        assert target.exists()
        assert parse_golden_master(target.read_text(encoding="utf-8"))

    def test_mismatch_reports_unified_diff(
        self,
        boundary: MagicSquareBoundary,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        target = tmp_path / "golden_master_expected.txt"
        write_golden_master(target)

        actual = capture_all_scenarios(boundary)
        scenario_key = GOLDEN_SCENARIOS[0].key
        mutated = GoldenCapture(
            kind=actual[scenario_key].kind,
            input_text=actual[scenario_key].input_text,
            body="[9, 9, 9, 9, 9, 9]",
        )
        expected_captures = dict(actual)
        expected_captures[scenario_key] = mutated
        target.write_text(render_golden_master(expected_captures), encoding="utf-8")

        monkeypatch.setenv("GOLDEN_MASTER_APPROVE", "0")

        with pytest.raises(AssertionError) as exc_info:
            assert_golden_master(path=target, boundary=boundary)

        message = str(exc_info.value)
        assert "Golden Master mismatch." in message
        assert "---" in message
        assert "+++" in message
        assert "@@" in message
        assert unified_section_diff(
            scenario_key,
            mutated,
            actual[scenario_key],
        ) in message


@pytest.mark.parametrize(
    "scenario_key",
    [scenario.key for scenario in GOLDEN_SCENARIOS],
    ids=[scenario.test_id for scenario in GOLDEN_SCENARIOS],
)
def test_committed_baseline_section_exists(scenario_key: str) -> None:
    sections = parse_golden_master(GOLDEN_MASTER_PATH.read_text(encoding="utf-8"))
    assert scenario_key in sections
    assert SCENARIO_BY_KEY[scenario_key].key == scenario_key
