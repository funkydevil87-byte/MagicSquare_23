# MagicSquare_23

4×4 마방진(Magic Square) **부분 격자 해결**을 다루는 TDD·Clean Architecture 학습 프로젝트입니다.

빈칸 2개가 있는 `4×4` 격자에 누락된 두 숫자를 채워 **마방 상수 34**를 만족하는 해를, **고정된 입·출력 계약**과 **Dual-Track TDD**로 구현합니다. 알고리즘 난이도보다 **레이어 분리 · 계약 기반 테스트 · 리팩토링** 훈련이 목표입니다.

> **TDD 시작 선언**: 구현 전에 Scenario → Acceptance Criteria → RED Test ID → Test Skeleton → RED Failure → GREEN Task → REFACTOR Candidate 추적 구조를 고정합니다. **RED**는 Test Skeleton 실행 후 **기대한 이유로 실패하는 상태를 확인**하는 단계입니다.

---

## 1. 고정 입·출력 계약 (변경 금지)

| 항목 | 고정 값 |
|------|---------|
| 입력 | `4×4 int[][]`, `0` = 빈칸, 빈칸 **정확히 2개**, 값 `0` 또는 `1~16`, 0 제외 중복 금지 |
| 출력 (성공) | `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index** |
| Attempt 1 | 작은 누락 숫자 → 첫 빈칸, 큰 누락 숫자 → 둘째 빈칸 |
| Attempt 2 | Attempt 1 실패 시 반대 조합 |
| 둘 다 유효 | **Attempt 1 우선** (UC-D6) |
| 마방 상수 | **34** (행 4 + 열 4 + 대각선 2 = **10개 선**) |
| 첫 빈칸 | row-major(행 우선) 스캔 시 처음 발견되는 `0` |
| 실패 신호 | 정의된 Error Code + Message를 포함하는 **예외(throw)** |
| 입력 검증 실패 | Domain resolver **미호출** |
| 해결 불가 | `UNSOLVABLE` + `주어진 배치로는 마방진을 완성할 수 없습니다` |

근거: [`Report/02.MagicSquare_DualTrack_TDD_CleanArchitecture_Design.md`](Report/02.MagicSquare_DualTrack_TDD_CleanArchitecture_Design.md), [`docs/PRD_MagicSquare.md`](docs/PRD_MagicSquare.md) v1.1

---

## 2. 프로젝트 목적

| 관점 | 내용 |
|------|------|
| **Problem** | “마방진을 만든다”가 아니라, **검증 가능한 불변식 조건**을 고정 계약으로 구현한다 |
| **학습 목표** | 불변식 기반 사고, Boundary/Domain 분리, RED→GREEN→REFACTOR, Concept→Test 추적성 |
| **대상 사용자** | TDD 학습자, ECB/Clean Architecture 학습자, 계약 기반 코드 리뷰어 |
| **범위 밖** | UI 화면, DB/Web, N×N 일반화, 힌트·생성기 |

초기 문제 정의(완성 격자 **판정** 중심)는 [`Report/01.MagicSquare_ProblemDefinition_Report.md`](Report/01.MagicSquare_ProblemDefinition_Report.md)에 기록되어 있으며, 현재 PRD는 **부분 격자 해결(2빈칸 채우기)** 로 범위가 확장되었습니다.

---

## 3. TDD 개발 흐름

```
Scenario → Acceptance Criteria → RED Test ID → Test Skeleton
    → RED Failure 확인 → GREEN Task (최소 구현) → REFACTOR Candidate
