# MagicSquare 4x4 TDD Practice

## 1. Project Start Declaration

**MagicSquare_1004** 프로젝트는 4×4 부분 마방진(빈칸 2개) 문제를 도메인으로, **불변식(Invariant) 중심 설계·검증·구현 체계**를 TDD로 구축하는 학습 프로젝트입니다.

현재 단계는 **PRD 기반 TDD 시작 준비**입니다. PRD(`docs/PRD_MagicSquare.md`)와 Report 시리즈에서 고정한 입력/출력 계약, Domain 불변식(I1~I11), Dual-Track TDD 추적 구조를 바탕으로 개발을 시작합니다.

**RED**는 “실패하는 테스트를 먼저 작성하고, `pytest` 실행으로 **테스트 실패 상태를 확인하는 단계**”입니다. RED 단계에서는 production 구현 코드를 작성하지 않습니다.

**GREEN**은 RED에서 확인한 실패를 통과시키기 위한 **최소 구현 작업 후보**를 정의하는 단계이며, **REFACTOR**는 GREEN 이후 구조를 개선하는 **후보**만 기록합니다. REFACTOR는 GREEN이 유지되는 전제에서 수행합니다.

본 README는 단순 소개 문서가 아닙니다. **구현 전에 개발 방향과 Concept → Scenario → Test → Component 추적 구조를 고정**하는 시작 선언 및 TDD 개발 가이드입니다.

---

## 2. PRD Summary

### 프로젝트 목적

빈칸 2개가 있는 4×4 부분 격자를 입력받아, 누락된 두 숫자의 유효 배치를 결정하고 `int[6]` 형식의 좌표·값 결과를 반환하는 순수 로직 프로그램을 **Dual-Track TDD**로 완성합니다. 핵심 가치는 “정답 프로그램”이 아니라 **계약 기반 설계·검증·리팩토링 훈련**입니다.

### 학습 목표

| 영역 | 목표 |
|------|------|
| 불변식 중심 설계 | I1~I11을 컴포넌트·유스케이스에 귀속 |
| Dual-Track TDD | Logic Track(Domain Mock 금지) vs Boundary Track(Mock 허용) |
| 입출력 계약 | E001~E007, Input/Output schema 고정 |
| TDD 사이클 | RED(실패 확인) → GREEN(최소 구현) → REFACTOR(구조 개선) |
| 추적성 | Concept → Rule → Use Case → Contract → Test → Component |

### 핵심 도메인 규칙

| 규칙 | 내용 |
|------|------|
| 입력 형식 | 4×4 `int` 행렬 |
| 빈칸 표기 | `0` |
| 빈칸 개수 | 정확히 2개 |
| 값 범위 | `0` 또는 `1~16` |
| 중복 | `0`을 제외한 중복 숫자 불허 |
| 마방진 상수 | M = **34** (`MagicConstant` SSOT) |
| 빈칸 순서 | row-major 스캔으로 처음 발견되는 `0`이 첫 번째 빈칸 |
| 해결 전략 | Step A: (작은 누락→첫 빈칸, 큰 누락→둘째 빈칸) → 실패 시 Step B: 반대 조합 |
| Domain 실패 | 두 조합 모두 무효 → `UnsolvableDomainError` → Boundary E006 |

### 입력 계약

- 형식: `4×4 int[][]`
- `0` = 빈칸 (정확히 2개)
- 값: `0` 또는 `1~16`, `0` 제외 distinct
- 위반 시 Boundary에서 E001~E005 반환, **Domain 0회 호출**

### 출력 계약

- 형식: `int[6]` = `[r1, c1, n1, r2, c2, n2]`
- 좌표: **1-index** (`1 ≤ r, c ≤ 4`)
- `n1`, `n2`: 두 누락 숫자
- Step A 성공 시 `(n1, n2) = (smaller, larger)`; Step B 성공 시 `(n1, n2) = (larger, smaller)`

