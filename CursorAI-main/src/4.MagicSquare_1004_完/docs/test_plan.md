# Magic Square 4×4 — 테스트 계획서

| 항목 | 내용 |
|------|------|
| **문서 ID** | TP-MS-001 |
| **앵커 AC** | AC-FR01-01 (`matrix == null` → E003, Domain 0회) |
| **PRD 참조** | FR-01 (§10), §12.1·§12.3, §13.1, BR-01·BR-05, NFR-01·NFR-02 |
| **기술 스택** | Python 3.11+, pytest, pydantic, unittest.mock |
| **작성 기준** | `docs/PRD_MagicSquare.md` v0.2 (SSOT) |
| **작성일** | 2026-05-24 |

---

## 1. 목적 및 범위

본 계획서는 **FR-01 Input Verification (Boundary)** 의 선행 AC인 **AC-FR01-01**을 앵커로, 입력 유효성 검사 및 **Domain 진입점(`SolvePartialMagicSquare.execute`) 호출 격리**를 pytest 단위 테스트로 검증하는 범위·우선순위·측정 전략을 정의한다.

### 1.1 In-Scope

| 구분 | 대상 | 설명 |
|------|------|------|
| **Track A (Boundary)** | `InputValidator`, `UIBoundary` | E001·E003 반환, Failure schema, Domain 0회 |
| **흐름 검증** | U-FLOW-02 | invalid 입력 시 Control Mock 0회 호출 |
| **계약 모델** | pydantic Error/Success schema | `type`, `error.code`, `error.message` 불변 |

### 1.2 Out-of-Scope (본 앵커 AC 범위 외 — 포함 금지)

| 항목 | 사유 | 해당 AC |
|------|------|---------|
| **4×4 유효 격자 (G1 등)** | 검증 통과 → Domain 1회 호출 시나리오 | AC-FR01-07, U-FLOW-01 |
| 빈칸 개수·값 범위·중복 검증 | FR-01 후속 검증 단계 | AC-FR01-04~06 |
| Domain Solver·Validator 로직 | Track B (Logic Track) | D-VAL-*, D-SOL-* |
| E2E Integration | IT-01, IT-E* | 별도 Integration Test Plan |

> **용어 정리:** PRD SSOT 기준 `null` 입력은 **E003** (`INVALID_MATRIX_NULL`). 크기 불일치는 **E001** (`INVALID_MATRIX_SIZE: expected 4x4`). 요청 문맥의 `INVALID_SIZE`는 E001 크기 위반 코드에 해당하며, `grid=None` 앵커 케이스는 E003이다.

---

## 2. pytest 단위 테스트 범위 및 우선순위

Dual-Track TDD 원칙에 따라 **Track A(Boundary)를 우선** 실행한다. Domain Mock은 Boundary 테스트에서만 허용한다.

### 2.1 우선순위 매트릭스

| 우선순위 | Test ID | 테스트 파일 (예정) | 검증 대상 | AC / BR |
|----------|---------|------------------|-----------|---------|
| **P0** | U-IN-01 | `tests/boundary/test_input_validator.py` | `matrix=None` → E003, message exact | AC-FR01-01 |
| **P0** | U-FLOW-02 | `tests/boundary/test_ui_boundary.py` | invalid 입력 → `execute` **0회** | AC-FR01-01, AC-FR01-08, BR-05 |
| **P1** | U-IN-02 | `tests/boundary/test_input_validator.py` | 행 수 ≠ 4 → E001 | AC-FR01-02 |
| **P1** | U-IN-03 | `tests/boundary/test_input_validator.py` | 열 수 ≠ 4 → E001 | AC-FR01-03 |
| **P2** | U-FLOW-02 (확장) | `tests/boundary/test_ui_boundary.py` | size 위반 입력도 Domain 0회 | AC-FR01-08 |
| **P3** | — | `tests/boundary/test_error_schema.py` | pydantic Failure envelope 직렬화 | BR-20, UX-02 |

### 2.2 RED → GREEN 권장 순서

```
1. U-IN-01  (null → E003)           ← AC-FR01-01 앵커
2. U-FLOW-02 (null → execute 0회)
3. U-IN-02  (3×4, 5×5, [] → E001)
4. U-IN-03  ([[]]*4, 4×3 → E001)
5. U-FLOW-02 확장 (size 위반 → execute 0회)
```