```

| 단계 | 정의 |
|------|------|
| **RED** | Test Skeleton 실행 → 기대한 이유로 FAIL/ERROR 확인 |
| **GREEN** | RED 실패를 통과시키는 **최소 구현** |
| **REFACTOR** | 동작 불변 하에 구조 개선 |

---

## 4. Dual-Track TDD

| Track | RED Test ID | 검증 대상 | Domain 호출 |
|-------|-------------|-----------|-------------|
| **Track A — Boundary** | `U-T*` / `A-RED-*` | 입력 스키마, Error Code/Message, 출력 형식 | 입력 검증 실패 시 **미호출** |
| **Track B — Domain/Logic** | `D-T*` | 빈칸·누락 숫자, 합 34, Attempt 1/2, UNSOLVABLE | Entity/Control 단위 RED |

Track A 상세 테스트 계획: [`docs/test_plan.md`](docs/test_plan.md)

---

## 5. ECB 레이어 분리

| 레이어 | 패키지 | 책임 |
|--------|--------|------|
| **Entity** | `src/magicsquare/entity/` | 도메인 VO·Service, 불변식, 마방진 판정·해결 |
| **Control** | `src/magicsquare/control/` | 유스케이스 오케스트레이션 (Attempt 1/2, UC-D6) |
| **Boundary** | `src/magicsquare/boundary/` | 입력 검증, Error Contract, 공개 API, Domain 호출 단락 |

의존 방향: `Boundary → Control → Entity` (역방향 금지)

---

## 6. Scenario 추적 보드 (요약)

15개 Scenario가 PRD·설계서·README 추적 구조에 확정되어 있습니다. 전체 AC·Test Skeleton·GREEN/REFACTOR 후보는 [`Report/07.MagicSquare_README_TDD_Start_Report.md`](Report/07.MagicSquare_README_TDD_Start_Report.md) §2.4를 참고하세요.

| Scenario ID | 요약 | RED Test ID | ECB Layer |
|-------------|------|-------------|-----------|
| SC-B01 | None 입력 | U-T09 | Boundary |
| SC-B02 | 4×4가 아닌 입력 | U-T02, U-T03 | Boundary |
| SC-B03 | 빈칸 개수 오류 | U-T04, U-T05 | Boundary |
| SC-B04 | 값 범위 오류 | U-T06, U-T07 | Boundary |
| SC-B05 | 중복 숫자 오류 | U-T08 | Boundary |
| SC-B06 | 결과 배열 길이 6 | U-T01 (부분) | Boundary |
| SC-B07 | 반환 좌표 1-index | U-T11 (부분) | Boundary + Entity |
| SC-D01 | 빈칸 좌표 row-major 탐색 | D-T05 | Entity |
| SC-D02 | 누락 숫자 오름차순 탐색 | D-T06 | Entity |
| SC-D03~D05 | 행·열·대각선 합 34 검증 | D-T01 (부분) | Entity |
| SC-D06 | small-first 성공 | D-T02 | Control |
| SC-D07 | small-first 실패 후 reverse 성공 | D-T03 | Control |
| SC-D08 | 두 조합 모두 실패 | D-T14, U-T10 | Control + Boundary |

---

## 7. RED 시작 체크리스트

### Track A — Boundary (FR-01, `docs/test_plan.md` 기준)

- [x] **A-RED-01**: `grid=None` → `NULL_INPUT`, Domain 0회 호출
- [x] **A-RED-06**: 모든 계약 위반 입력 → Domain 0회 호출 (AC-FR01-01)
- [x] **A-RED-02**: 행 개수 ≠ 4 → `INVALID_ROW_COUNT`
- [x] **A-RED-03**: jagged / 열 개수 ≠ 4 → `INVALID_COL_COUNT`
- [x] **A-RED-04**: 빈칸(0) 개수 ≠ 2 → `INVALID_EMPTY_COUNT`
- [x] **A-RED-05**: 범위/중복 위반 → `OUT_OF_RANGE` / `DUPLICATE_VALUE`
- [x] **test_u_*** — U-FLOW/U-IN/U-OUT **11건 GREEN** (`tests/boundary/test_u_*.py`)

### Track B — Domain/Logic

- [x] **D-T01~D-T06**: 마방진 판정, 빈칸·누락 숫자, Attempt 1/2 (`test_d_*`)
- [x] **D-T14**: 두 조합 모두 실패 → `UNSOLVABLE`
- [x] **D-T22**: both-valid 시 Attempt 1 우선 (`test_d_sol_22_both_valid.py`)

### 환경·품질

- [x] `python -m pytest` 실행 환경 확인 (**78 passed**)
- [x] AAA 패턴, Error Message **완전 일치**(`==`) 검증
- [x] core 커버리지 **≥85%** (`screen/app.py` 제외, `pytest-cov`)

### 결함 목록 연결

- [x] [`defect_list.md`](defect_list.md) 생성 및 발견 결함 기록
- [x] 모든 결함 수정 후 회귀 테스트 통과 확인 (v2.0)

### Track A — GREEN (AC-FR-01-01, `tests/boundary/test_ac_fr_01_01_contract_violation.py`)

> **대상 AC**: AC-FR-01-01 · PRD §8.1 `INVALID_SIZE` (`Grid must be 4x4.`)  
> **RED 선행**: RED-01~05 (`TestScopeLimitation` → `TestNormalFailureReturn` → `TestBoundaryValues` → `TestIsolationVerification` → `TestMessageIdentity`)  
> **완료 기준**: 아래 W0~W4 완료 후 **29 passed** (현재 RED-01 `#24~#28` ScopeLimitation 6건은 구현 없이 통과)

