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

- [ ] **A-RED-01**: `grid=None` → `NULL_INPUT`, Domain 0회 호출
- [ ] **A-RED-06**: 모든 계약 위반 입력 → Domain 0회 호출 (AC-FR01-01)
- [ ] **A-RED-02**: 행 개수 ≠ 4 → `INVALID_ROW_COUNT`
- [ ] **A-RED-03**: jagged / 열 개수 ≠ 4 → `INVALID_COL_COUNT`
- [ ] **A-RED-04**: 빈칸(0) 개수 ≠ 2 → `INVALID_EMPTY_COUNT`
- [ ] **A-RED-05**: 범위/중복 위반 → `OUT_OF_RANGE` / `DUPLICATE_VALUE`

### Track B — Domain/Logic (설계서 기준, 후속)

- [ ] **D-T01~D-T06**: 마방진 판정, 빈칸·누락 숫자, Attempt 1/2
- [ ] **D-T14**: 두 조합 모두 실패 → `UNSOLVABLE`

### 환경·품질

- [ ] `python -m pytest` 실행 환경 확인
- [ ] AAA 패턴, Error Message **완전 일치**(`==`) 검증
- [ ] Domain Logic 커버리지 95%+, Boundary 85%+, 전체 90%+ (목표)

### 결함 목록 연결

- [x] [`defect_list.md`](defect_list.md) 생성 및 발견 결함 기록 (2026-05-29, RED 24 ERROR)
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

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
│   └── test_plan.md                   ← Track A Boundary 테스트 계획
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
│   └── 13.MagicSquare_TrackA_GREEN_AC_FR_01_01_Complete_Report.md
├── Prompting/                         ← 워크숍 프롬프트·트랜스크립트
│   ├── 05.MagicSquare_TrackA_RED_Test_Transcript.md
│   ├── 06.MagicSquare_DualTrack_RED_Design_Transcript.md
│   ├── 07.MagicSquare_DualTrack_RED_Skeleton_Test_Transcript.md
│   ├── 08.MagicSquare_TrackA_GREEN_01_EmptyGrid_Transcript.md
│   ├── 09.MagicSquare_TrackA_GREEN_Planning_Checklist_Transcript.md  (+ 01~04)
│   └── 10.MagicSquare_TrackA_GREEN_AC_FR_01_01_Complete_Transcript.md
├── src/magicsquare/
│   ├── boundary/                      ← Boundary 레이어 (AC-FR-01-01 GREEN 진행 중)
│   ├── control/                       ← Control 레이어 (구현 예정)
│   └── entity/                        ← Entity 레이어 (User TDD 완료)
├── tests/
│   ├── conftest.py                    ← G0~G3 fixture placeholder
│   ├── boundary/                      ← Track A RED (Report/08 + test_u_*)
│   └── entity/                        ← User GREEN + test_d_* RED skeleton
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
| Track B Domain RED → GREEN | ⏳ 예정 | Report/02 §1.5 |
| Magic Square 본 기능 구현 | ⏳ 예정 | PRD FR-01~05 |

### Track A GREEN 진행 (AC-FR-01-01)

| 슬라이스 | node id | 상태 |
|----------|---------|------|
| GREEN-01 `grid=[]` | `TestBoundaryValues::test_empty_list_grid_returns_failure_result` | ✅ |
| GREEN-03 `GRID_EMPTY_COLS` | `TestBoundaryValues::test_empty_cols_grid_returns_failure_result` | ✅ |
| GREEN-04 `GRID_3X4` | `TestBoundaryValues::test_3x4_grid_returns_failure_result` | ✅ |
| GREEN-W4 통합 | `test_ac_fr_01_01_contract_violation.py` 전체 | ✅ **29 passed** |

### 다음 단계

1. **REFACTOR** — `input_validator` `tests` import 제거, `schemas.FailureResult` 통합
2. **AC-FR-01-02~** — 다음 Boundary AC RED/GREEN 착수
3. Track B Domain 테스트(D-T*) 착수

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

### Open Questions (미해결)

| ID | 내용 |
|----|------|
| DQ-01 | User Journey 1차 근거 문서 부재 |
| DQ-02 | Data Layer 포함 여부 (Report/02 vs PRD Out-of-Scope) |

---

## 12. 빠른 시작

```powershell
# 테스트 실행 (Python 3.10+)
python -m pytest

# 커버리지 (pytest-cov 설치 후)
python -m pytest --cov=src/magicsquare --cov-report=term-missing
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
| 2026-05-29 | Report/13 · Prompting/10 — AC-FR-01-01 GREEN 완료 세션 Export |

---

*본 README는 TDD 시작 선언 및 프로젝트 개요입니다. 상세 AC·테스트 데이터·Traceability Matrix는 PRD와 Report 문서를 참고하세요.*