### 2.3 테스트 패턴 (AAA)

모든 단위 테스트는 **Arrange–Act–Assert** 패턴을 따른다.

```python
# Arrange — invalid matrix fixture
# Act   — InputValidator.validate(matrix) 또는 UIBoundary.solve(matrix)
# Assert — error code, message exact match, execute.call_count == 0
```

### 2.4 Naming Convention

| 규칙 | 예시 |
|------|------|
| 파일 | `test_<component>.py` |
| 함수 | `test_<test_id>_<scenario>` |
| 예 | `test_u_in_01_null_matrix_returns_e003` |

---

## 3. 경계값 케이스 목록

FR-01 Processing Rule 6: **null → size → empty count → value range → duplicate**

본 절의 케이스는 **null·size 검증 단계**에 한정한다. 4×4 정상 입력은 **포함하지 않는다.**

### 3.1 null 입력 (AC-FR01-01)

| # | 입력 | 기대 code | 기대 message | Domain 호출 |
|---|------|-----------|--------------|-------------|
| BV-01 | `matrix = None` | **E003** | `INVALID_MATRIX_NULL: matrix must not be null` | **0회** |

### 3.2 행/열 크기 불일치 (AC-FR01-02, AC-FR01-03)

| # | 입력 | 기대 code | 기대 message | Domain 호출 | 비고 |
|---|------|-----------|--------------|-------------|------|
| BV-02 | `matrix = []` | **E001** | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | `len(matrix)==0` |
| BV-03 | `matrix = [[]] * 4` | **E001** | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | 행 4개, 각 행 `len==0` |
| BV-04 | 3×4 격자 (행 3, 열 4) | **E001** | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | AC-FR01-02 |
| BV-05 | 4×3 격자 (행 4, 열 3) | **E001** | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | AC-FR01-03 |
| BV-06 | 5×5 격자 | **E001** | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | 행·열 모두 초과 |

#### BV-04~BV-06 구체 입력 예시

```python
# BV-04: 3×4
matrix_3x4 = [[1]*4, [2]*4, [3]*4]

# BV-05: 4×3
matrix_4x3 = [[1, 2, 3]] * 4

# BV-06: 5×5
matrix_5x5 = [[1]*5 for _ in range(5)]
```

### 3.3 검증 순서(Short-circuit) 경계

| # | 입력 | 기대 | 근거 |
|---|------|------|------|
| BV-07 | `None` + (가상 size 위반 혼합 불가) | E003 (E001 아님) | null 검사가 size보다 선행 |
| BV-08 | `[]` (null 아님) | E001 (E003 아님) | null 통과 후 size 검사 진입 |

### 3.4 명시적 제외 케이스

| 입력 | 제외 사유 |
|------|-----------|
| G1 (4×4, 빈칸 2개, 유효 값) | AC-FR01-07 범위 — Domain **1회** 호출 시나리오 |
| 4×4 + 빈칸 1개/3개 | AC-FR01-04 — empty count 단계 (본 계획 후속) |
| 4×4 + 값 17 / 중복 | AC-FR01-05~06 — value/duplicate 단계 (본 계획 후속) |

---

## 4. 예외·특이 케이스 목록

| ID | 시나리오 | 입력/조건 | 기대 동작 | Test ID |
|----|----------|-----------|-----------|---------|
| EX-01 | 명시적 `None` | `UIBoundary.solve(None)` | E003, execute 0회 | U-IN-01, U-FLOW-02 |
| EX-02 | 빈 리스트 `[]` | `len==0` | E001 (null 아님) | U-IN-02 |
| EX-03 | `[[]] * 4` 행 별칭 | 4행 존재, 열 0 | E001; **첫 번째 행** `len!=4`에서 즉시 실패 | U-IN-03 |
| EX-04 | `[None] * 4` | 행 원소가 list가 아님 | E001 또는 TypeError — **구현 전 RED에서 계약 확정** | U-IN-02 (후보) |
| EX-05 | `matrix[2] = None` (부분 null 행) | 4행 중 1행 None | E001 (`len(None)` TypeError 방어) | U-IN-03 (후보) |
| EX-06 | jagged array | `[[1,2,3,4], [1,2,3], [1,2,3,4], [1,2,3,4]]` | E001 — 2행째 `len==3` | U-IN-03 |
| EX-07 | pydantic 직렬화 | E003/E001 ErrorResponse | `type=="ERROR"`, `error` 필드만; `data` 없음 | schema test |
| EX-08 | Success/Failure 혼재 금지 | E003 응답 | `data` 키 **부재** (UX-05) | U-IN-01 |
| EX-09 | message 불변 | E001~E003 | 대소문자·구두점 **완전 일치** (RG-01) | U-IN-* |
| EX-10 | null vs size 동시 후보 불가 | `None` | E003만 반환; size 검사 미진입 | AC-FR01-08 |