#### GREEN 완료 게이트

- [x] `pytest tests/boundary/test_ac_fr_01_01_contract_violation.py -q` → **29 passed**

#### GREEN-W0 — 스키마·조기 반환 (기반)

- [x] `src/magicsquare/boundary/schemas.py` — `FailureResult`, `INVALID_SIZE_CODE`, `INVALID_SIZE_MESSAGE` 고정
- [x] `src/magicsquare/boundary/input_validator.py` — `tests` import 제거, `schemas` 사용 *(REFACTOR 완료)*
- [x] `MagicSquareBoundary.solve()` — 검증 실패 시 `FailureResult` **조기 반환**, Domain/Control 미진입
- [x] 검증: `pytest tests/boundary/test_ac_fr_01_01_contract_violation.py::TestScopeLimitation -q` → 6 passed

#### GREEN-W1 — `grid is None` → `INVALID_SIZE`

- [x] `InputValidator.validate()` — `grid is None` 분기 추가
- [x] `#01~#05` `TestNormalFailureReturn` 통과
- [x] `#11`, `#15` `TestIsolationVerification` (`none` spy) 통과
- [x] `#16`, `#20`, `#21` `TestMessageIdentity` (`none` 계열) 통과
- [x] 검증: `pytest tests/boundary/test_ac_fr_01_01_contract_violation.py -k "none" -q`

#### GREEN-W2 — `grid == []` → `INVALID_SIZE`

- [x] `InputValidator.validate()` — 빈 리스트(`[]`) 분기 유지·정리
- [x] `#06`, `#09` `TestBoundaryValues` (`empty_list`) 통과
- [x] `#12` `TestIsolationVerification` (`empty_list` spy) 통과
- [x] `#17`, `#22` `TestMessageIdentity` (`empty_list` 계열) 통과
- [x] 검증: `pytest tests/boundary/test_ac_fr_01_01_contract_violation.py -k "empty_list" -q`

#### GREEN-W3 — 4×4가 아닌 크기 → `INVALID_SIZE`

- [x] `InputValidator.validate()` — `len(rows) != 4` 또는 `any(len(row) != 4 for row in rows)` 분기
- [x] `#07`, `#08`, `#10` `TestBoundaryValues` (`empty_cols`, `3x4`) 통과
- [x] `#13`, `#14` `TestIsolationVerification` (`empty_cols`, `3x4` spy) 통과
- [x] `#18`, `#19`, `#23` `TestMessageIdentity` (`empty_cols`, `grid_3x4` 계열) 통과
- [x] 검증: `pytest tests/boundary/test_ac_fr_01_01_contract_violation.py::TestBoundaryValues tests/boundary/test_ac_fr_01_01_contract_violation.py::TestIsolationVerification tests/boundary/test_ac_fr_01_01_contract_violation.py::TestMessageIdentity -q`

#### GREEN-W4 — 4종 그리드 통합 (W1+W2+W3 완료 시)

- [x] `#29` `test_in_scope_failure_codes_only_invalid_size` — `None`, `[]`, `GRID_EMPTY_COLS`, `GRID_3X4` 모두 `INVALID_SIZE`
- [x] `#24~#28` `TestScopeLimitation` — 구현 변경 없이 계속 통과 (AC-FR-01-02~08·FR-02~05 범위 밖)
- [x] 검증: `pytest tests/boundary/test_ac_fr_01_01_contract_violation.py -q` → **29 passed**