### 성공 기준

| ID | 기준 |
|----|------|
| SC-01 | 유효 입력 → `int[6]` 반환 |
| SC-02 | invalid 입력 → E001~E005; Domain 0회 호출 |
| SC-03 | Domain 해결 불가 → E006 |
| SC-04 | Domain Logic coverage ≥ 95% |
| SC-05 | REFACTOR 후 E001~E007 message·`int[6]` 형식 불변 |
| SC-06 | 정답·매직 넘버 하드코딩 금지 |
| SC-07 | I1~I11 각각 ≥1 Test ID 연결 |

---

## 3. TDD Development Flow

```
Scenario
  → Acceptance Criteria
  → RED Test ID
  → Test Skeleton
  → Run Test
  → Confirm Failure = RED
  → Minimal Implementation = GREEN
  → Structure Improvement = REFACTOR
```

| 단계 | 의미 |
|------|------|
| **Scenario** | Given-When-Then 형태로 검증할 행위·조건을 정의합니다. |
| **Acceptance Criteria** | Scenario를 테스트 가능한 단일 진술(통과/실패 판정 가능)로 분해합니다. |
| **RED Test ID** | 각 AC에 고유 테스트 식별자(`RED-BND-*`, `RED-DOM-*`)를 부여합니다. |
| **Test Skeleton** | AAA(Arrange-Act-Assert) 구조의 pytest 테스트 골격을 작성합니다. |
| **Run Test** | `python -m pytest`로 테스트를 실행합니다. |
| **Confirm Failure = RED** | 테스트가 **의도한 이유로 실패**하는지 확인합니다. production 코드 작성은 아직 하지 않습니다. |
| **Minimal Implementation = GREEN** | RED 실패를 통과시키기 위한 **최소 구현 작업 후보**를 수행합니다. |
| **Structure Improvement = REFACTOR** | GREEN을 유지한 채 구조·가독성·중복 제거 등 **개선 후보만** 기록·수행합니다. |

---

## 4. Development Methodology

### Dual-Track UI + Logic TDD

| Track | 테스트 경로 | Mock 정책 | RED ID 접두 |
|-------|-------------|-----------|-------------|
| **Track A — Boundary RED** | `tests/boundary/` | Control/Entity Mock **허용** | `RED-BND-*` |
| **Track B — Logic RED** | `tests/entity/` | Domain Mock **금지** | `RED-DOM-*` |
| **Integration RED** | `tests/test_integration.py` | real stack | `RED-INT-*` |

### Boundary RED와 Logic RED의 분리

- **Boundary RED**: 입력 검증(E001~E005), 출력 형식(`int[6]`, 1-index), Domain 호출 횟수, 에러 매핑(E006/E007)을 검증합니다. Domain Invariant를 직접 구현하지 않습니다.
- **Logic RED**: `MagicSquareValidator`, `EmptyCellLocator`, `MissingNumberFinder`, `TwoCellSolver` 등 Domain 불변식(I1~I11)을 **Mock 없이** 검증합니다.

### ECB 역할 분리

Entity는 Board 상태와 순수 도메인 규칙을 표현하고, Control은 검증과 해 결정 흐름을 조정하며, Boundary는 입력 검증·출력 형식·오류 정책을 담당합니다. Domain은 UI, DB, Web, 파일 시스템에 의존하지 않습니다.

### Concept-to-Code Traceability

```
Concept / Invariant
  → User Story (US-01~05)
  → Scenario (SC-*)
  → RED Test ID
  → Test Skeleton
  → ECB Component
```

### RED → GREEN → REFACTOR 원칙

| Phase | 규칙 |
|-------|------|
| **RED** | 실패 테스트 선작성 → pytest로 **실패 상태 확인** → production 코드 작성 금지 |
| **GREEN** | RED 실패를 통과시키는 **최소 구현 후보**만 수행 |
| **REFACTOR** | GREEN 유지 → 구조 개선 **후보만** 기록 → E001~E007·`int[6]` 계약 불변 |

