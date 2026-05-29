# PRD — Magic Square 4x4 TDD Practice

| 항목 | 내용 |
|------|------|
| 버전 | **1.1** (검토 반영) |
| 기준일 | 2026-05-29 |
| 검토 근거 | `Report/05.MagicSquare_PRD_Review_Report.md` P0~P3 |
| 변경 요약 | UC-D6 both-valid 우선순위, DQ-03 확정, NULL_INPUT·예외 계층, Layer 분리, AC/Matrix/NFR-AC·fixture 보강 |

## 1. Executive Summary
본 프로젝트는 4×4 정수 행렬에서 정확히 2개의 빈칸(0)에 누락된 두 숫자를 채워 **마방진(상수 34)**을 만족시키는 해를 **고정된 입력/출력 계약**에 따라 산출하는 과제를 통해, **불변식 기반 사고**, **Boundary/Domain 분리(Dual-Track TDD)**, **RED→GREEN→REFACTOR** 흐름, 그리고 **Concept→Rule→Use Case→Contract→Test→Component** 추적성을 훈련하는 것을 목표로 한다. 이 PRD는 구현 전에 검증 가능한 요구사항과 실패 정책을 확정하여, 리팩토링 이후에도 계약이 깨지지 않도록 “사전 기준(Contracts & Invariants)”을 제공한다.