#### GREEN 커밋 권장 (4~5건)

| 커밋 | 묶음 | 검증 |
|------|------|------|
| 1 | W0 — 스키마·조기 반환 | `TestScopeLimitation -q` | ✅ 부분 완료 (`schemas`, `MagicSquareBoundary` — 5/6) |
| 2 | W1 — `None` | `-k "none" -q` | ✅ `#01` 완료 (`TestNormalFailureReturn::test_none_grid_returns_failure_result_not_success`) |
| 3 | W2 — `[]` | `-k "empty_list" -q` | ✅ `#06` 완료 (`TestBoundaryValues::test_empty_list_grid_returns_failure_result`) |
| 4 | W3 + W4 — 크기 위반 + 통합 | 전체 파일 `-q` | ✅ **29 passed** (`#07`~`#08`, `#10`, spy `#11`~`#15`, `#29`) |

> W4는 별도 구현이 거의 없으므로 **W3와 같은 커밋**에 포함해도 됩니다.

---

## RED 단계 To-Do 리스트

### Golden Master 회귀 안전장치

Refactoring 시작 전 구축.
GREEN 완료 후 즉시 적용.

#### 기준 파일 생성

- [x] **GM-01**: `tests/golden_master_expected.txt` 생성
- [x] **GM-02**: 정상/역순/오류 시나리오 추가
- [x] **GM-03**: `git add tests/golden_master_expected.txt`

#### 테스트 코드

- [x] **GM-04**: `tests/boundary/test_golden_master_magic_square.py` 작성
- [x] **GM-05**: approve 패턴 적용 (`GOLDEN_MASTER_APPROVE=1`)
- [x] **GM-06**: Golden Master 테스트 PASS 확인 (`pytest -m golden_master -v`)

#### 회귀 보호

- [x] **GM-07**: row-major 규칙 보호 (GM-TC-01/02)
- [x] **GM-08**: 1-index 출력 보호 (GM-TC-01/02)
- [x] **GM-09**: reverse 조합 fallback 보호 (GM-TC-02)
- [x] **GM-10**: Error Contract 보호 (GM-TC-03~05)

> 설계: [`docs/golden_master_design.md`](docs/golden_master_design.md) · 실행 예시: [`docs/golden_master_execution_example.txt`](docs/golden_master_execution_example.txt)

---

## 8. Quality Gates

| 항목 | 기준 |
|------|------|
| 테스트 프레임워크 | pytest + AAA |
| 실행 | `python -m pytest` |
| 실패 신호 | 예외 throw만 허용 (sentinel/`int[6]` 실패 반환 금지) |
| 금지 | `print(...)`, bare except, 매직 넘버, 레이어 경계 위반 |
| 규칙 | `.cursorrules`, `.cursor/rules/*.mdc` |

---

## 9. 저장소 구조