---

## 5. ECB Role Separation

| ECB Layer | Responsibility | Example Component |
|-----------|----------------|-------------------|
| **Entity** | Board(`Grid`) 상태와 순수 도메인 규칙(I1~I11) 표현. UI·DB·Web·파일 시스템 비의존 | `Grid`, `MagicConstant`, `EmptyCellLocator`, `MissingNumberFinder`, `MagicSquareValidator`, `TwoCellSolver` |
| **Control** | Domain 서비스 오케스트레이션, 검증·해 결정 흐름 조정. Boundary와 Entity 사이 조율 | `SolvePartialMagicSquare` (Use Case) |
| **Boundary** | 입력 검증, 출력 형식(`int[6]`), 오류 정책(E001~E007), Domain 호출 횟수 관리. **Domain Invariant를 직접 구현하지 않음** | `InputValidator`, `UIBoundary`, `ErrorMapper` |

---

## 6. Scenario → AC → RED → GREEN Tracking Board

| Status | Scenario ID | Scenario Summary | Acceptance Criteria | RED Test ID | Test Skeleton Candidate | Expected RED Failure | GREEN Task Candidate | REFACTOR Candidate | ECB Layer | Code Target |
|--------|-------------|------------------|---------------------|-------------|-------------------------|----------------------|----------------------|--------------------|-----------|-------------|
| ⬜ | SC-BND-001 | None(null) 입력 | `null` 입력 시 E003 반환, Domain 0회 호출 | RED-BND-001 (U-IN-01) | `tests/boundary/test_input_validator.py::test_null_matrix_returns_e003` | `ModuleNotFoundError` 또는 assertion 실패 (E003 미구현) | `InputValidator.validate()`에서 `None` → E003 반환 구현 | 에러 코드 enum/상수 SSOT 추출 | Boundary | `InputValidator` |
| ⬜ | SC-BND-002 | 4×4가 아닌 입력 | 행·열 ≠ 4 시 E001 반환, Domain 0회 호출 | RED-BND-002 (U-IN-02) | `tests/boundary/test_input_validator.py::test_non_4x4_matrix_returns_e001` | assertion 실패 (E001 미구현) | 크기 검증 로직 최소 구현 | 검증 순서(null→size→…) 명시적 함수 분리 | Boundary | `InputValidator` |
| ⬜ | SC-BND-003 | 빈칸 개수 오류 | `count(0) ≠ 2` 시 E002 반환, Domain 0회 호출 | RED-BND-003 (U-IN-03) | `tests/boundary/test_input_validator.py::test_empty_cell_count_not_two_returns_e002` | assertion 실패 (E002 미구현) | 빈칸 개수 카운트·E002 반환 최소 구현 | 빈칸 카운트 헬퍼 추출 | Boundary | `InputValidator` |
| ⬜ | SC-BND-004 | 값 범위 오류 | 값 ∉ {0}∪{1..16} 시 E004 반환, Domain 0회 호출 | RED-BND-004 (U-IN-04) | `tests/boundary/test_input_validator.py::test_out_of_range_value_returns_e004` | assertion 실패 (E004 미구현) | 값 범위 검증 최소 구현 | 범위 상수 `VALID_MIN`/`VALID_MAX` SSOT화 | Boundary | `InputValidator` |
| ⬜ | SC-BND-005 | 중복 숫자 오류 | 0 제외 중복 시 E005 반환, Domain 0회 호출 | RED-BND-005 (U-IN-05) | `tests/boundary/test_input_validator.py::test_duplicate_nonzero_returns_e005` | assertion 실패 (E005 미구현) | non-zero distinct 검증 최소 구현 | 중복 검사를 set 기반으로 정리 | Boundary | `InputValidator` |
| ⬜ | SC-DOM-LOC-001 | 빈칸 좌표 row-major 탐색 | G1 격자에서 `first=(2,2)`, `second=(3,3)` (1-index) | RED-DOM-007 (D-LOC-01) | `tests/entity/test_empty_cell_locator.py::test_g1_row_major_locate_returns_2_2_and_3_3` | `ImportError` 또는 assertion 실패 | `EmptyCellLocator.locate()` row-major 스캔 최소 구현 | `CellCoordinate` Value Object 분리 | Entity | `EmptyCellLocator` |
| ⬜ | SC-DOM-MIS-001 | 누락 숫자 오름차순 탐색 | G1에서 `smaller=7`, `larger=10` | RED-DOM-012 (D-MIS-01) | `tests/entity/test_missing_number_finder.py::test_g1_find_returns_7_and_10` | assertion 실패 | `{1..16}\present` 2개 탐색·오름차순 정렬 최소 구현 | `MissingNumberPair` Value Object 분리 | Entity | `MissingNumberFinder` |
| ⬜ | SC-DOM-VAL-002 | 모든 행 합 34 검증 | 행 1개 불일치 완전 격자 → `false` | RED-DOM-002 (D-VAL-02) | `tests/entity/test_magic_square_validator.py::test_row_mismatch_returns_false` | assertion 실패 | 행 합 = M(34) 검사 최소 구현 | 행/열/대각 검사 공통 헬퍼 추출 | Entity | `MagicSquareValidator` |
| ⬜ | SC-DOM-VAL-003 | 모든 열 합 34 검증 | 열 1개 불일치 완전 격자 → `false` | RED-DOM-003 (D-VAL-03) | `tests/entity/test_magic_square_validator.py::test_col_mismatch_returns_false` | assertion 실패 | 열 합 = M(34) 검사 최소 구현 | `sum_col()` 헬퍼 추출 | Entity | `MagicSquareValidator` |
| ⬜ | SC-DOM-VAL-004 | 두 대각선 합 34 검증 | 대각 불일치 완전 격자 → `false` | RED-DOM-004 (D-VAL-04) | `tests/entity/test_magic_square_validator.py::test_diagonal_mismatch_returns_false` | assertion 실패 | 주대각·부대각 합 검사 최소 구현 | 대각선 검사 단일 함수로 통합 | Entity | `MagicSquareValidator` |
| ⬜ | SC-DOM-SOL-001 | small-first 성공 | G1 Step A 성공 → `[2,2,7,3,3,10]` | RED-DOM-015 (D-SOL-01) | `tests/entity/test_two_cell_solver.py::test_g1_step_a_success_returns_ascending` | assertion 실패 | Step A: smaller→first, larger→second 배치·검증 최소 구현 | `SolutionResult` Value Object 분리 | Entity | `TwoCellSolver` |
| ⬜ | SC-DOM-SOL-002 | small-first 실패 후 reverse 성공 | G2 Step A 실패·Step B 성공 → Step B 배치 출력 | RED-DOM-016 (D-SOL-02) | `tests/entity/test_two_cell_solver.py::test_g2_step_b_success_returns_descending` | assertion 실패 | Step B: larger→first, smaller→second 반대 조합 최소 구현 | Step A/B 공통 try-combination 헬퍼 추출 | Entity | `TwoCellSolver` |
| ⬜ | SC-DOM-SOL-003 | 두 조합 모두 실패 | G3 → `UnsolvableDomainError` | RED-DOM-017 (D-SOL-03) | `tests/entity/test_two_cell_solver.py::test_g3_both_fail_raises_unsolvable` | `pytest.raises` 실패 또는 예외 미발생 | Step A·B 모두 실패 시 `UnsolvableDomainError` 최소 구현 | 예외 계층 Domain 전용 패키지 정리 | Entity | `TwoCellSolver` |
| ⬜ | SC-BND-OUT-001 | 결과 배열 길이 6 | 유효 입력 성공 시 반환 배열 길이 = 6 | RED-BND-011 (U-OUT-01) | `tests/boundary/test_ui_boundary.py::test_success_result_length_is_six` | assertion 실패 | `SolutionResult` → `int[6]` 직렬화 최소 구현 | 직렬화/역직렬화 분리 | Boundary | `UIBoundary` |
| ⬜ | SC-BND-OUT-002 | 반환 좌표 1-index | 출력 좌표가 1-index (`1 ≤ r,c ≤ 4`) | RED-BND-012 (U-OUT-02) | `tests/boundary/test_ui_boundary.py::test_success_result_coordinates_are_1_indexed` | assertion 실패 | Domain 1-index → Boundary 출력 매핑 최소 구현 | 좌표 변환 유틸 SSOT화 | Boundary | `UIBoundary` |

