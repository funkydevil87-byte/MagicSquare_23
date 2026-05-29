# MagicSquare TDD — 상세 참조

## 에러 코드 (Boundary)

| 코드 | 조건 | Domain 호출 |
|------|------|-------------|
| E001 | 4×4 형식 아님 | 0회 |
| E002 | 빈칸 개수 ≠ 2 | 0회 |
| E003 | 값 범위 위반 (0, 1~16 외) | 0회 |
| E004 | 좌표/형식 오류 | 0회 |
| E005 | 0 제외 중복 숫자 | 0회 |
| E006 | Domain 해결 불가 (`UnsolvableDomainError`) | 호출 후 |
| E007 | 내부/예상치 못한 오류 | — |

invalid 입력 시 Domain은 **절대 호출하지 않는다** (U-FLOW-02 Domain Isolation).

---

## 불변식 I1~I11

| ID | 내용 | 검증 주체 |
|----|------|-----------|
| I1 | 모든 행 합 = M | MagicSquareValidator |
| I2 | 모든 열 합 = M | MagicSquareValidator |
| I3 | 주·부대각 합 = M | MagicSquareValidator |
| I4 | 값 집합 = {1..16} 각 1회 | MagicSquareValidator |
| I5 | M = 34 | MagicConstant |
| I6 | 빈칸 2개, 행 우선 1-index | EmptyCellLocator |
| I7 | 누락 = {1..16} \ present, 2개 | MissingNumberFinder |
| I8 | Step A 성공 → (n1,n2)=(smaller,larger) | TwoCellSolver |
| I9 | Step B 성공 → (n1,n2)=(larger,smaller) | TwoCellSolver |
| I10 | 두 조합 모두 실패 → UnsolvableDomainError | TwoCellSolver |
| I11 | 0은 빈칸만, 누락 후보 제외 | MissingNumberFinder |

---

## 테스트 ID → 파일 매핑

### Logic Track (Domain)

| Test ID | 파일 | 대상 컴포넌트 |
|---------|------|---------------|
| D-VAL-01~06 | `tests/entity/test_d_val_01_06_magic_square_validator.py` | MagicSquareValidator |
| D-LOC-01 | `tests/entity/test_d_loc_01_empty_cell_locator.py` | EmptyCellLocator |
| D-MIS-01 | `tests/entity/test_d_mis_01_missing_number_finder.py` | MissingNumberFinder |
| D-SOL-01~04 | `tests/entity/test_d_sol_01_04_two_cell_solver.py` | TwoCellSolver |
| — | `tests/control/test_solve_partial_magic_square.py` | SolvePartialMagicSquare |

### UI Contract Track (Boundary)

| Test ID | 파일 | 검증 내용 |
|---------|------|-----------|
| U-IN-01~08 | `tests/boundary/test_u_in_04_08_input_validation.py` | E001~E005 입력 검증 |
| U-OUT-01~03 | `tests/boundary/test_u_out_01_03_output_contract.py` | int[6] 출력 계약 |
| U-FLOW-02 | `tests/boundary/test_u_flow_02_domain_isolation.py` | invalid 시 Domain 0회 호출 |
| AC-FR-01-01 | `tests/boundary/test_ac_fr_01_01_*.py` | UI 수용 기준 |

### Golden Master

| Test ID | 파일 |
|---------|------|
| GM-01 | `tests/test_gm_01_magic_square_golden_master.py` |

---

## 컴포넌트 → 경로

```
src/entity/
├── grid.py
├── value_objects/
│   ├── cell_coordinate.py
│   ├── empty_cell_pair.py
│   ├── missing_number_pair.py
│   ├── magic_constant.py
│   └── solution_result.py
├── services/
│   ├── empty_cell_locator.py
│   ├── missing_number_finder.py
│   ├── magic_square_validator.py
│   └── two_cell_solver.py
└── exceptions/domain_errors.py

src/control/
└── solve_partial_magic_square.py

src/boundary/
├── ui_boundary.py
├── input_validator.py
├── error_mapper.py
├── schemas.py
└── screen/          # PyQt6 GUI (optional)
```

---

## Golden Master 시나리오

| 시나리오 | 기대 |
|----------|------|
| normal_success | int[6] `[3,3,1,4,4,6]` |
| reverse_success | int[6] `[2,2,7,3,3,10]` |
| invalid_blank_count | E002 |
| duplicate_number | E005 |
| no_valid_solution | E006 |

---

## AAA 테스트 템플릿

```python
def test_d_val_01_row_sum_equals_magic_constant(g1_complete_grid: list[list[int]]) -> None:
    # Arrange
    validator = MagicSquareValidator()

    # Act
    result = validator.is_valid(g1_complete_grid)

    # Assert
    assert result is True
```

---

## 추적 체인

```
Concept → Rule(I*) → Use Case(UC-*) → Contract(E*) → Test ID(D-*/U-*) → Component
```

새 기능 추가 시 Report 테스트 ID와 pytest 함수명을 1:1로 대응시킨다.