```
MagicSquare_23/
├── README.md                          ← 이 파일 (TDD 시작 선언 · 프로젝트 개요)
├── pyproject.toml                     ← pytest 설정 (pythonpath=src)
├── docs/
│   ├── PRD_MagicSquare.md             ← PRD v1.1
│   ├── test_plan.md                   ← Track A Boundary 테스트 계획
│   ├── golden_master_design.md        ← Golden Master approve 패턴 설계
│   └── golden_master_execution_example.txt
├── defect_list.md                     ← RED 결함·회귀 추적 (QA)
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md
│   ├── 02.MagicSquare_DualTrack_TDD_CleanArchitecture_Design.md
│   ├── 03.CursorRules_and_UserEntity_Implementation_Report.md
│   ├── 04.CursorAgents_Setup_Report.md
│   ├── 05.MagicSquare_PRD_Review_Report.md
│   ├── 07.MagicSquare_README_TDD_Start_Report.md
│   ├── 08.MagicSquare_TrackA_RED_Test_and_Defect_Report.md
│   ├── 09.MagicSquare_DualTrack_RED_Design_Report.md
│   ├── 10.MagicSquare_DualTrack_RED_Skeleton_Test_Report.md
│   ├── 11.MagicSquare_TrackA_GREEN_01_EmptyGrid_Report.md
│   ├── 12.MagicSquare_TrackA_GREEN_Planning_Checklist_Report.md
│   ├── 13.MagicSquare_TrackA_GREEN_AC_FR_01_01_Complete_Report.md
│   ├── 14.MagicSquare_TrackB_GREEN_and_GUI_Report.md
│   ├── 15.MagicSquare_FR01_E2E_Full_GREEN_Report.md
│   └── 16.MagicSquare_Golden_Master_Regression_Report.md
├── Prompting/                         ← 워크숍 프롬프트·트랜스크립트
│   ├── 05.MagicSquare_TrackA_RED_Test_Transcript.md
│   ├── 06.MagicSquare_DualTrack_RED_Design_Transcript.md
│   ├── 07.MagicSquare_DualTrack_RED_Skeleton_Test_Transcript.md
│   ├── 08.MagicSquare_TrackA_GREEN_01_EmptyGrid_Transcript.md
│   ├── 09.MagicSquare_TrackA_GREEN_Planning_Checklist_Transcript.md  (+ 01~04)
│   ├── 10.MagicSquare_TrackA_GREEN_AC_FR_01_01_Complete_Transcript.md
│   ├── 11.MagicSquare_TrackB_GREEN_and_GUI_Transcript.md
│   ├── 12.MagicSquare_FR01_E2E_Full_GREEN_Transcript.md
│   └── 13.MagicSquare_Golden_Master_Regression_Transcript.md
├── src/magicsquare/
│   ├── boundary/                      ← Boundary + screen GUI
│   ├── control/                       ← SolvePartialMagicSquare
│   └── entity/                        ← Domain services
├── tests/
│   ├── conftest.py                    ← G0~G3 fixtures
│   ├── boundary/                      ← Track A GREEN + E2E + Golden Master
│   ├── golden_master_helper.py        ← GM 캡처·approve·contract 검증
│   ├── golden_master_expected.txt     ← GM 기준 파일 (버전 관리)
│   └── entity/                        ← Track B GREEN
└── .cursor/
    ├── rules/                         ← 프로젝트 Cursor Rules
    └── agents/                        ← 역할별 Cursor Agent 정의
```

---

## 10. 현재 진행 상태

| 단계 | 상태 | 근거 |
|------|------|------|
| STEP 1~5 — 문제 정의 | ✅ 완료 | Report/01 |
| Dual-Track · ECB 설계 | ✅ 완료 | Report/02 |
| Cursor Rules · ECB 스켈레톤 | ✅ 완료 | Report/03 |
| User(Entity) TDD 예제 | ✅ 완료 (6 tests passed) | Report/03 |
| Cursor Agent 구성 | ✅ 완료 | Report/04 |
| PRD v1.1 작성·검토 | ✅ 완료 | Report/05, `docs/PRD_MagicSquare.md` |
| README TDD 시작 선언 | ✅ 완료 | Report/07 |
| Track A Test Skeleton + RED | ✅ 완료 | Report/08, Report/10 |
| Track A GREEN (AC-FR-01-01) | ✅ 완료 (**29/29**) | Report/11, Report/12 |
| Track B Domain RED → GREEN | ✅ 완료 | Report/14 |
| FR-01 전체 + test_u_* GREEN | ✅ 완료 | Report/15 |
| Boundary E2E + D-T22 | ✅ 완료 | `test_boundary_e2e.py`, `test_d_sol_22` |
| Magic Square 본 기능 (FR-02~05) | ✅ 완료 | Entity/Control/Boundary E2E |
| Golden Master (GM-01~10) | ✅ 완료 | Report/16 · **91 passed** |
| ECB REFACTOR 계획 | ✅ 완료 (계획만) | Report/17 · README §REFACTOR TODO |

### Track A GREEN 진행 (AC-FR-01-01)

