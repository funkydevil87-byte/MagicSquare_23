# Magic Square — 테스트 계획서 (Track A: FR-01 / AC-FR01-03)

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.0 |
| 기준일 | 2026-05-29 |
| 기준 PRD | `docs/PRD_MagicSquare.md` v1.1 |
| 앵커 AC | **AC-FR01-03** (부가: AC-FR01-01, AC-FR01-02) |
| 기술 스택 | Python 3.13+, pytest, pydantic, unittest.mock |
| Track | **Track A — Boundary / Contract TDD** |

---

## 1. 목적 및 범위

본 계획서는 FR-01(Input Verification, Boundary)의 **선행 조건인 입력 유효성 검사**를 pytest 단위 테스트로 고정하기 위한 문서이다. 샘플 앵커는 **AC-FR01-03** (`matrix = null` → `NULL_INPUT`)이며, 동일 Track A RED 사이클에서 **Domain 해 결정 진입점 미호출(AC-FR01-01)** 을 함께 검증한다.

### 1.1 In-Scope

- Boundary 계층 입력 계약 검증 (`BoundaryValidator` 및 공개 API 진입점)
- Error Code + Message 예외 throw 계약 (§13, DQ-03 확정)
- 계약 위반 시 Domain/Control solver 진입점 **0회 호출**
- 경계값·예외·특이 입력에 대한 FR-01 실패 분류

### 1.2 Out-of-Scope (본 계획서)

- **4×4 정상 입력** 및 성공 경로 (`int[6]` 반환) — AC-FR01-01 범위 외, **본 문서에 포함하지 않음**
- Domain 불변식(빈칸 탐색, 누락 숫자, 마방진 판정, Attempt 1/2) — Track B 별도 계획
- UI/DB/Web, N×N 일반화, 성능 측정(NFR) — 후속 단계

---

## 2. pytest 단위 테스트 범위 및 우선순위

### 2.1 테스트 대상 컴포넌트

| 우선순위 | 대상 | 패키지 경로 | 관련 FR/AC |
|:--------:|------|-------------|------------|
| **P0** | `BoundaryValidator` | `src/magicsquare/boundary/` | FR-01, AC-FR01-03~08 |
| **P0** | 공개 API (Boundary 진입점) | `src/magicsquare/boundary/` | AC-FR01-01, §13.1 |
| **P1** | Error Code enum / 예외 타입 | `src/magicsquare/boundary/` | AC-FR01-02 |
| **P1** | pydantic Error Contract 모델 | `src/magicsquare/boundary/` | §12.1, §13 Error schema |
| **P2** | Control 오케스트레이션 (검증 실패 단락) | `src/magicsquare/control/` | AC-FR01-01 |

> Domain(`entity`) 컴포넌트는 본 Track A RED 단계에서 **Mock 대상**이며, 직접 단위 테스트 범위에 포함하지 않는다.

### 2.2 테스트 파일 배치 (권장)

```
tests/
  boundary/
    test_boundary_validator.py      # P0: 순수 검증 로직
    test_boundary_api_contract.py   # P0: 공개 API + Domain 미호출
    test_error_contract.py          # P1: Error Code/Message pydantic 계약
  conftest.py                       # 공통 fixture, mock factory
```

### 2.3 우선순위별 RED Test ID

| 우선순위 | Test ID | AC | 검증 요약 |
|:--------:|---------|-----|-----------|
| **P0** | A-RED-01 | AC-FR01-03 | `grid=None` → `NULL_INPUT`, Domain 0회 |
| **P0** | A-RED-06 | AC-FR01-01 | 모든 계약 위반 입력 → Domain 0회 (공통 invariant) |
| **P1** | A-RED-02 | AC-FR01-04 | 행 개수 ≠ 4 → `INVALID_ROW_COUNT` |
| **P1** | A-RED-03 | AC-FR01-05 | jagged / 열 개수 ≠ 4 → `INVALID_COL_COUNT` |
| **P2** | A-RED-04 | AC-FR01-06 | 빈칸(0) 개수 ≠ 2 → `INVALID_EMPTY_COUNT` |
| **P2** | A-RED-05 | AC-FR01-07/08 | 범위/중복 위반 → `OUT_OF_RANGE` / `DUPLICATE_VALUE` |

### 2.4 테스트 작성 규칙