> **Canonical Test ID:** Report/02·PRD SSOT는 `D-*`, `U-*` 접두를 사용합니다. 본 표의 `RED-BND-*`, `RED-DOM-*`는 Tracking Board alias이며, Test Skeleton 작성 시 PRD ID와 병기합니다.

---

## 7. RED Start Checklist

- [ ] 모든 Scenario가 정의되었는가?
- [ ] 모든 Acceptance Criteria가 테스트 가능한 문장인가?
- [ ] 모든 Scenario에 RED Test ID가 부여되었는가?
- [ ] 모든 RED Test ID에 Test Skeleton 후보가 있는가?
- [ ] 각 RED 항목에 Expected RED Failure가 명시되었는가?
- [ ] 각 RED 실패에 대응하는 GREEN Task 후보가 있는가?
- [ ] Boundary RED와 Logic RED가 분리되었는가?
- [ ] ECB Layer가 명확히 지정되었는가?
- [ ] 아직 구현 코드를 작성하지 않았는가?
- [ ] 아직 테스트 코드를 작성하지 않았는가?
- [ ] 아직 REFACTOR를 수행하지 않았는가?

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Golden Master 회귀 안전장치

Refactoring 시작 전 구축.
GREEN 완료 후 즉시 적용.

#### 기준 파일 생성