| 슬라이스 | node id | 상태 |
|----------|---------|------|
| GREEN-01 `grid=[]` | `TestBoundaryValues::test_empty_list_grid_returns_failure_result` | ✅ |
| GREEN-03 `GRID_EMPTY_COLS` | `TestBoundaryValues::test_empty_cols_grid_returns_failure_result` | ✅ |
| GREEN-04 `GRID_3X4` | `TestBoundaryValues::test_3x4_grid_returns_failure_result` | ✅ |
| GREEN-W4 통합 | `test_ac_fr_01_01_contract_violation.py` 전체 | ✅ **29 passed** |

### 다음 단계 (REFACTOR 착수 전)

1. README §REFACTOR **High 3그룹** 순서: 그룹 1 → 2 → 3
2. PRD throw vs `FailureResult` SSOT 확정 (RF-DQ-01)
3. GUI 수동 검증 — `python -m magicsquare.boundary.screen.app`

---

## REFACTOR 단계 To-Do 리스트

> **전제**: GREEN **78 passed** · Golden Master GM-01~10 완료 · REFACTOR = **동작 불변** 구조 개선  
> **근거**: `Report/17.MagicSquare_ECB_REFACTOR_Planning_Report.md` · `.cursor/rules/magicsquare-tdd-testing.mdc` §REFACTOR  
> **파일 매핑**: `domain.py` → `control/solve_partial_magic_square.py` · `ui_boundary` → `boundary/magic_square_boundary.py` · `main_window` → `boundary/screen/app.py`  
> **실행 순서**: **그룹 1 → 그룹 2 → 그룹 3** (각 그룹 내 RF-ID 오름차순)

### High — 그룹 1: 선행 · REFACTOR 게이트 (Test) ✅

> 구조 변경 **전** 반드시 선행. 테스트 없이 REFACTOR 금지.

- [x] **RF-01-01**: `tests/boundary/screen/test_app.py` — `_read_grid()` (빈칸→0, 형식·범위 `ValueError`)
- [x] **RF-01-02**: `_display_result()` — `FailureResult` / `list[6]` / unknown 문자열·tone
- [x] **RF-01-03**: `on_solve()` — `MagicSquareBoundary` mock 분기
- [x] **RF-01-04**: `load_grid()` — 0→빈칸 표시
- [x] **RF-01-05**: `pytest tests/boundary/screen/ -q` → GREEN (**13 passed**)

### High — 그룹 2: 계약 · E001~E007 · 검증 SSOT (Contract) ✅

> 외부 API·Error Code·입력 검증 드리프트 방지. 계약 깨짐 리스크 최대.

- [x] **RF-02-01**: E001~E005 — `FailureResult` 반환 → PRD §13 **예외 throw** (`BoundaryValidationError`)
- [x] **RF-02-02**: E006 `UNSOLVABLE` — `UnsolvableError` 매핑 유지
- [x] **RF-02-03**: `test_u_*` · AC-FR-01-01 · Golden Master 회귀 GREEN
- [x] **RF-06-01**: `input_validator` — `bool` 셀 거부 (`type(value) is int`)
- [x] **RF-06-02**: `16` → Entity `CELL_MAX` SSOT
- [x] **RF-06-03**: bool·범위 경계 테스트 GREEN

### High — 그룹 3: 구조 · ECB 레이어 분리 (Architecture)

> Control/Boundary/Screen에 섞인 Entity·직렬화 책임 분리. Attempt·`int[6]` 회귀 주의.

- [ ] **RF-03-01**: `UnsolvableDomainError` catch → `control/magic_square_solver.py`로 이동
- [ ] **RF-03-02**: `magic_square_boundary.py` — Entity import 제거 (`boundary→control`만)
- [ ] **RF-04-01**: `_attempt` → `entity/services/two_cell_solver.py` 추출 (complete+validate 시도)
- [ ] **RF-04-02**: `solve_partial_magic_square.execute` — Attempt 1/2 **순서만**
- [ ] **RF-04-03**: `tests/entity/test_two_cell_solver.py` · D-SOL-01~04/22 GREEN
- [ ] **RF-05-01**: `int[6]` → `boundary/result_formatter.py` SSOT
- [ ] **RF-05-02**: Screen `_display_result` — Formatter 위임
- [ ] **RF-05-03**: `tests/boundary/test_result_formatter.py` GREEN