- **패턴**: AAA (Arrange → Act → Assert)
- **명명**: `test_<조건>_<기대결과>` (예: `test_null_grid_raises_null_input_without_domain_call`)
- **실패 신호**: sentinel/`int[6]` 실패 반환 **금지** — 예외 throw만 허용 (§13, RESOLVED-01)
- **메시지 검증**: PRD §13.1 표준 문구와 **완전 일치** (`==` 비교)
- **TDD 흐름**: RED 확인 → GREEN(최소 구현) → REFACTOR(동작 불변)

---

## 3. 경계값 케이스 목록

본 섹션은 FR-01 입력 검증의 경계값만 다룬다. **4×4 정상 입력은 AC-FR01-01(계약 위반 시 Domain 미호출) 검증 범위 밖이므로 의도적으로 제외**한다.

### 3.1 경계값 매트릭스

| # | 입력 (`grid`) | 분류 | 기대 Error Code | 기대 Message | 관련 AC | Domain 호출 |
|---|---------------|------|-----------------|--------------|---------|:-----------:|
| BV-01 | `None` | 명시적 null | `NULL_INPUT` | `입력이 null입니다` | AC-FR01-03 | 0 |
| BV-02 | `[]` | 행 0개 (빈 리스트) | `INVALID_ROW_COUNT` | `행 개수는 4여야 합니다` | AC-FR01-04 | 0 |
| BV-03 | `[[]] * 4` | 행 4, 열 0 (jagged/빈 열) | `INVALID_COL_COUNT` | `열 개수는 4여야 합니다` | AC-FR01-05 | 0 |
| BV-04 | 3×4 행렬 | 행 개수 3 | `INVALID_ROW_COUNT` | `행 개수는 4여야 합니다` | AC-FR01-04 | 0 |
| BV-05 | 4×3 행렬 | 열 개수 3 | `INVALID_COL_COUNT` | `열 개수는 4여야 합니다` | AC-FR01-05 | 0 |
| BV-06 | 5×5 행렬 | 행 개수 5 | `INVALID_ROW_COUNT` | `행 개수는 4여야 합니다` | AC-FR01-04 | 0 |

### 3.2 경계값 입력 예시 (Arrange용)

```python
# BV-01: AC-FR01-03 앵커
grid_none = None

# BV-02: 빈 리스트 — 행 개수 0
grid_empty = []

# BV-03: 행 존재, 열 없음 — jagged
grid_empty_cols = [[]] * 4

# BV-04: 3×4
grid_3x4 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

# BV-05: 4×3
grid_4x3 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]

# BV-06: 5×5
grid_5x5 = [[1, 2, 3, 4, 5] for _ in range(5)]
```

### 3.3 검증 순서 (FR-01 Processing Rules)

Boundary는 아래 **단락(short-circuit) 순서**로 검증한다. 테스트는 각 경계값이 **해당 단계에서 즉시 실패**함을 확인한다.

1. `matrix is None` → `NULL_INPUT` (BV-01)
2. `len(matrix) != 4` → `INVALID_ROW_COUNT` (BV-02, BV-04, BV-06)
3. 임의 행 `len(row) != 4` → `INVALID_COL_COUNT` (BV-03, BV-05)
4. *(본 계획서 범위 외)* 0 개수, 값 범위, 중복

> BV-02(`[]`)는 BV-01(null)과 구분하여 **null이 아닌 빈 컬렉션** 경계를 검증한다.

### 3.4 명시적 제외

| 입력 | 제외 사유 |
|------|-----------|
| 4×4 정상 입력 (예: TD-01 fixture) | AC-FR01-01은 **계약 위반** 시 Domain 미호출을 검증한다. 정상 입력은 성공 경로(U-T01)로 Track A 후속 또는 E2E에서 다룬다. |

---

## 4. 예외 / 특이 케이스 목록

FR-01 경계값 외, Boundary 계약 안정성을 위한 예외·특이 케이스이다.