---

## 5. Domain 해결 진입점 호출 횟수 검증 전략

### 5.1 검증 대상

| 진입점 | 레이어 | 역할 |
|--------|--------|------|
| `SolvePartialMagicSquare.execute(grid: Grid)` | Control | Domain 오케스트레이션 단일 진입점 |

Boundary invalid 입력 시 **execute는 0회** 호출되어야 한다 (BR-05).

### 5.2 Mock / Spy 전략

Track A 규칙: **Control/Entity Mock 허용**. Domain Logic Track에서는 Mock **금지**.

#### 5.2.1 U-IN-* (InputValidator 단독)

| 항목 | 전략 |
|------|------|
| Mock 필요 | **없음** |
| 이유 | `InputValidator`는 pure validation; Control 미호출 |
| Assert | `ValidationResult.is_error`, `code`, `message` |

#### 5.2.2 U-FLOW-02 (UIBoundary + Mock Spy)

```python
from unittest.mock import MagicMock

# Arrange
mock_execute = MagicMock()
boundary = UIBoundary(solve_use_case=SolvePartialMagicSquare(execute=mock_execute))
# 또는 patch:
# with patch("src.control.solve_partial_magic_square.SolvePartialMagicSquare.execute") as mock_execute:

# Act
result = boundary.solve(None)  # BV-01

# Assert
mock_execute.assert_not_called()
assert result.type == "ERROR"
assert result.error.code == "E003"
```

| 검증 포인트 | 방법 |
|-------------|------|
| 호출 횟수 | `mock_execute.assert_not_called()` 또는 `call_count == 0` |
| 호출 인자 | invalid 시 `call_args` **없음** |
| size 위반 확장 | BV-02~BV-06 각각 `assert_not_called()` |
| valid 입력 (범위 외) | `assert_called_once()` — **별도 U-FLOW-01** |

#### 5.2.3 Spy vs Mock 선택 기준

| 도구 | 사용 시점 |
|------|-----------|
| `MagicMock` | UIBoundary가 주입받는 Control port 대체 (권장) |
| `patch` | UIBoundary 내부에서 Control을 직접 생성하는 경우 |
| `wraps=` (spy) | 실제 execute 부수효과 관찰 필요 시 (본 FR-01 범위에서는 불필요) |

### 5.3 금지 사항

- Logic Track (`tests/entity/`)에서 Domain Service Mock 사용 금지
- assert 완화·skip·xfail로 Domain 호출 횟수 검증 우회 금지
- invalid 입력에서 execute가 1회라도 호출되면 **테스트 FAIL** (BR-05 위반)

---

## 6. 커버리지 목표

PRD §14 NFR-01·NFR-02 및 `.cursorrules` 기준.

| 레이어 | 경로 | Line Coverage 목표 | Gate |
|--------|------|-------------------|------|
| **Domain (Entity + Control)** | `src/entity/`, `src/control/` | **≥ 95%** | Logic Track GREEN + REFACTOR |
| **Boundary** | `src/boundary/` | **≥ 85%** | Track A GREEN + REFACTOR |
| **전역** | `src/` | **≥ 80%** | REFACTOR phase gate (NFR-03) |

### 6.1 본 계획(앵커 AC) 기대 커버리지 기여

| 모듈 | 기대 커버 대상 |
|------|----------------|
| `input_validator.py` | null 분기, size 분기 (행·열) |
| `ui_boundary.py` | validate 실패 시 early return, execute 미호출 경로 |
| `error_schema.py` (pydantic) | E001, E003 Failure envelope |