### Medium / Low — High 3그룹 완료 후 (RF-07~RF-17)

> 상세·전체 17건 목록: [`Report/17`](Report/17.MagicSquare_ECB_REFACTOR_Planning_Report.md) §8

| RF-ID | 요약 |
|-------|------|
| RF-07~08 | Screen `_read_grid` / `_display_result` Boundary 위임 |
| RF-09~10 | `tests/control/` 미러링 · Attempt DRY |
| RF-11~12 | SAMPLE fixture 이동 · `ui_boundary`/`main_window` rename |
| RF-13~17 | pass-through·GRID_SIZE SSOT·`_build_layout`·dead code 정리 |

### REFACTOR 회귀 게이트 (매 단계 후)

```powershell
python -m pytest
python -m pytest -m golden_master -v
python -m pytest tests/boundary/test_ac_fr_01_01_contract_violation.py -q
python -m pytest tests/boundary/test_boundary_e2e.py -q
python -m pytest --cov=src/magicsquare --cov-report=term-missing
```

- Golden Master baseline diff **0** (무변경 PASS)
- TD-01/G1/G2 `int[6]` · E001~E005 code/message · Attempt 1→2 · UC-D6 **불변**

---

## 11. 참고 문서

| 문서 | 역할 |
|------|------|
| [Report/01 — 문제 정의](Report/01.MagicSquare_ProblemDefinition_Report.md) | Observation · Why 체인 · 진짜 문제 정의 |
| [Report/02 — 설계](Report/02.MagicSquare_DualTrack_TDD_CleanArchitecture_Design.md) | Dual-Track TDD · ECB · Domain API · 테스트 ID |
| [Report/03 — 개발 환경](Report/03.CursorRules_and_UserEntity_Implementation_Report.md) | Cursor Rules · ECB 스켈레톤 · User TDD |
| [Report/04 — Cursor Agent](Report/04.CursorAgents_Setup_Report.md) | 역할별 Agent 정의 |
| [Report/05 — PRD 검토](Report/05.MagicSquare_PRD_Review_Report.md) | PRD 품질 검토 · P0~P3 개선 권고 |
| [Report/07 — README TDD 선언](Report/07.MagicSquare_README_TDD_Start_Report.md) | README 작성 세션 · 15 Scenario 추적 보드 |
| [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) | 구현 전 요구사항 · FR · AC · Traceability |
| [docs/test_plan.md](docs/test_plan.md) | Track A Boundary RED 테스트 계획 |
| [docs/golden_master_design.md](docs/golden_master_design.md) | Golden Master approve 패턴 · GM-TC-01~05 |
| [defect_list.md](defect_list.md) | RED 실행 결함 목록 · 회귀 체크리스트 |
| [Report/08 — Track A RED·결함](Report/08.MagicSquare_TrackA_RED_Test_and_Defect_Report.md) | RED 테스트·결함 세션 보고서 |
| [Prompting/05 — Track A RED Transcript](Prompting/05.MagicSquare_TrackA_RED_Test_Transcript.md) | Track A RED·결함 세션 Transcript |
| [Report/09 — Dual-Track RED 설계](Report/09.MagicSquare_DualTrack_RED_Design_Report.md) | FR-01~05 RED 설계표 세션 보고서 |
| [Prompting/06 — Dual-Track RED Transcript](Prompting/06.MagicSquare_DualTrack_RED_Design_Transcript.md) | RED 설계표 세션 Transcript |
| [Report/10 — Dual-Track RED 스켈레톤](Report/10.MagicSquare_DualTrack_RED_Skeleton_Test_Report.md) | Report/09 기반 pytest 스켈레톤 23건 세션 보고서 |
| [Prompting/07 — RED 스켈레톤 Transcript](Prompting/07.MagicSquare_DualTrack_RED_Skeleton_Test_Transcript.md) | RED 스켈레톤 테스트 세션 Transcript |
| [Report/11 — Track A GREEN-01](Report/11.MagicSquare_TrackA_GREEN_01_EmptyGrid_Report.md) | GREEN 1차 슬라이스 (`grid=[]`) |
| [Prompting/08 — GREEN-01 Transcript](Prompting/08.MagicSquare_TrackA_GREEN_01_EmptyGrid_Transcript.md) | GREEN-01 세션 Transcript |
| [Report/12 — Track A GREEN 계획](Report/12.MagicSquare_TrackA_GREEN_Planning_Checklist_Report.md) | GREEN W0~W4 순서·README TODO 체크리스트 |
| [Prompting/09 — GREEN 계획 Transcript](Prompting/09.MagicSquare_TrackA_GREEN_Planning_Checklist_Transcript.md) | GREEN 계획·체크리스트 세션 Transcript |
| [Report/13 — Track A GREEN 완료](Report/13.MagicSquare_TrackA_GREEN_AC_FR_01_01_Complete_Report.md) | AC-FR-01-01 GREEN 29/29 완료 세션 |
| [Prompting/10 — GREEN 완료 Transcript](Prompting/10.MagicSquare_TrackA_GREEN_AC_FR_01_01_Complete_Transcript.md) | AC-FR-01-01 GREEN 완료 세션 Transcript |
| [Report/14 — Track B GREEN·GUI](Report/14.MagicSquare_TrackB_GREEN_and_GUI_Report.md) | Entity/Control GREEN + tkinter GUI |
| [Report/15 — FR-01·E2E Full GREEN](Report/15.MagicSquare_FR01_E2E_Full_GREEN_Report.md) | FR-01·test_u_*·E2E·D-T22·회귀 세션 |
| [Report/16 — Golden Master](Report/16.MagicSquare_Golden_Master_Regression_Report.md) | GM-01~GM-10 회귀 안전장치 구축 |
| [Prompting/13 — Golden Master Transcript](Prompting/13.MagicSquare_Golden_Master_Regression_Transcript.md) | Golden Master 세션 Transcript |
| [Report/17 — ECB REFACTOR 계획](Report/17.MagicSquare_ECB_REFACTOR_Planning_Report.md) | 코드 리뷰·ECB/SRP·REFACTOR 17건 우선순위 |
| [Prompting/14 — REFACTOR 계획 Transcript](Prompting/14.MagicSquare_ECB_REFACTOR_Planning_Transcript.md) | REFACTOR 계획 세션 Transcript |