| # | 케이스 ID | 입력 / 조건 | 기대 동작 | 관련 AC |
|---|-----------|-------------|-----------|---------|
| EX-01 | null vs empty 구분 | `None` vs `[]` | 서로 다른 Error Code (`NULL_INPUT` vs `INVALID_ROW_COUNT`) | AC-FR01-02, 03, 04 |
| EX-02 | jagged 혼합 | `[[1,2,3,4], [1,2,3], [1,2,3,4], [1,2,3,4]]` | `INVALID_COL_COUNT` (첫 위반 행에서 단락) | AC-FR01-05 |
| EX-03 | `[[]]*4` 참조 공유 | 동일 객체 4행 | 열 길이 0으로 `INVALID_COL_COUNT` | AC-FR01-05 |
| EX-04 | null 행 포함 | `[None, [1,2,3,4], ...]` × 4행 | 구현 정의: `TypeError` 또는 `INVALID_COL_COUNT` — **RED 전에 Boundary 정책 확정 필요** | Decision Needed |
| EX-05 | 비정형 타입 | `grid = "not a grid"` | Boundary에서 예외 throw, Domain 0회 | AC-FR01-01 |
| EX-06 | Error Message 완전 일치 | 모든 FR-01 실패 | 공백·문장부호·한글 문구 1자도 불일치 없음 | AC-FR01-02, 03~08 |
| EX-07 | 예외 타입 일관성 | 동일 Error Code | 항상 동일 Boundary 예외 클래스/속성 | AC-FR01-02 |
| EX-08 | pydantic 계약 위반 | `code`/`message` 필드 누락 mock | Boundary 내부 버그로 분류, 공개 API 노출 금지 | §12.2 성공 계약 위반 정책 준용 |
| EX-09 | Domain 예외 역류 금지 | 계약 위반 입력 | Domain 전용 예외(`UnsolvablePartialGridException` 등) **노출 없음** | §13.2 |
| EX-10 | 입력 불변 (NFR) | 계약 위반 호출 전후 | 입력 객체 변경 없음 (null 제외) | AC-NFR-04 |

---

## 5. Domain 해 결정 진입점 호출 횟수 검증 전략

### 5.1 검증 대상 (Mock/Spy)

| Mock 대상 | 역할 | 패치 경로 (권장) |
|-----------|------|------------------|
| `PartialMagicSquareSolver.solve` | Domain 해 결정 핵심 | `magicsquare.entity.partial_magic_square_solver.PartialMagicSquareSolver.solve` |
| 또는 `Solver.solve` | Control 오케스트레이션 | `magicsquare.control.solver.Solver.solve` |

> **원칙**: 테스트는 **호출자(Boundary/Control) 관점**에서 patch한다. *"Boundary가 검증 실패 시 Control/Domain을 호출하지 않는다"* 를 검증한다 (§13.1, AC-FR01-01).

### 5.2 전략 A — `unittest.mock.patch` (권장, P0)

```python
from unittest.mock import patch

@patch("magicsquare.control.solver.Solver.solve")
def test_null_grid_does_not_invoke_domain_solver(mock_solve, boundary_api):
    # Arrange
    grid = None

    # Act & Assert
    with pytest.raises(NullInputException) as exc_info:
        boundary_api.solve(grid)

    assert exc_info.value.code == "NULL_INPUT"
    assert exc_info.value.message == "입력이 null입니다"
    mock_solve.assert_not_called()
```

- **장점**: 호출 횟수 `assert_not_called()` / `assert_called_once()` 명시적
- **적용**: BV-01~BV-06 전체 + EX-01~EX-05

### 5.3 전략 B — `MagicMock` Spy (P1, Control 단위)

```python
from unittest.mock import MagicMock

def test_boundary_validator_short_circuits_before_control():
    control = MagicMock()
    validator = BoundaryValidator(control=control)

    validator.validate(None)

    control.solve.assert_not_called()
```

- Control을 생성자 주입하여 Boundary 단위에서 **격리 수준 높은** 검증
- Domain Mock 없이 Control spy만으로 AC-FR01-01 입증 가능

### 5.4 전략 C — `wraps` Spy (P2, 리그ression)

```python
from unittest.mock import patch, MagicMock

real_solver = PartialMagicSquareSolver()
spy = MagicMock(wraps=real_solver)

with patch.object(control, "domain_solver", spy):
    ...
```

- REFACTOR 단계에서 내부 위임 경로 변경 시 회귀 감지용
- Track A RED 초기에는 **전략 A**만으로 충분

### 5.5 AC-FR01-03 + AC-FR01-01 통합 검증 체크리스트

| 단계 | Assert |
|------|--------|
| Act | `boundary_api.solve(grid=None)` 호출 |
| 예외 | `NullInputException` (또는 동등 타입) raise |
| Code | `exc.value.code == "NULL_INPUT"` |
| Message | `exc.value.message == "입력이 null입니다"` |
| Domain | `mock_solve.call_count == 0` |
| 반환 | `int[6]` **반환 없음** (예외로만 종료) |

### 5.6 pydantic Error Contract 검증 (P1)

```python
from pydantic import BaseModel

class BoundaryErrorContract(BaseModel):
    code: str
    message: str

# 예외 객체를 contract로 파싱하여 code/message 스키마 고정
contract = BoundaryErrorContract(
    code=exc.value.code,
    message=exc.value.message,
)
```