- [x] GM-01: `golden_master_expected.txt` 생성
- [x] GM-02: 정상/역순/오류 시나리오 추가
- [x] GM-03: `git add tests/golden_master_expected.txt`

#### 테스트 코드

- [x] GM-04: `test_golden_master_magic_square` 작성
- [x] GM-05: approve 패턴 적용
- [x] GM-06: Golden Master 테스트 PASS 확인

#### 회귀 보호

- [x] GM-07: row-major 규칙 보호
- [x] GM-08: 1-index 출력 보호
- [x] GM-09: reverse 조합 fallback 보호
- [x] GM-10: Error Contract 보호

> 상세: `docs/golden_master_design.md` · 실행: `pytest tests/test_gm_01_magic_square_golden_master.py -v`

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 8. Quality Gates

| 항목 | 기준 |
|------|------|
| Domain Logic coverage | ≥ 95% |
| Boundary Validation coverage | ≥ 85% |
| 전역 coverage (REFACTOR gate) | ≥ 80% |
| 테스트 프레임워크 | pytest (`python -m pytest`) |
| 테스트 패턴 | AAA (Arrange-Act-Assert) |
| 테스트 약화 | 금지 (assertion 삭제·완화로 GREEN 달성 불가) |
| 디버깅 | `print()` 금지 |
| 매직 넘버 | 설명 없는 magic number 금지 (`MagicConstant` SSOT 사용) |
| 타입 | type hints 필수 |
| 코드 스타일 | PEP8 준수 |
| 계약 불변 | 입력/출력 계약(E001~E007, `int[6]`) 변경 금지 |

### pytest 설정 (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

---

## 9. Reference Documents