### Open Questions (미해결)

| ID | 내용 |
|----|------|
| DQ-01 | User Journey 1차 근거 문서 부재 |
| DQ-02 | Data Layer 포함 여부 (Report/02 vs PRD Out-of-Scope) |

---

## 12. 빠른 시작

```powershell
# 설치 (최초 1회)
pip install -e ".[dev]"

# 테스트 실행 (Python 3.10+)
python -m pytest

# 커버리지 (screen GUI 제외)
python -m pytest --cov=src/magicsquare --cov-report=term-missing

# Golden Master 회귀 테스트
python -m pytest -m golden_master -v

# GUI 수동 확인
python -m magicsquare.boundary.screen.app
```

---

## 문서 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-28 | STEP 1~5 문제 정의 보고서 · README 초판 |
| 2026-05-29 | PRD v1.1 · Dual-Track 설계 · 개발 환경 · README TDD 시작 선언 반영 |
| 2026-05-29 | Track A GREEN 계획·README §7 GREEN TODO · Report/12 · Prompting/09 |
| 2026-05-29 | GREEN-01 (`grid=[]`) · GREEN-02 (`grid=None`) 완료 · AC-FR-01-01 **17/29** passed |
| 2026-05-29 | GREEN-W3/W4 완료 · AC-FR-01-01 **29/29** passed · Control `MagicSquareSolver` 스텁 |
| 2026-05-29 | Golden Master GM-01~GM-10 · Report/16 · Prompting/13 · 78 tests passed |
| 2026-05-29 | ECB REFACTOR 계획 · README §REFACTOR TODO RF-01~17 · Report/17 · Prompting/14 |
| 2026-05-29 | README §REFACTOR — High 3그룹( Test → Contract → Architecture ) 요약 정리 |

---

*본 README는 TDD 시작 선언 및 프로젝트 개요입니다. 상세 AC·테스트 데이터·Traceability Matrix는 PRD와 Report 문서를 참고하세요.*