- Error Code enum과 pydantic 모델을 연동하여 AC-FR01-02(유형별 고유 코드) 회귀 방지

---

## 6. 커버리지 목표

PRD §14 NFR 및 AC-NFR-01/02 기준.

| 계층 | 패키지 | 목표 | 근거 |
|------|--------|:----:|------|
| **Domain** | `src/magicsquare/entity/` | **≥ 95%** | AC-NFR-01, Track B 불변식 |
| **Boundary** | `src/magicsquare/boundary/` | **≥ 85%** | AC-NFR-02, Track A 계약 |
| Control | `src/magicsquare/control/` | ≥ 85% (권장) | 오케스트레이션 단락 경로 |

### 6.1 본 Track A RED 단계 기대 커버리지

| 파일/모듈 | RED 직후 최소 | GREEN 목표 |
|-----------|:-------------:|:----------:|
| `boundary_validator.py` | FR-01 null/size 분기 | **85%+** |
| `boundary` 예외/enum | Error Code 6종 | **85%+** |
| `entity` (Mock only) | 0% (호출 없음) | 변화 없음 |

> Domain 95%는 Track B GREEN 이후 달성. Track A RED에서는 Boundary 경로를 우선 채운다.

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest-cov
```

### 7.2 기본 측정 (로컬)

```bash
pytest --cov=src --cov-report=term-missing
```

### 7.3 계층별 분리 측정 (권장)

```bash
# Boundary only (Track A 목표 85%+)
pytest tests/boundary/ \
  --cov=src/magicsquare/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85

# Domain only (Track B 목표 95%+)
pytest tests/entity/ \
  --cov=src/magicsquare/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 7.4 HTML 리포트 (리뷰/CI용)

```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
# 산출물: htmlcov/index.html
```

### 7.5 측정 정책

| 정책 | 설명 |
|------|------|
| **측정 시점** | GREEN 달성 후, REFACTOR 전·후 각 1회 |
| **Branch coverage** | FR-01 단락 분기(null → row → col) 누락 방지를 위해 `--cov-branch` 권장 |
| **제외** | `__init__.py` re-export만 있는 파일은 omit 가능 |
| **실패 기준** | Boundary < 85% 또는 Domain < 95% → merge 차단 (CI gate) |
| **Mock 경로** | Mock된 Domain 코드는 호출되지 않으므로 Domain coverage는 Track B 테스트로만 상승 |

### 7.6 pyproject.toml 권장 설정 (후속)

```toml
[tool.coverage.run]
source = ["src/magicsquare"]
branch = true

[tool.coverage.report]
fail_under = 85
show_missing = true
```

---

## 8. 추적성 매트릭스 (본 계획서)

| Test ID | 입력 | Error Code | AC | BV/EX | Domain 호출 |
|---------|------|------------|-----|-------|:-----------:|
| A-RED-01 / U-T09 | `None` | `NULL_INPUT` | AC-FR01-03 | BV-01 | 0 |
| A-RED-02 / U-T02 | 3×4 | `INVALID_ROW_COUNT` | AC-FR01-04 | BV-04 | 0 |
| A-RED-02 | 5×5 | `INVALID_ROW_COUNT` | AC-FR01-04 | BV-06 | 0 |
| A-RED-02 | `[]` | `INVALID_ROW_COUNT` | AC-FR01-04 | BV-02 | 0 |
| A-RED-03 / U-T03 | `[[]]*4` | `INVALID_COL_COUNT` | AC-FR01-05 | BV-03 | 0 |
| A-RED-03 | 4×3 | `INVALID_COL_COUNT` | AC-FR01-05 | BV-05 | 0 |
| A-RED-06 | BV-01~06 전체 | *(각 Code)* | AC-FR01-01 | — | 0 |

---

## 9. 실행 순서 (QA Lead 권고)

1. **RED**: A-RED-01 (`grid=None`) 단독 실패 확인
2. **RED 확장**: BV-02~BV-06 parametrized 실패 확인
3. **GREEN**: `BoundaryValidator` null/row/col 최소 구현
4. **REFACTOR**: Error Code enum + pydantic contract 추출, 테스트 유지
5. **Coverage gate**: Boundary 85%+ 확인 후 Track B 착수

---

## 10. 참고 문서

- `docs/PRD_MagicSquare.md` — FR-01, §12.1, §13.1, §15.1, §16.2 ES-01
- `Report/02.MagicSquare_DualTrack_TDD_CleanArchitecture_Design.md` — U-T02~U-T09
- `.cursor/rules/magicsquare-tdd-testing.mdc` — RED→GREEN→REFACTOR, AAA