| 문서 | 역할 |
|------|------|
| `docs/PRD_MagicSquare.md` | 프로젝트 SSOT — 목적, FR/NFR, I/O 계약, E001~E007, Traceability Matrix |
| `Report/01.MagicSquare_ProblemDefinition_Report.md` | 문제 정의, Why Chain, 불변식(I1~I11) 1차 기준 |
| `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md` | Dual-Track TDD 설계, Domain/Boundary API, Test ID(`D-*`, `U-*`) SSOT |
| `Report/03.MagicSquare_CursorRules_And_FirstEntity_Report.md` | 개발 환경, `.cursorrules`, ECB, pytest 인프라, User Entity 워밍업 |
| `Report/04.MagicSquare_CursorAgents_Setup_Report.md` | Cursor Custom Agent 8종 설정 및 역할 분담 |
| `Report/05.MagicSquare_UserJourney_To_Scenario_Report.md` | Epic → User Journey → User Story → Scenario → Verification (Level 1~5) |
| `Report/06.MagicSquare_PRD_And_Review_Report.md` | PRD 작성·7기준 검토 통합, v0.2 개정 근거 |
| `Report/07.MagicSquare_TDD_ToDo_And_README_Start_Report.md` | TDD To-Do Tracking Board(38 TASK) + README 시작 선언 통합 SSOT |
| `.cursorrules` | Cursor AI 개발 규칙 SSOT — RED 우선, Dual-Track, forbidden 패턴 |
| `.cursor/rules/*.mdc` | (향후) glob별 세분화 규칙 — ECB, pytest-AAA, python-standards 등 |
| `Prompting/` | 대화형 프롬프트 Transcript 모음 (01~07 워크플로 재현용) |

### 문서 간 관계

```
Report/01 (문제 정의)
  → Report/02 (Dual-Track TDD 설계)
  → Report/03 (Cursor Rules + ECB)
  → Report/04 (Cursor Agents)
  → Report/05 (User Journey → Scenario)
  → Report/06 (PRD 작성·검토)
  → docs/PRD_MagicSquare.md (PRD v0.2 SSOT)
  → Report/07 (TDD To-Do + README 시작 선언)
  → README.md (본 문서 — TDD 착수 선언)
```

---

## 10. Current Project Status

| 항목 | 상태 |
|------|------|
| **현재 단계** | PRD 기반 TDD 시작 준비 |
| **구현 코드** | ⬜ 아직 작성 전 (마방진 Domain/Boundary) |
| **테스트 코드** | ⬜ 아직 작성 전 (마방진 RED) |
| **User Entity (ECB 워밍업)** | ✅ Report/03 — pytest 10 passed |
| **PRD** | ✅ `docs/PRD_MagicSquare.md` v0.2 |
| **Tracking Board** | ✅ 15 필수 Scenario 정의 완료 (본 README §6) |
| **다음 단계** | Test Skeleton 작성 → `pytest` 실행 → **RED 실패 확인** |

### 권장 RED 착수 순서

```
Track B (Logic):
  RED-DOM-001 (G0 Validator) → RED-DOM-002~004 (행·열·대각)
  → RED-DOM-007 (Locator) → RED-DOM-012 (Finder)
  → RED-DOM-015 (G1 Step A) → RED-DOM-016 (G2 Step B) → RED-DOM-017 (G3)

Track A (Boundary):
  RED-BND-001~005 (입력 검증) → RED-BND-011~012 (출력)
  → RED-BND-009~010 (Flow) → RED-BND-013~014 (E006/E007)

Integration:
  RED-INT-001 (G1 E2E) → RED-INT-002 (G2 E2E) → RED-INT-003~006 (IT-E*)
```

---

*본 README는 MagicSquare_1004 TDD Practice의 시작 선언 문서입니다. 구현·테스트 코드는 RED 단계에서 Test Skeleton 작성 후 pytest 실패 확인을 통해 순차적으로 진행합니다.*