## 2. Background
학습자는 종종 구현을 먼저 시작하여 테스트 기준이 불명확해지고, Boundary와 Domain 책임이 섞이며, 리팩토링 후 계약이 붕괴한다. 마방진 문제는 결과가 참/거짓으로 명확한 **불변식들의 조합**으로 정의되므로, “알고리즘 창작”이 아니라 “검증 가능한 규칙(불변식) 고정”에 적합한 TDD 훈련 과제다. (근거: `Report/01.MagicSquare_ProblemDefinition_Report.md`의 Why #3 및 “진짜 문제 정의”)

## 3. Problem Statement
문제는 “마방진을 만든다”가 아니라, 다음을 만족하는 **검증 가능한 불변식 조건을 완성**하는 것이다.

- 입력으로 주어진 `4x4 int[][]`에서 `0`으로 표시된 **정확히 2개의 빈칸**을 찾는다.
- `1..16` 중 입력에 존재하지 않는 **정확히 2개의 누락 숫자**를 찾는다.
- 두 누락 숫자를 두 빈칸에 배치하는 2가지 조합(Attempt 1/2)을 고정된 순서로 시도하여, 완성된 4×4가 **마방진 상수 34** 및 **10개 선(행4+열4+대각2) 합 동일**을 만족하는지 판정한다.
- 성공 시 고정 출력 계약 `int[6] = [r1,c1,n1,r2,c2,n2]`을 반환한다.
- 실패 정책(검증 실패/해결 불가)을 단 하나의 방식으로 확정한다.

입력/출력 계약은 TDD의 전제이며, 계약이 모호하면 테스트가 흔들려 리팩토링 회귀 보호가 불가능하다. (근거: `Report/02...Design`의 “고정 입·출력 계약(변경 금지)”)

## 4. Why Now / Why Chain
본 프로젝트를 지금 수행해야 하는 이유는 학습자의 반복되는 실패 패턴을 “계약과 불변식”으로 닫기 위함이다.

- 구현 먼저 시작 → **RED 기준 부재**로 요구사항이 코드에 끌려감
- 테스트 기준 불명확 → 성공/실패 판정이 흔들려 회귀가 발생
- Boundary와 Domain 책임 혼합 → 입력 검증이 로직에 섞이고, 실패 정책이 일관되지 않음
- 리팩토링 후 계약 붕괴 → 출력 포맷/좌표 인덱스/시도 순서가 변경되거나 누락됨

따라서 “고정 계약 + 불변식 + Dual-Track TDD”를 구현 전에 문서로 확정한다. (근거: `Report/01...ProblemDefinition` Why 체인)

## 5. Target Users
- **TDD 학습자**: 계약 기반 RED→GREEN→REFACTOR를 반복 학습
- **코드 리뷰어**: 요구사항-테스트-컴포넌트 추적성을 기준으로 리뷰
- **Clean Architecture/ECB 학습자**: boundary/control/entity(또는 domain) 책임 분리 훈련

사용 환경:
- 콘솔 실행 또는 테스트 실행 중심
- UI 화면/DB/Web은 범위 밖(Out-of-Scope)

## 6. Vision & Epic Goal
- **Epic Goal**: “불변식 기반 사고 훈련 시스템 구축”
- **Vision**: 사용자가 고정된 계약과 불변식으로 문제를 정의하고, Dual-Track TDD로 Boundary 계약과 Domain 불변식을 병렬로 고정하여, 리팩토링 후에도 동일 계약을 유지하는 훈련을 수행한다.

## 7. Persona
- **TDD 학습 중 개발자**: 테스트로 규칙을 먼저 고정하는 습관을 만들고자 함
- **계층 분리 학습자**: ECB 의존 방향과 책임 경계를 코드로 체화하려 함
- **훈련 중심 사용자**: 알고리즘 “정답”보다 “계약/테스트/리팩토링” 흐름을 성공 기준으로 삼음

## 8. User Journey Summary
- **문제 인식**: “마방진을 만든다”가 아니라 “불변식 판정과 계약 고정” 문제임을 인식
  - Pain Point: 요구사항이 모호하여 테스트가 못 써짐
  - Learning Outcome: 불변식 목록을 요구사항으로 분해
- **계약 정의**: 입력/출력/실패 정책을 문장 단위로 고정
  - Pain Point: 1-index/0-index, 출력 포맷이 흔들림
  - Learning Outcome: 계약 스냅샷을 회귀 기준으로 사용
- **도메인 분리**: Domain 로직이 Boundary 검증과 분리됨
  - Pain Point: 검증 실패에도 Domain이 호출됨
  - Learning Outcome: “검증 실패 → Domain 미호출”을 테스트로 고정
- **Dual-Track TDD 진행**: Track A(Contract)와 Track B(Invariant)를 병렬로 RED
  - Pain Point: Domain 먼저 다 만들고 Boundary 붙이는 방식으로 흐름이 깨짐
  - Learning Outcome: 병렬 RED/GREEN으로 경계를 강제
- **회귀 보호**: 리팩토링 후에도 동일 계약/불변식 유지
  - Pain Point: 리팩토링이 동작 변경을 포함
  - Learning Outcome: 테스트 약화 금지, 계약 유지

> 참고: 본 PRD의 User Journey/Acceptance/Gherkin은 원칙적으로 `Report/4.UserJourney...`를 1차 근거로 삼아야 하나, 현재 리포지토리에 해당 파일이 존재하지 않아 “Decision Needed”에 반영한다.

## 9. Scope

### 9.1 In-Scope
- 빈칸 좌표 탐색(첫 빈칸/둘째 빈칸 규칙 포함)
- 누락 숫자 탐색(정확히 2개, 오름차순(min,max) 정의 포함)
- 마방진 판정(상수 34, 10개 선 합 동일)
- 두 조합 시도(Attempt 1/Attempt 2) 후 결과 반환
- Boundary 계층 입력 검증(계약 위반 시 Domain 미호출)
- 출력 계약 검증(성공 반환값의 형태/범위)
- RED→GREEN→REFACTOR 흐름에 맞춘 테스트 가능성(요구사항 문장 자체가 테스트 가능)

### 9.2 Out-of-Scope
- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전한 마방진 생성 알고리즘(탐색/생성기)
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동

> 범위 충돌 표기: `Report/02...Design`에는 Data Layer(저장/로드) 설계가 포함되어 있으나, 본 PRD의 Out-of-Scope에 “DB 저장/검색” 및 “UI/DB/Web 의존성 없이”가 명시되어 있으므로 Data Layer는 본 PRD 범위에서 제외한다. (Decision Needed로 재확인 항목 등록)

## 10. Functional Requirements

### FR-01 Input Verification, Boundary
- **Description**: Boundary는 입력 행렬이 고정 입력 계약을 만족하는지 검증하고, 위반 시 정의된 실패 정책으로 종료한다.
- **Layer**: Boundary (Track A)
- **Input**: `int[][] matrix`
- **Processing Rules**:
  - `matrix`가 null이면 실패 처리한다.
  - 행 개수는 정확히 4여야 한다.
  - 각 행의 열 개수는 정확히 4여야 한다(비정형/jagged 금지).
  - 모든 값은 `0` 또는 `1..16`이어야 한다.
  - 값 `0`의 개수는 정확히 2개여야 한다.
  - `0`을 제외한 값은 중복될 수 없다.
- **Output**:
  - 성공(계약 만족): Domain/Control에 입력 전달
  - 실패(계약 위반): Error/Failure Policy에 정의된 방식으로 실패를 신호한다.
- **Acceptance Criteria**:
  - AC-FR01-01: 계약 위반 입력에 대해 Domain resolver는 호출되지 않는다.
  - AC-FR01-02: 각 계약 위반 유형은 고유 Error Code로 분류된다.
  - AC-FR01-03: `matrix`가 null이면 `NULL_INPUT` 예외가 발생하고 Message는 `입력이 null입니다`와 **완전 일치**한다.
  - AC-FR01-04: 행 개수≠4이면 `INVALID_ROW_COUNT` + Message `행 개수는 4여야 합니다`.
  - AC-FR01-05: jagged 또는 열 개수≠4이면 `INVALID_COL_COUNT` + Message `열 개수는 4여야 합니다`.
  - AC-FR01-06: 0 개수≠2이면 `INVALID_EMPTY_COUNT` + Message `빈칸(0)은 정확히 2개여야 합니다`.
  - AC-FR01-07: 범위 위반이면 `OUT_OF_RANGE` + Message `값은 0 또는 1부터 16까지여야 합니다`.
  - AC-FR01-08: 0 제외 중복이면 `DUPLICATE_VALUE` + Message `0을 제외한 값은 중복될 수 없습니다`.
- **Error / Exception Policy**: 섹션 13을 따른다.
- **Related Business Rules**: BR-01, BR-02, BR-03, BR-04, BR-05
- **Related Test Direction**: Track A의 “Domain 미호출” 검증을 포함한다.
- **Component Candidate**: `BoundaryValidator`

### FR-02 Blank Coordinate Discovery
- **Description**: 입력 행렬에서 0의 좌표 2개를 row-major 순서로 탐색하여 (첫 빈칸, 둘째 빈칸)을 결정한다.
- **Layer**: Domain (Track B)
- **Input**: `4x4 int[][]` (FR-01을 통과한 입력)
- **Processing Rules**:
  - row-major(행 1→4, 열 1→4) 스캔 시 처음 발견되는 0이 첫 빈칸이다.
  - 다음에 발견되는 0이 둘째 빈칸이다.
  - 좌표는 1-index 기준으로 표현한다.
- **Output**: `(r1,c1)` 및 `(r2,c2)` (둘 다 1..4)
- **Acceptance Criteria**:
  - AC-FR02-01: 입력이 동일하면 빈칸 좌표 결과는 항상 동일하다.
  - AC-FR02-02: 반환 좌표는 1-index 기준이다.
- **Error / Exception Policy**:
  - **공개 API 경로**: 빈칸 개수·크기·범위·중복 위반은 Boundary(FR-01)에서만 차단하며, Domain resolver는 호출되지 않는다.
  - **Domain 방어 검증(Report/02 D-T10~13)**: Boundary를 우회한 내부 호출·단위 테스트에서 Domain이 방어적으로 실패할 수 있다. 이 경우 Domain은 Boundary Error Code를 던지지 않으며, Domain 전용 예외 또는 `valid=false`로 처리한다(섹션 13.2).
- **Related Business Rules**: BR-06, BR-07
- **Related Test Direction**: 첫/둘째 빈칸 규칙(스캔 순서)을 독립 테스트한다.
- **Component Candidate**: `BlankFinder`

### FR-03 Missing Number Discovery
- **Description**: `1..16` 중 입력에 존재하지 않는 숫자 2개를 찾아 `(min,max)`로 산출한다.
- **Layer**: Domain (Track B)
- **Input**: `4x4 int[][]` (FR-01 통과)
- **Processing Rules**:
  - `0`은 빈칸으로만 취급하며 누락 숫자 계산에서 제외한다.
  - `1..16` 집합에서 입력에 존재하는 비영(≠0) 값을 제외한 결과가 누락 숫자 집합이다.
  - 누락 숫자는 정확히 2개여야 한다.
  - 반환은 오름차순 `(min,max)`로 정의한다.
- **Output**: `(min,max)` (각각 1..16, `min<max`)
- **Acceptance Criteria**:
  - AC-FR03-01: 누락 숫자 2개는 입력에 존재하지 않는다.
  - AC-FR03-02: 반환 순서는 항상 `min<max`다.
- **Error / Exception Policy**: 입력 범위/중복 위반은 FR-01에서 차단한다.
- **Related Business Rules**: BR-08, BR-09
- **Related Test Direction**: 누락 숫자 도출이 0의 위치와 무관함을 검증한다.
- **Component Candidate**: `MissingNumberFinder`

### FR-04 Magic Square Validation
- **Description**: 완성된 4×4에서 마방진 상수 34 및 10개 선 합 동일 불변식을 판정한다.
- **Layer**: Domain (Track B)
- **Input**: 0이 없는 완성 4×4 (시도 조합으로 생성된 후보)
- **Processing Rules**:
  - 검증 대상 선은 행 4개, 열 4개, 대각선 2개 총 10개다.
  - 모든 선의 합은 동일해야 하며, 그 값은 34여야 한다.
- **Output**: `valid=true/false` (또는 이에 상응하는 판정 결과)
- **Acceptance Criteria**:
  - AC-FR04-01: 10개 선 합이 모두 34인 경우에만 valid=true다.
  - AC-FR04-02: 10개 선 중 하나라도 34가 아니면 valid=false다.
  - AC-FR04-03: 입력 격자에 `0`이 0개이고, `1..16` 각 값이 정확히 1회씩일 때만 valid 판정을 수행한다(완성 격자 전제).
- **Error / Exception Policy**: 완성 격자 조건(0 없음)은 조합 시도 단계에서 보장되어야 한다.
- **Related Business Rules**: BR-09, BR-10, BR-11
- **Related Test Direction**: 한 선만 깨지는 최소 반례를 포함한다.
- **Component Candidate**: `MagicSquareValidator`

### FR-05 Two-Combination Solver and Result Formatting

FR-05는 **Control 오케스트레이션**을 중심으로 하며, Attempt 실행·판정은 Domain, 포맷·Boundary 예외 매핑은 Boundary가 담당한다.

#### FR-05-A Solver (Control + Domain)
- **Description**: 두 누락 숫자를 두 빈칸에 배치하는 2가지 조합을 고정 순서로 시도하고, 유효한 조합을 선택한다.
- **Layer**: Control(오케스트레이션), Domain(Attempt 판정·`MagicSquareValidator` 호출)
- **Input**: `4x4 int[][]` (FR-01 통과, FR-02/03 산출물 사용)
- **Processing Rules**:
  - Attempt 1 (조합 A / small-first): `small→첫 빈칸`, `large→둘째 빈칸` — 유효하면 즉시 선택(Attempt 2 미시도).
  - Attempt 2 (조합 B / reverse): Attempt 1 실패 시 `large→첫 빈칸`, `small→둘째 빈칸`.
  - **Both-valid (Report/02 UC-D6)**: Attempt 1·2 **모두** 마방진이면 **Attempt 1(조합 A) 결과를 반환**한다.
  - 둘 다 실패: Domain은 `UnsolvablePartialGridException`(또는 동등 신호)을 발생시키고, Control이 Boundary로 전달한다.
- **Output**: `SolutionVector` (내부) — `(r1,c1,n1,r2,c2,n2)` 의미 보유
- **Acceptance Criteria**:
  - AC-FR05-01: Attempt 1이 유효하면 Attempt 2는 시도하지 않는다.
  - AC-FR05-02: Attempt 1이 실패하고 Attempt 2가 유효하면 Attempt 2 결과를 반환한다.
  - AC-FR05-05: Attempt 1·2가 **모두** 유효할 때 출력은 Attempt 1(small-first) 순서 `[r1,c1,small,r2,c2,large]`이다. (UC-D6 / D-T22)
  - AC-FR05-06: 출력 `(r1,c1,r2,c2)`는 FR-02 `BlankFinder` 탐색 결과와 동일하다(1-index, 0-index 사용 금지).
- **Component Candidate**: `Solver` (Control), `PartialMagicSquareSolver` (Domain)

#### FR-05-B Result Formatting (Boundary)
- **Description**: `SolutionVector`를 외부 계약 `int[6]`으로 변환한다.
- **Layer**: Boundary
- **Input**: `SolutionVector`
- **Output**: `int[6] = [r1,c1,n1,r2,c2,n2]`
- **Acceptance Criteria**:
  - AC-FR05-03: 성공 출력의 좌표는 1-index이며 `r,c ∈ {1,2,3,4}`이다(0-index 금지).
  - AC-FR05-04: 성공 출력의 `n1,n2`는 1..16이며 서로 다르다.
  - AC-FR05-07: 반환 배열 길이는 항상 6이다.
- **Error / Exception Policy**: UNSOLVABLE 등 Domain 실패는 Control 경유 후 Boundary가 섹션 13 Error Code 예외로 매핑한다.
- **Component Candidate**: `ResultFormatter`

- **Related Business Rules**: BR-11, BR-12, BR-13, BR-16
- **Related Test Direction**: NS-01, NS-02, NS-03, ES-05, TD-01, TD-02, TD-07

## 11. Business Rules / Domain Rules
각 규칙은 항상 참이어야 하는 불변식 또는 불변식에 기반한 규칙이다.

- **BR-01 (Grid Size)**: 입력 행렬은 정확히 4×4여야 한다.
- **BR-02 (Zero as Blank)**: 값 `0`은 빈칸을 의미하며, 빈칸 외 의미로 사용되지 않는다.
- **BR-03 (Blank Count)**: 입력 행렬에서 `0`의 개수는 정확히 2개여야 한다.
- **BR-04 (Value Range)**: 모든 값은 `0` 또는 `1..16`이어야 한다.
- **BR-05 (No Duplicate Non-Zero)**: `0`을 제외한 값은 중복될 수 없다.
- **BR-06 (First Blank Definition)**: row-major 스캔(행 우선)으로 처음 발견되는 `0`의 좌표가 첫 번째 빈칸이다.
- **BR-07 (Second Blank Definition)**: 첫 번째 빈칸 이후 다음으로 발견되는 `0`의 좌표가 두 번째 빈칸이다.
- **BR-08 (Missing Numbers Exactly Two)**: `1..16` 중 입력에 존재하지 않는 숫자는 정확히 2개여야 한다.
- **BR-09 (Missing Numbers Ordered)**: 누락 숫자 쌍은 `(small, large)`로 정의되며 `small < large`다.
- **BR-10 (Magic Constant)**: 4×4 마방진 상수는 34다.
- **BR-11 (Line Sum Rule)**: 완성 격자에서 4개 행, 4개 열, 2개 대각선의 합은 모두 동일해야 한다.
- **BR-12 (Attempt 1: small-first)**: Attempt 1은 `small→첫 빈칸`, `large→둘째 빈칸`이다.
- **BR-13 (Attempt 2: reverse)**: Attempt 1 실패 시 Attempt 2는 `large→첫 빈칸`, `small→둘째 빈칸`이다.
- **BR-14 (Output Coordinate Indexing)**: 출력 좌표 `(r,c)`는 1-index 기준이다.
- **BR-15 (Output Shape)**: 성공 출력은 길이 6의 `int[6]`이며 `[r1,c1,n1,r2,c2,n2]` 순서다.
- **BR-16 (Both-Valid Priority)**: Attempt 1·2가 모두 마방진이면 **Attempt 1(조합 A / small-first)을 우선** 반환한다. (`Report/02` UC-D6)

## 12. Input / Output Contract

### 12.1 Input Contract (Boundary)
| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code / Failure Policy |
|---|---|---|---|---|---|
| matrix | `int[][]` | null 금지 | 4x4 배열 | null | `NULL_INPUT` |
| row count | int | 4여야 함 | 4 | 3 | `INVALID_ROW_COUNT` |
| col count | int | 모든 행 4여야 함 | 각 행 길이 4 | jagged(행 길이 4/3 혼재) | `INVALID_COL_COUNT` |
| value range | int | 각 값 ∈ {0}∪[1..16] | 0,1,16 | -1,17 | `OUT_OF_RANGE` |
| zero count | int | 0의 개수=2 | 2 | 1,3 | `INVALID_EMPTY_COUNT` |
| non-zero uniqueness | set | 0 제외 중복 금지 | 1..16 중 일부가 1회씩 | 5가 2회 | `DUPLICATE_VALUE` |

### 12.2 Output Contract (Success)
| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code / Failure Policy |
|---|---|---|---|---|---|
| output | `int[6]` | 길이 6 | `[1,1,7, 4,4,10]` | 길이 5/7 | (성공 계약 위반은 “버그”) |
| r1,c1,r2,c2 | int | 1..4, 1-index | 1,4 | 0,5 | (성공 계약 위반은 “버그”) |
| n1,n2 | int | 1..16, `n1≠n2` | 1,16 | 0,17, 동일값 | (성공 계약 위반은 “버그”) |
| position mapping | semantic | r1,c1은 첫 빈칸 좌표, r2,c2는 둘째 빈칸 좌표 | row-major 기반 | 스캔 규칙 불일치 | (성공 계약 위반은 “버그”) |
| attempt ordering | semantic | Attempt 1 성공 시 small-first, Attempt 2 성공 시 reverse, both-valid 시 Attempt 1 우선 | 규칙 준수 | 임의 순서 | (성공 계약 위반은 “버그”) |

**성공 계약 위반 처리(확정)**: 내부 invariant 위반(길이≠6, 0-index 좌표 등)은 **호출자에게 전달하지 않는** 구현 버그로 분류한다. 테스트에서는 `assert`/내부 예외로만 검출하며, Boundary 공개 API는 정상 경로에서 성공 계약을 항상 만족해야 한다.

## 13. Error / Failure Policy
실패 신호 방식은 단 하나로 고정한다.

- **Failure Signaling (고정 정책)**:
  - Boundary API는 성공 시에만 `int[6]`을 반환한다.
  - 실패 시에는 **정의된 Error Code와 Message를 포함하는 예외(throw)**로 실패를 신호한다.
  - 입력 검증 실패 시 Domain resolver는 호출되지 않는다.

### 13.1 Failure Cases
| Failure Case | Error Code | Message (exact) | Layer | Domain resolver 호출 여부 | Related Acceptance Criteria |
|---|---|---|---|---:|---|
| null 입력 | `NULL_INPUT` | `입력이 null입니다` | Boundary | No | AC-FR01-01, AC-FR01-03 |
| 4x4가 아닌 입력 (row) | `INVALID_ROW_COUNT` | `행 개수는 4여야 합니다` | Boundary | No | AC-FR01-01, AC-FR01-04 |
| 4x4가 아닌 입력 (col/jagged) | `INVALID_COL_COUNT` | `열 개수는 4여야 합니다` | Boundary | No | AC-FR01-01, AC-FR01-05 |
| 빈칸 개수≠2 | `INVALID_EMPTY_COUNT` | `빈칸(0)은 정확히 2개여야 합니다` | Boundary | No | AC-FR01-01, AC-FR01-06 |
| 값 범위 위반 | `OUT_OF_RANGE` | `값은 0 또는 1부터 16까지여야 합니다` | Boundary | No | AC-FR01-01, AC-FR01-07 |
| 0 제외 중복 | `DUPLICATE_VALUE` | `0을 제외한 값은 중복될 수 없습니다` | Boundary | No | AC-FR01-01, AC-FR01-08 |
| 두 조합 모두 실패 | `UNSOLVABLE` | `주어진 배치로는 마방진을 완성할 수 없습니다` | Control→Boundary 매핑 | Yes (solve 1회) | AC-FR05-02, ES-05 |

> 메시지 문구는 `Report/02...Design` 섹션 2.4 표준 문구와 **완전 일치**해야 한다.

### 13.2 Exception Hierarchy (확정)

| 계층 | 역할 | 예시 | Boundary Error Code 노출 |
|---|---|---|---|
| Domain | 순수 로직 실패·방어 검증 | `UnsolvablePartialGridException`, `InvalidEmptyCountException`(내부) | **No** — Domain은 Boundary enum을 모른다 |
| Control | Domain 호출 순서·Attempt 1/2·both-valid 우선순위 | solve 파이프라인 | No |
| Boundary | 공개 API 계약·Error Code+Message 예외 | `NullInputException` 등 → `NULL_INPUT` | **Yes** |

- **공개 API**: 성공 시 `int[6]`, 실패 시 **Error Code + Message 포함 예외 throw** (DQ-03 **확정**, sentinel/`int[6]` 실패 반환 금지).
- **UNSOLVABLE 흐름**: Domain `UnsolvablePartialGridException` → Control catch → Boundary가 `UNSOLVABLE` + 고정 Message로 throw.

## 14. Non-Functional Requirements
- **Test Coverage**:
  - Domain Logic test coverage는 **95% 이상**이어야 한다.
  - Boundary Validation coverage는 **85% 이상**이어야 한다.
- **Deterministic execution**:
  - 동일 입력에 대해 반환되는 성공 출력(또는 실패 코드)은 **항상 동일**해야 한다.
- **No side effects**:
  - 입력 행렬은 호출 전후가 동일해야 하며, 시스템은 **입력 행렬을 변경하지 않는다**.
- **Performance**:
  - 4×4 기준 단일 실행(입력 검증+해결 시도)은 **50ms 이내**에 완료되어야 한다.
- **Maintainability**:
  - Boundary와 Domain 책임 분리를 준수해야 한다(의존 방향: Boundary→Control→Domain).
  - 의미 없는 하드코딩/매직 넘버를 금지하고, 의미 있는 이름의 상수로 표현해야 한다.
  - 설명 없는 상수(예: 34, 4, 16)를 코드에 직접 산재시키지 않는다(상수화 및 테스트 근거 필요).

### 14.1 Non-Functional Acceptance Criteria

| ID | 요구 | 검증 가능 문장 |
|---|---|---|
| AC-NFR-01 | Domain coverage ≥ 95% | `pytest --cov` Domain 패키지 커버리지가 95% 이상이다 |
| AC-NFR-02 | Boundary coverage ≥ 85% | Boundary 패키지 커버리지가 85% 이상이다 |
| AC-NFR-03 | 결정성 | 동일 `int[][]` 입력에 대해 10회 연속 호출 시 성공 출력 또는 Error Code가 모두 동일하다 |
| AC-NFR-04 | 입력 불변 | 호출 전후 입력 행렬 원소가 변경되지 않는다(스냅샷 비교) |
| AC-NFR-05 | 성능 | 4×4 단일 solve(검증+시도)가 50ms 이내 완료된다(로컬 기준, 측정 테스트 1회) |

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
Track A는 “입력/출력 계약과 실패 정책”을 테스트로 고정한다.
- 입력 검증 테스트: 크기/빈칸/범위/중복
- 출력 형식 테스트: 성공 결과의 길이 6 및 1-index 의미
- 실패 응답 테스트: Error Code/Message 일치
- Domain resolver 미호출 테스트: 계약 위반 입력에서 Domain 호출 0회

### 15.2 Track B — Domain / Logic TDD
Track B는 “불변식과 시도 순서”를 테스트로 고정한다.
- 빈칸 탐색 테스트: row-major 첫/둘째 빈칸
- 누락 숫자 탐색 테스트: 정확히 2개, (small,large)
- 마방진 검증 테스트: 10개 선 합 동일 및 34
- small-first 성공 테스트
- small-first 실패 후 reverse 성공 테스트
- 두 조합 모두 실패 테스트(UNSOLVABLE)

### 15.3 Parallel Progression Rules
- Track A의 RED와 Track B의 RED를 분리한다.
- Track A의 GREEN과 Track B의 GREEN을 각각 최소 구현으로 처리한다.
- REFACTOR 단계에서만 구조 개선을 수행한다.
- Domain을 모두 구현한 뒤 Boundary를 붙이는 방식을 금지한다.
- 테스트를 약화/삭제/skip하여 통과시키는 것을 금지한다.

## 16. Test Plan / QA

### 16.1 Normal Scenarios
- **NS-01 small-first 성공**: Attempt 1에서 마방진 성립 → small-first 출력 반환 (`TD-01`)
- **NS-02 reverse 성공**: Attempt 1 실패, Attempt 2에서 마방진 성립 → reverse 출력 반환 (`TD-02`)
- **NS-03 both-valid (Attempt 1 우선)**: Attempt 1·2 모두 마방진 → Attempt 1 출력 반환 (`TD-07`, `D-T22`)

### 16.2 Exception Scenarios
- **ES-01 invalid size (row/col)**: 4×4 위반 → 해당 Error Code/Message 예외 발생, Domain 미호출
- **ES-02 invalid blank count**: 0 개수≠2 → `INVALID_EMPTY_COUNT`, Domain 미호출
- **ES-03 invalid range**: -1 또는 17 포함 → `OUT_OF_RANGE`, Domain 미호출
- **ES-04 duplicate non-zero**: 중복 값 존재 → `DUPLICATE_VALUE`, Domain 미호출
- **ES-05 unsolvable**: 두 조합 모두 실패 → `UNSOLVABLE`

### 16.3 Boundary Scenarios
- **BS-01 최소값/최대값**: 1과 16을 포함한 유효 입력에서 계약 유지
- **BS-02 0은 빈칸으로만 처리**: 누락 숫자 계산에서 0 제외
- **BS-03 출력 좌표 1-index**: r,c ∈ [1..4]
- **BS-04 반환 배열 길이 6**: 성공 출력은 항상 길이 6

### 16.4 Representative Test Data

각 TD는 **필수 속성**과 **대표 행렬(Appendix 23.5)**을 함께 고정한다. 테스트는 속성·행렬 모두로 RED를 설계할 수 있다.

| ID | 목적 | attempt1_valid | attempt2_valid | 기대 출력 규칙 |
|---|---|:---:|:---:|---|
| TD-01 | small-first만 성공 | true | false | `[r1,c1,small,r2,c2,large]` |
| TD-02 | reverse만 성공 | false | true | `[r1,c1,large,r2,c2,small]` |
| TD-03 | invalid size | — | — | Boundary Error, Domain 미호출 |
| TD-04 | invalid blank count | — | — | `INVALID_EMPTY_COUNT` |
| TD-05 | duplicate value | — | — | `DUPLICATE_VALUE` |
| TD-06 | invalid range | — | — | `OUT_OF_RANGE` |
| TD-07 | both-valid (인위 fixture) | true | true | Attempt 1 우선 (`BR-16`) |

- **TD-03** 예: `[[1,2,3],[4,5,6],[7,8,9]]` (3×3)
- **TD-04** 예: 0이 1개 또는 3개인 4×4
- **TD-05** 예: 동일 비영 값 2회 포함 4×4
- **TD-06** 예: `-1` 또는 `17` 포함 4×4
- **TD-07**: 표준 완성 마방진에서 2칸 제거만으로는 both-valid가 성립하지 않을 수 있음. `Report/02` D-T22처럼 **의도적으로 구성**하며, Appendix 23.5 속성 표를 만족하는 행렬을 테스트 설계 단계에서 확정한다.

## 17. Architecture Overview, High-Level
- **Boundary Layer**:
  - 입력 검증(계약 위반 차단)
  - 오류 코드/메시지 매핑 및 예외 신호
  - 성공 출력 포맷(`int[6]`) 보장
- **Domain Layer**:
  - 빈칸 탐색, 누락 숫자 탐색, 마방진 판정, 두 조합 시도 규칙
  - 순수 로직으로만 구성(외부 I/O 의존 금지)
- **Control / Application Layer (필요 시만)**:
  - Boundary에서 검증된 입력을 Domain 흐름으로 오케스트레이션
  - Attempt 1/2의 실행 순서 및 결과 반환을 조정

**Dependency Direction (고정)**:
- Boundary → Control → Domain
- Domain은 Boundary를 몰라야 한다.
- Domain은 UI/DB/Web/파일시스템에 의존하지 않아야 한다. (근거: `.cursor/rules/magicsquare-ecb-architecture.mdc`)

## 18. Component Candidates
| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| BoundaryValidator | 입력 계약 검증 및 실패 신호(예외) | Boundary | `int[][]` | pass/fail | FR-01 | U-T02~U-T09 성격(계약 위반 시 Domain 미호출) |
| BlankFinder | row-major 첫/둘째 빈칸 좌표 산출(1-index) | Domain | 4×4 grid | (r1,c1),(r2,c2) | FR-02 | D-T05 |
| MissingNumberFinder | 누락 숫자 2개 산출 및 (small,large) 정렬 | Domain | 4×4 grid | (small,large) | FR-03 | D-T06 |
| MagicSquareValidator | 10개 선 합 동일 및 상수 34 판정 | Domain | 완성 4×4 | valid/invalid | FR-04 | D-T01, D-T24 |
| Solver | Attempt 1/2 실행 순서, both-valid 시 Attempt 1 우선, Domain 호출 조율 | Control | 부분 4×4 | SolutionVector | FR-05-A | D-T02, D-T03, D-T14, D-T22 |
| PartialMagicSquareSolver | 조합 생성·`MagicSquareValidator` 호출·UNSOLVABLE 판정 | Domain | 부분 4×4 | SolutionVector / Domain 예외 | FR-05-A | D-T02, D-T03, D-T14 |
| ResultFormatter | SolutionVector → `int[6]`, Boundary Error Code 예외 매핑 | Boundary | SolutionVector | `int[6]` | FR-05-B | BS-04, AC-FR05-07 |

## 19. Risks & Ambiguities
| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index/0-index 혼동 | 출력 계약 위반 및 테스트/구현 불일치 | BR-14/BR-15를 계약으로 고정하고, 성공 출력 r,c 범위 테스트 포함 |
| row-major 첫 빈칸 정의 누락 | 시도 순서가 달라져 결과가 달라짐(결정성 깨짐) | BR-06/BR-07을 요구사항으로 고정하고 D-T05로 보호 |
| small-first vs reverse 데이터 혼동 | Attempt 1/2 로직이 검증되지 않음 | TD-01/TD-02 대표 행렬·속성 표로 분리, NS-01/NS-02 연결 |
| both-valid 시 Attempt 2 반환 | UC-D6 위반, 결정성 깨짐 | BR-16, AC-FR05-05, NS-03, TD-07 |
| 입력 행렬 변경 여부 불명확 | 테스트 간 간섭 및 부작용 발생 | NFR의 “입력 불변”을 고정, 호출 전후 스냅샷 비교 테스트 후보 |
| 두 조합 모두 실패 정책 누락 | 구현마다 다르게 처리되어 회귀 발생 | 섹션 13에서 `UNSOLVABLE` 예외로 단일화 |
| 34 상수 하드코딩 | 의미 상실 및 유지보수 저하 | 금지 규칙에 따라 상수로 명명하고 테스트로 근거 남김 |
| Boundary/Domain 책임 혼합 | 검증/실패 정책이 Domain에 침투 | “검증 실패 시 Domain 미호출”을 Track A 핵심 기준으로 고정 |

## 20. Engineering Principles
(근거: `.cursorrules`, `.cursor/rules/*.mdc`, `Report/03...Implementation_Report.md`)
- **PEP8**: 엄격 준수, 최대 라인 길이 88
- **Type hints**: 모든 함수 파라미터/반환값에 필수
- **pytest**: 테스트 프레임워크로 사용
- **AAA pattern**: Arrange-Act-Assert 순서를 유지
- **Coverage goals**: Domain 95%+, Boundary 85%+
- **ECB separation**: boundary/control/entity(또는 domain) 분리, 의존 방향 강제
- **RED→GREEN→REFACTOR**: RED 확인 없이 구현 금지, GREEN에서 리팩터 금지, REFACTOR는 동작 변경 없이
- **Forbidden**:
  - `print()` 디버깅 금지
  - `bare except` 금지
  - 테스트 약화/삭제/skip 금지
  - 설명 없는 magic number 금지(의미 있는 상수/Enum로 추출)

## 21. Traceability Matrix
| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | AC-FR01-01~02, AC-FR01-04~05 | ES-01, TD-03, U-T02~03 | BoundaryValidator |
| 0=빈칸 의미 | BR-02 | FR-01/FR-03 | AC-FR03-01 | BS-02 | BoundaryValidator, MissingNumberFinder |
| 빈칸 2개 | BR-03 | FR-01/FR-02 | AC-FR01-06, AC-FR02-01 | ES-02, TD-04, D-T05 | BoundaryValidator, BlankFinder |
| 값 범위 0 또는 1~16 | BR-04 | FR-01 | AC-FR01-07 | ES-03, TD-06, U-T06~07 | BoundaryValidator |
| 중복 금지(0 제외) | BR-05 | FR-01 | AC-FR01-08 | ES-04, TD-05, U-T08 | BoundaryValidator |
| null 입력 금지 | BR-01 | FR-01 | AC-FR01-03 | U-T09, TD-03 | BoundaryValidator |
| row-major 첫 번째 빈칸 | BR-06 | FR-02 | AC-FR02-01, AC-FR02-02 | D-T05, TD-01 | BlankFinder |
| row-major 두 번째 빈칸 | BR-07 | FR-02 | AC-FR02-01 | D-T05 | BlankFinder |
| 누락 숫자 2개 | BR-08 | FR-03 | AC-FR03-01 | D-T06 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-09 | FR-03 | AC-FR03-02 | D-T06 | MissingNumberFinder |
| 마방진 상수 34 | BR-10 | FR-04 | AC-FR04-01 | D-T01, B-RED-03 | MagicSquareValidator |
| 행/열/대각선 합 규칙 | BR-11 | FR-04 | AC-FR04-01~03 | D-T24 | MagicSquareValidator |
| 완성 격자 전제(0 없음) | BR-11 | FR-04 | AC-FR04-03 | D-T24 | MagicSquareValidator |
| small-first 시도 | BR-12 | FR-05-A | AC-FR05-01, AC-FR05-05 | NS-01, TD-01, D-T02 | Solver, PartialMagicSquareSolver |
| reverse 시도 | BR-13 | FR-05-A | AC-FR05-02 | NS-02, TD-02, D-T03 | Solver, PartialMagicSquareSolver |
| both-valid Attempt 1 우선 | BR-16 | FR-05-A | AC-FR05-05 | NS-03, TD-07, D-T22 | Solver |
| int[6] 반환 | BR-15 | FR-05-B | AC-FR05-04, AC-FR05-07 | BS-04 | ResultFormatter |
| 1-index 좌표 | BR-14 | FR-02/FR-05-B | AC-FR02-02, AC-FR05-03, AC-FR05-06 | BS-03 | BlankFinder, ResultFormatter |
| UNSOLVABLE | BR-13 | FR-05-A | AC-FR05-02 | ES-05, D-T14, U-T10 | PartialMagicSquareSolver, ResultFormatter |
| 결정성 | — | NFR | AC-NFR-03 | D-T23 | Solver |
| 입력 불변 | — | NFR | AC-NFR-04 | D-T23 | Solver |
| Domain coverage 95%+ | — | NFR | AC-NFR-01 | pytest-cov | Domain tests |
| Boundary coverage 85%+ | — | NFR | AC-NFR-02 | pytest-cov | Boundary tests |
| 성능 50ms | — | NFR | AC-NFR-05 | perf test | End-to-end |

## 22. Open Questions / Decision Needed

### 22.1 확정된 결정 (검토 반영)

| ID | 항목 | 확정 내용 |
|---|---|---|
| **RESOLVED-01** | 실패 신호 (구 DQ-03) | 공개 API 실패는 **Error Code + Message 예외 throw**. sentinel/`int[6]` 실패 반환 **금지** (섹션 13, 13.2) |
| **RESOLVED-02** | both-valid 우선순위 | Attempt 1·2 모두 유효 시 **Attempt 1(조합 A) 반환** — `BR-16`, `AC-FR05-05`, `Report/02` UC-D6 |
| **RESOLVED-03** | 예외 계층 | Domain 내부 예외 → Control → Boundary Error Code 매핑 (섹션 13.2) |
| **RESOLVED-04** | Domain 방어 검증 | 공개 API는 Boundary 선검증; Domain 방어는 내부/단위 테스트 전용, Boundary Code 미노출 |

### 22.2 미결 (Decision Needed)

- **DQ-01 (Source Missing)**: 요구사항/검증 1차 자료 `Report/4.UserJourney_Epic_to_TechnicalScenario_Report.md` 부재. `Report/06`·`Report/01`·`Report/02` 기반으로 작성됨 — 확보 후 Journey/Gherkin 갱신 필요.
- **DQ-02 (Scope Conflict)**: `Report/02` Data Layer vs 본 PRD Out-of-Scope(DB 제외). 저장/로드 포함 여부 제품 결정 필요.

## 23. Appendix

### 23.1 참고 문서 목록
- `Report/01.MagicSquare_ProblemDefinition_Report.md`
- `Report/02.MagicSquare_DualTrack_TDD_CleanArchitecture_Design.md`
- `Report/03.CursorRules_and_UserEntity_Implementation_Report.md`
- `Report/04.CursorAgents_Setup_Report.md` (규칙 자체의 근거는 아니며, 운영 참고)
- `.cursorrules`
- `.cursor/rules/magicsquare-project.mdc`
- `.cursor/rules/magicsquare-ecb-architecture.mdc`
- `.cursor/rules/magicsquare-python-code-style.mdc`
- `.cursor/rules/magicsquare-tdd-testing.mdc`
- `.cursor/rules/magicsquare-forbidden.mdc`

### 23.2 Cursor Rules 요약(핵심)
- ECB 의존 방향: Boundary→Control→Domain(Entity)
- RED 확인 없는 구현 금지, GREEN에서 리팩터 금지, REFACTOR는 동작 불변
- 타입힌트 필수, PEP8 준수
- `print()` 금지, bare except 금지, 매직 넘버 금지, 테스트 약화 금지

### 23.3 대표 Gherkin Scenario 요약(본 PRD 버전)
- **Scenario: small-first로 성공한다** (NS-01 / TD-01)
  - Given: 4×4 입력, 0이 2개, 범위/중복 규칙 만족
  - When: Attempt 1(small-first)로 빈칸을 채운다
  - Then: 완성 격자는 10개 선 합이 모두 34이고, 출력은 `[r1,c1,small,r2,c2,large]`다
- **Scenario: small-first 실패 후 reverse로 성공한다** (NS-02 / TD-02)
  - Given: 동일한 입력 계약
  - When: Attempt 1은 실패하고 Attempt 2(reverse)를 시도한다
  - Then: 출력은 `[r1,c1,large,r2,c2,small]`다
- **Scenario: 두 조합 모두 유효할 때 Attempt 1을 반환한다** (NS-03 / TD-07 / D-T22)
  - Given: Attempt 1·2가 모두 마방진이 되는 인위 fixture
  - When: solve를 호출한다
  - Then: 출력은 Attempt 1 순서 `[r1,c1,small,r2,c2,large]`이며 Attempt 2는 시도하지 않거나 시도해도 결과에 영향 없음
- **Scenario: 두 조합 모두 실패한다** (ES-05)
  - Given: 동일한 입력 계약
  - When: Attempt 1/2 모두 마방진을 만들지 못한다
  - Then: `UNSOLVABLE` 예외(코드+메시지)가 발생한다

> 위 Gherkin·Test ID는 **실행 코드가 아닌** 설계 식별자이다.

### 23.4 향후 RED Test ID 후보(예시)
- Track A: A-RED-01(null), A-RED-02(size), A-RED-03(blank count), A-RED-04(range), A-RED-05(duplicate), A-RED-06(domain not called)
- Track B: B-RED-01(first blank), B-RED-02(missing pair), B-RED-03(validate 34), B-RED-04(attempt1 success), B-RED-05(attempt2 success), B-RED-06(unsolvable), B-RED-07(both-valid priority)

### 23.5 대표 Fixture 행렬 (검토 반영)

표준 4×4 마방진(상수 34)에서 2칸을 `0`으로 둔 **검증된 대표 행렬**이다. row-major 첫 빈칸·둘째 빈칸·누락 숫자는 아래와 같다.

**TD-01 — Attempt 1만 성공 (small-first)**

```
행렬 (4×4):
[16,  0,  2,  0]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]

첫 빈칸 (1,2), 둘째 빈칸 (1,4) | 누락: small=3, large=13
attempt1_valid=true, attempt2_valid=false
```

**TD-02 — Attempt 2만 성공 (reverse)**

```
행렬 (4×4):
[ 0,  0,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]

첫 빈칸 (1,1), 둘째 빈칸 (1,2) | 누락: small=3, large=16
attempt1_valid=false, attempt2_valid=true
```

**TD-07 — both-valid (속성만 고정, 행렬은 테스트 설계 시 구성)**

| 속성 | 값 |
|---|---|
| attempt1_valid | true |
| attempt2_valid | true |
| 기대 출력 | Attempt 1: `[r1,c1,small,r2,c2,large]` |
| 근거 | `Report/02` D-T22, UC-D6 |

> TD-07 구체 행렬은 표준 완성 마방진 2칸 제거만으로는 성립하지 않을 수 있으므로, RED 설계 시 위 속성을 만족하는 인위 fixture를 생성한다.