> AC-FR01-01~03만으로 Boundary 85% 전체 달성은 불가능하다. 후속 AC-FR01-04~06(U-IN-04~08) 및 U-OUT-*로 보완한다.

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest-cov
```

### 7.2 전역 측정 (CI·REFACTOR gate)

```bash
pytest --cov=src --cov-report=term-missing
```

| 옵션 | 목적 |
|------|------|
| `--cov=src` | production 코드 전체 측정 |
| `--cov-report=term-missing` | 미커버 라인 번호 출력 → RED/GREEN 대상 식별 |

### 7.3 Dual-Track 분리 측정 (NFR-01·NFR-02)

```bash
# Boundary Track (Track A)
pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing --cov-fail-under=85

# Domain Track (Track B)
pytest tests/entity/ tests/control/ --cov=src/entity --cov=src/control \
  --cov-report=term-missing --cov-fail-under=95
```

### 7.4 앵커 AC 전용 스모크 (개발 중)

```bash
# FR-01 null·size 검증만 실행
pytest tests/boundary/test_input_validator.py -k "u_in_01 or u_in_02 or u_in_03" -v

# Domain 0회 호출 검증
pytest tests/boundary/test_ui_boundary.py -k "u_flow_02" -v
```

### 7.5 커버리지 해석 규칙

| 규칙 | 설명 |
|------|------|
| 측정 대상 | `src/` only; `tests/` 제외 |
| REFACTOR gate | 전역 ≥ 80%, Boundary ≥ 85%, Domain ≥ 95% **동시** 충족 |
| 미커버 허용 | `__init__.py` re-export, unreachable defensive branch (문서화 필수) |
| 회귀 | REFACTOR 후 E001~E003 message 변경 시 U-IN-* **전부** 갱신 (§13.3) |

### 7.6 (선택) HTML 리포트

```bash
pytest --cov=src --cov-report=html
# htmlcov/index.html
```

---

## 8. 테스트 데이터·Fixture 전략

| Fixture | Scope | 용도 |
|---------|-------|------|
| `matrix_none` | function | BV-01 |
| `matrix_empty` | function | BV-02 |
| `matrix_four_empty_rows` | function | BV-03 (`[[]]*4`) |
| `matrix_3x4`, `matrix_4x3`, `matrix_5x5` | function | BV-04~BV-06 |
| `expected_e003`, `expected_e001` | module | message SSOT 상수 |

**주의:** `[[]]*4`는 행 객체가 동일 참조를 공유한다. mutation 테스트 시 function scope fixture를 사용하고 테스트 간 공유하지 않는다.

---

## 9. Exit Criteria (본 계획 완료 조건)

| # | 조건 | 검증 |
|---|------|------|
| EC-01 | BV-01~BV-08 전부 GREEN | pytest |
| EC-02 | EX-01~EX-03, EX-07~EX-10 GREEN | pytest |
| EC-03 | U-FLOW-02: null·size invalid → execute 0회 | mock assert |
| EC-04 | E003·E001 message PRD §12.3과 **완전 일치** | assert |
| EC-05 | `src/boundary/input_validator.py` null·size 분기 커버 | term-missing |
| EC-06 | 4×4 유효 입력 테스트 **본 계획 범위에 미포함** 확인 | scope review |

---

## 10. Traceability

| AC ID | Business Rule | Boundary Case | Test ID |
|-------|---------------|---------------|---------|
| AC-FR01-01 | BR-05 | BV-01 | U-IN-01, U-FLOW-02 |
| AC-FR01-02 | BR-01, BR-05 | BV-02, BV-04, BV-06 | U-IN-02 |
| AC-FR01-03 | BR-01, BR-05 | BV-03, BV-05 | U-IN-03 |
| AC-FR01-08 | BR-05 | BV-07, BV-08 | U-FLOW-02 |

---

## 11. 부록 — 기대 응답 Schema (pydantic)

### Failure (E003 — null)

```json
{
  "type": "ERROR",
  "error": {
    "code": "E003",
    "message": "INVALID_MATRIX_NULL: matrix must not be null"
  }
}
```

### Failure (E001 — size)

```json
{
  "type": "ERROR",
  "error": {
    "code": "E001",
    "message": "INVALID_MATRIX_SIZE: expected 4x4"
  }
}
```

---

*본 문서는 AC-FR01-01 앵커 기준 FR-01 null·size 입력 검증 테스트 계획이다. 후속 FR-01 AC(빈칸·값·중복) 및 Track B Domain 테스트는 별도 계획으로 확장한다.*
