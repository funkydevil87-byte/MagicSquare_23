# PRD — Magic Square 4×4 TDD Practice

| 항목 | 내용 |
|------|------|
| **문서 ID** | PRD-MS-001 |
| **프로젝트** | MagicSquare_1004 |
| **버전** | 0.2 |
| **상태** | 구현 전 기준 문서 (SSOT) |
| **SSOT 참조** | Report/01, Report/02, Report/03, Report/05, Report/06, `.cursorrules` |
| **작성일** | 2026-05-23 |
| **개정** | v0.2 — Report/06 Review P0~P1 반영 (입력/출력 인덱스, E007 매핑, Domain 예외 AC, Success envelope) |

---

## 1. Executive Summary

Magic Square 4×4 TDD Practice는 **빈칸 2개가 있는 4×4 부분 격자**를 입력받아, 누락된 두 숫자의 배치를 결정하고 **`int[6]` 형식의 좌표·값 결과**를 반환하는 순수 로직 프로그램이다. 본 프로젝트의 목적은 알고리즘 난이도가 아니라 **불변식(Invariant) 중심 설계·검증·구현 체계**를 훈련하는 것이다.

| 역량 | 정의 |
|------|------|
| **불변식 사고** | I1~I11을 컴포넌트·유스케이스에 귀속하고, 판정 기준을 명시적 진술로 표현한다. |
| **입력/출력 계약** | `4×4 int[][]` 입력과 `int[6]` 출력, E001~E007 오류 스키마를 구현 전에 고정한다. |
| **Dual-Track TDD** | Track A(Boundary/UI Contract)와 Track B(Domain/Logic Invariant)를 분리하여 RED→GREEN→REFACTOR를 수행한다. |
| **설계→테스트→구현→리팩토링** | Concept → Rule → Use Case → Contract → Test → Component 추적성을 유지한다. |

---

## 2. Background

4×4 마방진은 1~16의 서로 다른 정수를 4×4 격자에 배치할 때, **4개 행 + 4개 열 + 2개 대각선 = 10개 선**의 합이 모두 동일(M=34)해지는 배치 문제이다.

| 관찰 | 의미 |
|------|------|
| 규모 | 4×4는 학습 가능한 구성 규칙이 존재하고, 검증(10선 합 비교)이 기계적으로 명확하다. |
| 본질 | 탐색 문제처럼 보이나, **불변 조건(I1~I5) 동시 만족 문제**이다. |
| 수동 한계 | 10선 동시 추적, 검증 10회, 중복·누락 판별, 다중 해 존재로 인지·연산 비용이 크다. |

본 PRD는 “마방진 퍼즐 앱”이 아니라, **검증 가능한 계약(Contract)을 먼저 고정하고 TDD로 구현하는 훈련 프로젝트**를 정의한다. UI, DB, Web 의존성 없이 Boundary·Domain·Control 계층과 pytest 기반 Dual-Track TDD만으로 완결 가능한 범위를 다룬다.

---

## 3. Problem Statement

### 3.1 표면 문제 (PRD에서 배제)

> 「1~16을 4×4 칸에 넣어 합이 34가 되게 만든다.」

위 정의는 행위만 기술하며, 판정 기준·책임 범위·재현 가능성·실패 정책이 없어 테스트 불가능하다.

### 3.2 정확한 문제 정의

> **1~16의 서로 다른 정수를 4×4 격자에 배치할 때, 빈칸 2개(값 `0`)가 있는 부분 격자를 입력받아, 누락 숫자 2개의 유일한 유효 배치를 결정하고, 1-index 좌표와 값을 `int[6]`으로 반환한다. 입력 형식 위반은 Boundary에서 차단하고, Domain 해결 불가는 E006으로 반환한다.**

### 3.3 입력/출력 계약이 핵심인 이유

| 이유 | 설명 |
|------|------|
| 테스트 작성 가능 | 명확한 I/O 없이는 Given-When-Then·AAA 테스트를 작성할 수 없다. |
| Boundary/Domain 분리 | 입력 스키마(E001~E005)는 Boundary, 불변식(I1~I11)은 Domain 책임으로 분리된다. |
| 회귀 보호 | REFACTOR 후에도 외부 계약(E001~E007 message, `int[6]` 형식)이 불변이어야 한다. |
| 추적성 | Concept → Rule → Use Case → Contract → Test → Component 체인의 종착점이 계약이다. |

---

## 4. Why Now / Why Chain

### 4.1 Why Chain

```
[Why #1] 유효한 4×4 배치를 일관되게 판정·확보·공유해야 한다.
    ↓
[Why #2] 수동 계산은 반복·자동검증·오류방지·규칙 명시화에 한계가 있다.
    ↓
[Why #3] TDD는 “테스트 먼저”가 아니라, 통제 대상·불변식·I/O 계약을 구현 전에 고정하는 설계 방식이다.
    ↓
[Why Now] Dual-Track TDD + ECB로 Boundary/Domain 분리·계약 기반 RED→GREEN→REFACTOR를 훈련할 타이밍이다.
```

### 4.2 학습자 Pain Point

| Pain Point | PRD 대응 |
|------------|----------|
| 구현을 먼저 시작함 | RED phase: 실패 테스트 선작성, pytest RED 확인 후 구현 |
| 테스트 기준이 불명확함 | FR별 AC, Business Rules, Error Policy, Traceability Matrix |
| Boundary와 Domain 책임이 섞임 | ECB 레이어 정의, 입력 검증 실패 시 Domain 0회 호출 |
| 리팩토링 후 계약이 깨짐 | REFACTOR phase: 기능·공개 API·E001~E007 message 불변 |

---

## 5. Target Users

| 사용자 | 역할 | 사용 환경 |
|--------|------|-----------|
| **TDD 학습자** | RED→GREEN→REFACTOR 사이클 수행 | pytest 실행, 콘솔/IDE |
| **코드 리뷰어** | ECB 경계·계약·테스트 추적성 검토 | PR, Traceability Matrix |
| **Clean Architecture·ECB 훈련 개발자** | Boundary/Control/Entity 분리 실습 | `src/`, `tests/` 디렉터리 |

**범위 밖 환경:** UI 화면, DB, Web/API 서버, 네트워크, 외부 서비스.

---

## 6. Vision & Epic Goal

### 6.1 Epic

**「불변식 기반 사고 훈련 시스템 구축」** (Magic Square 4×4 TDD Practice)

### 6.2 Business Goal

4×4 Magic Square **부분 격자(빈칸 2개)** 문제를 도메인으로, **Concept → Invariant → Contract → Test → Component** 추적 가능한 소프트웨어를 완성한다. 핵심 가치는 “정답 프로그램”이 아니라 **계약 기반 설계·검증·리팩토링 훈련**이다.

### 6.3 Epic Success Criteria

| ID | 기준 | 검증 방법 |
|----|------|-----------|
| SC-01 | 유효 입력 → `int[6]` 반환 | IT-01, U-OUT-01 |
| SC-02 | invalid 입력 → E001~E005; Domain 0회 호출 | U-IN-*, U-FLOW-02, IT-E01~E02, IT-E05 |
| SC-03 | Domain 불가 → E006 | D-SOL-03, U-OUT-03, IT-E03 |
| SC-04 | Domain Logic line coverage ≥ 95% | pytest-cov |
| SC-05 | REFACTOR 후 E001~E007 message·`int[6]` 형식 불변 | RG-01, RG-02 |
| SC-06 | 정답·매직 넘버 하드코딩 금지 | 코드 리뷰, NFR-09, `MagicConstant` SSOT |
| SC-07 | I1~I11 각각 ≥1 Test ID 연결 | §21 Traceability Matrix |

---

## 7. Persona

**지민** — TDD·Clean Architecture 학습 중인 개발자.

| 속성 | 내용 |
|------|------|
| 목표 | 알고리즘 정답보다 설계·계약·테스트·리팩토링 흐름 훈련 |
| Pain | Boundary/Domain 혼합, 테스트 기준 모호, REFACTOR 후 계약 붕괴 |
| 성공 | US-01~05 AC 통과, Dual-Track GREEN, Traceability Matrix 유지 |

---

## 8. User Journey Summary

| Stage | User Action | Pain Point | Learning Outcome |
|-------|-------------|------------|-------------------|
| **1. Problem Recognition** | Report·I1~I11 paraphrase | “16칸 채우기”와 “조건 만족” 혼동 | 설계 훈련 문제로 재정의 |
| **2. Contract Definition** | Input/Output/Error schema 표 작성 | Boundary vs Domain 전제 혼합 | E001~E007, `int[6]` 계약 고정 |
| **3. Domain Separation** | ECB 컴포넌트 배치 | 책임 혼합, cross-layer import | SRP, I6~I11 검증 주체 명확 |
| **4. Dual-Track TDD** | U-*/D-* RED 순서 실행 | Domain Mock 남용, 선제 구현 | RED→GREEN→REFACTOR 리듬 |
| **5. Regression Protection** | Edge·IT-* 보강 | REFACTOR 후 계약 깨짐 | RG-01~06, 커버리지 목표 유지 |

---

## 9. Scope

### 9.1 In-Scope

| ID | 항목 | User Story |
|----|------|------------|
| S-01 | Boundary 입력 검증 (E001~E005) | US-01 |
| S-02 | 빈칸 좌표 탐색 (row-major, 1-index) | US-02 |
| S-03 | 누락 숫자 탐색 (0 제외, 오름차순) | US-03 |
| S-04 | 완전 격자 마방진 판정 (I1~I5) | US-04 |
| S-05 | 두 조합 시도 Solver + `int[6]` 반환 | US-05 |
| S-06 | Boundary 출력 직렬화·에러 매핑 (E006, E007) | US-01, US-05 |
| S-07 | Dual-Track TDD (U-*, D-*) | — |
| S-08 | End-to-End Integration (IT-01, IT-03, IT-E*) | — |

### 9.2 Out-of-Scope

| 항목 | 사유 |
|------|------|
| UI 화면 개발 | Boundary contract-first; UI shell 미정 |
| DB 저장/검색 | Report/02 Data Layer는 Phase 2 |
| Web/API 서버 | 순수 로직·pytest 중심 |
| N×N 일반화 | 4×4 고정 |
| 완전 마방진 생성 알고리즘 | 부분 격자 solve만 In-Scope |
| 사용자 인증/권한 | 도메인 무관 |
| 네트워크 오류 처리 | I/O 범위 밖 |
| QR 스캔, 외부 서비스 | 범위 밖 |
| User Entity (Report/03) | ECB 워밍업용; 본 PRD 범위 밖 |

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary)

- **Description:** 호출자가 전달한 `4×4 int[][]` 입력을 Boundary에서 검증한다. 위반 시 Error schema를 반환하고 Domain resolver를 호출하지 않는다.
- **Layer:** Boundary
- **Input:** `matrix: int[][] | null` (0-index 배열; §12.1)
- **Processing Rules:**
  1. `matrix == null` → E003
  2. `length(matrix) != 4` 또는 임의 행 `length != 4` → E001
  3. `count(v==0) != 2` → E002
  4. 임의 셀 `v ∉ {0} ∪ {1..16}` → E004
  5. `{v | v≠0}` 원소 distinct 위반 → E005
  6. 검증 순서: null → size → empty count → value range → duplicate
  7. 1~5 모두 통과 시 Domain resolver **정확히 1회** 호출
- **Output:** 검증 통과 → Control/Domain 호출 허용; 실패 → `{ type: "ERROR", error: { code, message } }`
- **Acceptance Criteria:**
  - AC-FR01-01: `null` → E003, Domain 0회
  - AC-FR01-02: 3×4 → E001, Domain 0회
  - AC-FR01-03: 4행 중 1행 length=3 → E001, Domain 0회
  - AC-FR01-04: 빈칸 0개 또는 3개 → E002, Domain 0회
  - AC-FR01-05: 셀 `-1` 또는 `17` → E004, Domain 0회
  - AC-FR01-06: non-zero `5` 중복 → E005, Domain 0회
  - AC-FR01-07: 유효 G1 → Domain **1회** 호출
  - AC-FR01-08: size 위반 입력 → Domain **0회**; null 검증이 선행됨 (U-FLOW-02)
- **Error / Exception Policy:** E001~E005 (§13 참조)
- **Related Business Rules:** BR-01~BR-05, BR-19
- **Related Test Direction:** Track A — U-IN-01~08, U-FLOW-01~02, IT-E01, IT-E02, IT-E05
- **Component Candidate:** `InputValidator`, `UIBoundary`

---

### FR-02 Blank Coordinate Discovery (Domain)

- **Description:** 검증된 격자에서 값 `0`인 칸 2개의 1-index 좌표를 row-major 순으로 탐색한다.
- **Layer:** Domain (Entity/Service)
- **Input:** `Grid` (빈칸 정확히 2개 전제; Boundary에서 보장)
- **Processing Rules:**
  1. `r=1..4`, `c=1..4` row-major 스캔
  2. 첫 번째 `0` → `first=(r,c)`; row-major 상 first 이후 다음 `0` → `second=(r,c)`
  3. 빈칸 ≠ 2 → `InvalidGridStateError` (Boundary 통과 입력에서는 발생하지 않음; §13.2)
- **Output:** `EmptyCellPair{ first: CellCoordinate, second: CellCoordinate }` (1-index)
- **Acceptance Criteria:**
  - AC-FR02-01: G1 → `first=(2,2)`, `second=(3,3)`
  - AC-FR02-02: G2 → `first=(3,3)`, `second=(4,4)`
  - AC-FR02-03: 빈칸 (1,1),(4,4) → `first=(1,1)`, `second=(4,4)`
  - AC-FR02-04: 빈칸 (2,4),(3,1) → `first=(2,4)`, `second=(3,1)`
  - AC-FR02-05: 빈칸 1개 Grid → `InvalidGridStateError` (D-LOC-02, Domain 단위 테스트 direct call)
  - AC-FR02-06: 빈칸 3개 Grid → `InvalidGridStateError` (D-LOC-03)
- **Error / Exception Policy:** `InvalidGridStateError` → Boundary E007 (§13.2)
- **Related Business Rules:** BR-06, BR-06a, BR-12
- **Related Test Direction:** Track B — D-LOC-01~05
- **Component Candidate:** `EmptyCellLocator`

---

### FR-03 Missing Number Discovery (Domain)

- **Description:** 격자에 없는 `{1..16}` 원소 2개를 찾고 `(smaller, larger)` 순으로 반환한다. `0`은 누락 후보에서 제외한다.
- **Layer:** Domain
- **Input:** `Grid` (0 제외 14개 distinct, 각 1~16)
- **Processing Rules:**
  1. present = `{v | v≠0}`
  2. missing = `{1..16} \ present`
  3. `|missing| == 2` → `(smaller, larger)` where `smaller ≤ larger`
  4. `0`을 missing 후보에 포함하지 않음
- **Output:** `MissingNumberPair{ smaller: int, larger: int }`
- **Acceptance Criteria:**
  - AC-FR03-01: G1 → `smaller=7`, `larger=10`
  - AC-FR03-02: G2 → `smaller=1`, `larger=6`
  - AC-FR03-03: 누락 `{1,16}` → `smaller=1`, `larger=16`
  - AC-FR03-04: 1~16 외 non-zero 값 포함 Grid → `InvalidNumberSetError` (D-MIS-02)
- **Error / Exception Policy:** `InvalidNumberSetError` → Boundary E007 (§13.2)
- **Related Business Rules:** BR-07, BR-08, BR-13
- **Related Test Direction:** Track B — D-MIS-01~03
- **Component Candidate:** `MissingNumberFinder`

---

### FR-04 Magic Square Validation (Domain)

- **Description:** **0이 없는** 완전 채워진 4×4 격자가 I1~I5를 모두 만족하는지 `boolean`으로 판정한다.
- **Layer:** Domain
- **Input:** `Grid` (완전 채워짐)
- **Processing Rules:**
  1. I1: 모든 행 합 = M
  2. I2: 모든 열 합 = M
  3. I3: 주대각·부대각 합 = M
  4. I4: 값 집합 = {1..16} 각 1회
  5. I5: M = 34 (`MagicConstant` SSOT)
  6. `0` 하나라도 포함 → `false` (예외 아님)
  7. I1~I5 중 하나라도 위반 → `false`
- **Output:** `true` | `false`
- **Acceptance Criteria:**
  - AC-FR04-01: G0(완전 유효) → `true`
  - AC-FR04-02: 행 1개 합 불일치 → `false`
  - AC-FR04-03: 열 1개 합 불일치 → `false`
  - AC-FR04-04: 대각선 1개 불일치 → `false`
  - AC-FR04-05: 1~16 중복 → `false`
  - AC-FR04-06: `0` 포함 → `false`
- **Error / Exception Policy:** 판정 실패는 `false` 반환; 예외 아님
- **Related Business Rules:** BR-09~BR-11
- **Related Test Direction:** Track B — D-VAL-01~06
- **Component Candidate:** `MagicSquareValidator`

---

### FR-05 Two-Combination Solver and Result Formatting

- **Description:** Step A(작은수→첫빈칸, 큰수→둘째빈칸) 시도 후 실패 시 Step B(반대) 시도. 성공 시 Success schema 반환; 둘 다 실패 시 E006.
- **Layer:** Domain (Solver) + Boundary (ResultFormatter)
- **Input:** `Grid` (I6·I7 전제)
- **Processing Rules:**
  1. `firstEmpty`, `secondEmpty` = FR-02 결과
  2. `smaller`, `larger` = FR-03 결과
  3. **Step A:** `gridA = copy(grid)`; `gridA[r1][c1]=smaller`; `gridA[r2][c2]=larger`; `isValidComplete(gridA)==true` → `[r1,c1,smaller,r2,c2,larger]`
  4. **Step B:** `gridB = copy(grid)`; `gridB[r1][c1]=larger`; `gridB[r2][c2]=smaller`; `isValidComplete(gridB)==true` → `[r1,c1,larger,r2,c2,smaller]`
  5. Step A·B 모두 `false` → `UnsolvableDomainError` → Boundary **E006**
  6. Solver는 **입력 Grid를 변경하지 않는다** (copy 사용)
  7. Boundary는 Domain `SolutionResult` → Success schema 직렬화; 좌표 1-index 유지
- **Output:** `{ type: "OK", data: int[6] }` where `data = [r1,c1,n1,r2,c2,n2]` (§12.2)
- **Acceptance Criteria:**
  - AC-FR05-01: G1 Step A 성공 → `data == [2,2,7,3,3,10]`
  - AC-FR05-02: G2 Step A 실패·Step B 성공 → `data == [3,3,6,4,4,1]`
  - AC-FR05-03: G3 Step A·B 모두 실패 → E006
  - AC-FR05-04: `len(data) == 6`
  - AC-FR05-05: `r1,c1,r2,c2` 각각 `1 ≤ v ≤ 4`
  - AC-FR05-06: `{n1,n2} == {smaller,larger}`
  - AC-FR05-07: Success 응답에 `error` 필드 없음 (UX-05)
  - AC-FR05-08: Domain `InvalidGridStateError` 또는 `InvalidNumberSetError` → E007 (U-OUT-03 패턴)
- **Error / Exception Policy:** `UnsolvableDomainError` → E006; `InvalidGridStateError`, `InvalidNumberSetError` → E007 (§13)
- **Related Business Rules:** BR-12~BR-16, BR-20
- **Related Test Direction:** Track B — D-SOL-01~03; Track A — U-OUT-01~03; IT-01, IT-03, IT-E03
- **Component Candidate:** `TwoCellSolver`, `UIBoundary`, `ErrorMapper`, `SolvePartialMagicSquare` (Control)

---

## 11. Business Rules / Domain Rules

| ID | 규칙 | 검증 주체 |
|----|------|-----------|
| **BR-01** | 입력 행렬은 `4×4` (`length==4`, 각 행 `length==4`) | Boundary |
| **BR-02** | 빈칸(`0`)은 **정확히 2개** | Boundary |
| **BR-03** | 각 셀 값은 `0` 또는 `1 ≤ v ≤ 16` | Boundary |
| **BR-04** | `0`을 제외한 값은 **중복 없음** (distinct) | Boundary |
| **BR-05** | Boundary 입력 검증 실패 시 Domain resolver **0회** 호출 | Boundary |
| **BR-06** | 첫 번째 빈칸 = row-major(`r=1..4`, `c=1..4`) 스캔 시 **처음** 발견된 `0` | Domain |
| **BR-06a** | 두 번째 빈칸 = first 이후 row-major 스캔에서 **다음** `0` | Domain |
| **BR-07** | 누락 숫자 = `{1..16} \ {v≠0}` **정확히 2개** | Domain |
| **BR-08** | 누락 숫자 쌍은 `(smaller, larger)` where `smaller ≤ larger` | Domain |
| **BR-09** | 완전 격자에서 모든 행 합 = M | Domain |
| **BR-10** | 완전 격자에서 모든 열 합 = M | Domain |
| **BR-11** | 완전 격자에서 주대각·부대각 합 = M; M = **34** (`MagicConstant` SSOT) | Domain |
| **BR-12** | Domain·출력 좌표 `(r,c)`는 **1-index** (`1 ≤ r,c ≤ 4`) | Domain + Boundary |
| **BR-13** | `0`은 빈칸으로만 해석; 누락 숫자 후보에서 **제외** | Domain |
| **BR-14** | Step A: `(smaller→firstEmpty, larger→secondEmpty)` 유효 시 `(n1,n2)=(smaller,larger)` | Domain |
| **BR-15** | Step B: `(larger→firstEmpty, smaller→secondEmpty)` 유효 시 `(n1,n2)=(larger,smaller)` | Domain |
| **BR-16** | Success `data` = `int[6]` = `[r1,c1,n1,r2,c2,n2]`; `length==6` | Boundary |
| **BR-17** | 동일 입력 → 동일 출력 (결정성) | System |
| **BR-18** | Solver/Validator는 입력 Grid **원본을 변경하지 않음** | Domain |
| **BR-19** | Caller 입력 `matrix[r][c]`는 **0-index** (`0≤r,c≤3`); Boundary가 Domain VO 변환 시 1-index 매핑 | Boundary |
| **BR-20** | Success 응답 `{ type: "OK", data: int[6] }`; Failure `{ type: "ERROR", error: { code, message } }`; 두 schema 혼재 금지 | Boundary |

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Error Code |
|--------------|------|------|---------------|-----------------|------------|
| `matrix` | `int[][]` | non-null | 4×4 배열 | `null` | E003 |
| `matrix.length` | `int` | `== 4` | `4` | `3` | E001 |
| `matrix[r].length` | `int` | `== 4` (0≤r≤3) | `4` | `3` | E001 |
| `matrix[r][c]` index | — | **0-index** (`0≤r,c≤3`) | `matrix[1][1]` = G1 center | — | — |
| `matrix[r][c]` value | `int` | `0` 또는 `1≤v≤16` | `0`, `7`, `16` | `-1`, `17` | E004 |
| empty count | — | `count(v==0) == 2` | G1 (2개 0) | 0개 또는 3개 0 | E002 |
| non-zero values | — | distinct | `{1..16}` subset | two `8`s | E005 |

**인덱스 규칙 (확정):**

- Caller가 전달하는 `matrix`는 Java/Python **0-index** 2차원 배열이다.
- Domain 내부 좌표 및 출력 `[r1,c1,...]`는 **1-index** (`1≤r,c≤4`)이다.
- Boundary가 0-index 배열 → Domain Grid(1-index) 변환을 담당한다.

### 12.2 Output Contract (Success)

| Field / Item | Type | Rule | Valid Example | Invalid Example |
|--------------|------|------|---------------|-----------------|
| `type` | `string` | `"OK"` | `"OK"` | `"ERROR"` |
| `data` | `int[6]` | `[r1,c1,n1,r2,c2,n2]`, 1-index | `[2,2,7,3,3,10]` | length≠6 |
| `r1,c1,r2,c2` | `int` | `1 ≤ v ≤ 4` | `2,2,3,3` | `0,5` |
| `n1,n2` | `int` | `1≤v≤16`, `n1≠n2`, missing pair 일치 | `7,10` | `7,7` |
| error field | — | Success 시 **없음** | — | `error` 키 존재 |

**Canonical Success Shape (확정):**

```json
{ "type": "OK", "data": [2, 2, 7, 3, 3, 10] }
```

### 12.3 Output Contract (Failure)

| Condition | type | code | message | Domain 호출 |
|-----------|------|------|---------|-------------|
| null matrix | ERROR | E003 | `INVALID_MATRIX_NULL: matrix must not be null` | 0회 |
| size ≠ 4×4 | ERROR | E001 | `INVALID_MATRIX_SIZE: expected 4x4` | 0회 |
| empty ≠ 2 | ERROR | E002 | `INVALID_EMPTY_COUNT: expected exactly 2 empty cells (0)` | 0회 |
| value out of range | ERROR | E004 | `INVALID_CELL_VALUE: each cell must be 0 or 1..16` | 0회 |
| duplicate non-zero | ERROR | E005 | `DUPLICATE_VALUE: non-zero values must be unique` | 0회 |
| both combinations invalid | ERROR | E006 | `UNSOLVABLE: no valid magic square completion` | 1회 |
| InvalidGridStateError | ERROR | E007 | `INTERNAL_ERROR: unexpected domain failure` | 1회 |
| InvalidNumberSetError | ERROR | E007 | `INTERNAL_ERROR: unexpected domain failure` | 1회 |

---

## 13. Error / Failure Policy

### 13.1 Boundary Input Errors (E001~E005)

| # | 조건 | Error Code | Layer | Domain 호출 | Related AC |
|---|------|------------|-------|-------------|------------|
| 1 | `matrix == null` | E003 | Boundary | **0회** | AC-FR01-01 |
| 2 | 행≠4 또는 열≠4 | E001 | Boundary | **0회** | AC-FR01-02, AC-FR01-03 |
| 3 | `count(0) ≠ 2` | E002 | Boundary | **0회** | AC-FR01-04 |
| 4 | 값 ∉ {0}∪{1..16} | E004 | Boundary | **0회** | AC-FR01-05 |
| 5 | non-zero 중복 | E005 | Boundary | **0회** | AC-FR01-06 |

### 13.2 Domain Exception → Boundary Code Mapping (확정)

| Domain Exception | 발생 조건 | Boundary Code | Domain 호출 | Related AC | Test ID |
|------------------|-----------|---------------|-------------|------------|---------|
| `UnsolvableDomainError` | Step A·B 모두 invalid | **E006** | 1회 | AC-FR05-03 | D-SOL-03, U-OUT-03, IT-E03 |
| `InvalidGridStateError` | 빈칸 ≠ 2 (Domain direct call) | **E007** | 1회 | AC-FR02-05, AC-FR02-06, AC-FR05-08 | D-LOC-02, D-LOC-03 |
| `InvalidNumberSetError` | present set invalid | **E007** | 1회 | AC-FR03-04, AC-FR05-08 | D-MIS-02 |

**Runtime Invariant:** Boundary 검증 통과 입력은 I6·I7을 보장한다. 정상 E2E 경로에서 `InvalidGridStateError`·`InvalidNumberSetError`는 발생하지 않는다. 해당 예외는 Domain 단위 테스트(direct call) 및 Boundary 버그 방어 경로에서 E007로 매핑한다.

### 13.3 Message Immutability

- E001~E007 message 문자열은 **대소문자·구두점 포함 완전 일치** (Report/02 §2.4, RG-01).
- message 변경 시 U-IN-*·U-OUT-* 테스트 **전부 동시 갱신**.

---

## 14. Non-Functional Requirements

| ID | 요구사항 | 측정/검증 |
|----|----------|-----------|
| NFR-01 | Domain Logic line coverage **≥ 95%** | pytest-cov, Dual-Track 분리 측정 |
| NFR-02 | Boundary Validation line coverage **≥ 85%** | pytest-cov |
| NFR-03 | 프로젝트 전역 line coverage **≥ 80%** (REFACTOR gate) | pytest-cov |
| NFR-04 | **결정성:** 동일 입력 → 동일 출력 | U-OUT-01 반복, IT-01 |
| NFR-05 | **부수효과 없음:** Solver/Validator는 입력 `matrix`/`Grid` **원본을 변경하지 않음** | 입력 deep copy 비교 assert |
| NFR-06 | **성능:** 4×4 단일 solve E2E **≤ 50ms** (로컬 pytest) | IT-01 타이밍 |
| NFR-07 | Boundary와 Domain **책임 분리** (ECB cross-layer import 금지) | import 감사 |
| NFR-08 | **매직 넘버 금지:** M=34 등은 `MagicConstant` SSOT | forbidden 규칙, SC-06 |
| NFR-09 | **정답 하드코딩 금지:** Solver는 Validator 기반 조합 시도만 | SC-06, D-SOL-*, 코드 리뷰 |
| NFR-10 | REFACTOR 후 E001~E007 message·Success/Failure schema **불변** | RG-01, RG-02 |

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD

| 항목 | 규칙 |
|------|------|
| 대상 | `InputValidator`, `UIBoundary`, `ErrorMapper` |
| Mock | Control/Entity **Mock 허용** |
| RED 테스트 | U-IN-01~08, U-OUT-01~03, U-FLOW-01~02 |
| 검증 | 입력 검증, Success/Failure schema, E001~E007 message, Domain 0/1회 |

### 15.2 Track B — Domain / Logic TDD

| 항목 | 규칙 |
|------|------|
| 대상 | `Grid`, Domain Services, `SolvePartialMagicSquare` |
| Mock | Domain **Mock 금지** |
| RED 테스트 | D-VAL-01~06, D-LOC-01~05, D-MIS-01~03, D-SOL-01~03 |
| 검증 | I1~I11, Step A/B, Domain 예외 |

### 15.3 Parallel Progression Rules

| # | 규칙 |
|---|------|
| P-01 | UI RED와 Logic RED를 **분리** |
| P-02 | UI GREEN과 Logic GREEN을 각각 **최소 구현** |
| P-03 | **REFACTOR**에서만 구조 개선; 계약 불변 |
| P-04 | Domain 완료 후 Boundary 일방향 순서 **금지** — Track 병행 허용 |
| P-05 | assert 완화·삭제·skip·xfail·Mock 남용 **금지** |
| P-06 | RED 확인 없이 production 코드 **금지** |

**권장 RED 순서:**

```
Track A: U-IN-01~08 → U-FLOW-02 → U-OUT-01~03
Track B: D-VAL-01 → D-LOC-01 → D-MIS-01 → D-SOL-01 (G1) → D-SOL-02 (G2) → D-SOL-03 (G3)
Integration: IT-01 → IT-03 → IT-E02, IT-E03, IT-E05
```

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios

| ID | 시나리오 | Given | Then | Test ID |
|----|----------|-------|------|---------|
| NS-01 | Step A (small-first) 성공 | G1 | `data == [2,2,7,3,3,10]` | D-SOL-01, IT-01 |
| NS-02 | Step A 실패 → Step B (reverse) 성공 | G2 | `data == [3,3,6,4,4,1]` | D-SOL-02, IT-03 |

### 16.2 Exception Scenarios

| ID | 시나리오 | Then | Test ID |
|----|----------|------|---------|
| ES-01 | 4×4 아님 | E001, Domain 0회 | U-IN-02, IT-E01 |
| ES-02 | 빈칸 1개 | E002, Domain 0회 | U-IN-04, IT-E02 |
| ES-03 | null | E003, Domain 0회 | U-IN-01 |
| ES-04 | 값 17 | E004, Domain 0회 | U-IN-07 |
| ES-05 | non-zero 중복 | E005, Domain 0회 | U-IN-08, IT-E05 |
| ES-06 | 두 조합 모두 실패 | E006 | D-SOL-03, IT-E03 |

### 16.3 Boundary Scenarios

| ID | 검증 | Then | Test ID |
|----|------|------|---------|
| BS-01 | 최소값 1 | missing `{1,x}` → smaller=1 | D-MIS-03 |
| BS-02 | 최대값 16 | missing `{x,16}` → larger=16 | D-MIS-03 |
| BS-03 | `0`은 빈칸만 | `isValidComplete` with 0 → false | D-VAL-06 |
| BS-04 | 출력 1-index | r,c ∈ [1,4] | U-OUT-02 |
| BS-05 | 반환 length=6 | `len(data)==6` | U-OUT-01 |

### 16.4 Representative Test Data

#### G0 — 완전 유효 마방진

| | c1 | c2 | c3 | c4 |
|---|-----|-----|-----|-----|
| r1 | 16 | 3 | 2 | 13 |
| r2 | 5 | 10 | 11 | 8 |
| r3 | 9 | 6 | 7 | 12 |
| r4 | 4 | 15 | 14 | 1 |

#### G1 — Step A (small-first) 성공

| | c1 | c2 | c3 | c4 |
|---|-----|-----|-----|-----|
| r1 | 16 | 3 | 2 | 13 |
| r2 | 5 | **0** | 11 | 8 |
| r3 | 9 | 6 | **0** | 12 |
| r4 | 4 | 15 | 14 | 1 |

- 1-index: first=(2,2), second=(3,3); missing {7,10}
- **기대:** `[2,2,7,3,3,10]`

#### G2 — Step B (reverse) 성공

| | c1 | c2 | c3 | c4 |
|---|-----|-----|-----|-----|
| r1 | 16 | 2 | 3 | 13 |
| r2 | 5 | 11 | 10 | 8 |
| r3 | 9 | 7 | **0** | 12 |
| r4 | 4 | 14 | 15 | **0** |

- 1-index: first=(3,3), second=(4,4); missing {1,6}; Step A invalid, Step B valid
- **기대:** `[3,3,6,4,4,1]`

#### G3 — Unsolvable

| | c1 | c2 | c3 | c4 |
|---|-----|-----|-----|-----|
| r1 | 1 | 2 | 3 | **0** |
| r2 | 5 | 6 | **0** | 8 |
| r3 | 9 | 10 | 11 | 12 |
| r4 | 13 | 14 | 15 | 16 |

- missing {4,7}; **기대:** E006

**Gherkin MVP:** solve 성공 G2(SC-DOM-SOL-001)만 Gherkin 확정; G1은 Test Plan NS-01·AC-FR05-01로 커ver (Report/05 §8 backlog).

---

## 17. Architecture Overview (High-Level)

### 17.1 Layer Responsibilities

| Layer | 책임 | Must Not |
|-------|------|----------|
| **Boundary** | 입력 검증(E001~E005), 0-index→1-index 변환, Success/Failure schema, Domain 예외 매핑 | Domain 알고리즘 직접 구현 |
| **Control** | Domain Service 오케스트레이션 (locate → find → solve), `execute` 진입점 | 입출력 검증, UI 문자열 하드코딩 |
| **Entity (Domain)** | Grid, VO, Services, I1~I11, 순수 로직 | Boundary/Control import |

### 17.2 Dependency Direction

```
Caller (0-index matrix)
  ↓
[Boundary]  ← Track A
  ↓ Grid (1-index)
[Control: SolvePartialMagicSquare]
  ↓
[Domain Services]  ← Track B
  ↓ SolutionResult
[Boundary] → { type: "OK", data: int[6] }
```

| 허용 | 금지 |
|------|------|
| boundary → control | entity → boundary |
| boundary → entity (VO 변환) | entity → control |
| control → entity | control → boundary |

---

## 18. Component Candidates

| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|-----------|----------------|-------|-------|--------|------------|--------------|
| **InputValidator** | E001~E005 | Boundary | `int[][]` | pass / Error | FR-01 | U-IN-* |
| **UIBoundary** | orchestrate, schema map | Boundary | `int[][]` | Success / Error | FR-01, FR-05 | U-OUT-*, U-FLOW-* |
| **ErrorMapper** | Domain → E006/E007 | Boundary | Domain exception | Error schema | FR-05 | U-OUT-03 |
| **SolvePartialMagicSquare** | UC-D05 | Control | `Grid` | `SolutionResult` | FR-05 | U-FLOW-01, IT-01 |
| **EmptyCellLocator** | row-major 빈칸 2개 | Domain | `Grid` | `EmptyCellPair` | FR-02 | D-LOC-* |
| **MissingNumberFinder** | 누락 2개·정렬 | Domain | `Grid` | `MissingNumberPair` | FR-03 | D-MIS-* |
| **MagicSquareValidator** | I1~I5 | Domain | complete `Grid` | `boolean` | FR-04 | D-VAL-* |
| **TwoCellSolver** | Step A/B | Domain | `Grid` | `SolutionResult` / exceptions | FR-05 | D-SOL-* |
| **Grid** | 격자·copy | Domain | — | — | FR-02~05 | — |
| **MagicConstant** | M=34 SSOT | Domain | — | `34` | FR-04 | D-VAL-01 |

---

## 19. Risks & Ambiguities

| Risk | Impact | Mitigation |
|------|--------|------------|
| 0-index vs 1-index 혼동 | 잘못된 좌표 | BR-19, §12.1 명시 |
| row-major 정의 누락 | first/second 뒤바뀜 | BR-06, BR-06a, G1/G2 fixture |
| G1 vs G2 혼동 | Step A/B 테스트 오적용 | §16.4 라벨, NS-01=G1, NS-02=G2 |
| 입력 Grid mutation | Caller 데이터 오염 | BR-18, NFR-05 |
| E007 vs E006 혼동 | 잘못된 error code | §13.2 매핑표 |
| 34 하드코딩 | SSOT 붕괴 | `MagicConstant`, NFR-08 |
| Boundary/Domain 혼합 | ECB 위반 | BR-05, Dual-Track Mock 규칙 |

---

## 20. Engineering Principles

| 영역 | 원칙 |
|------|------|
| Style | Python 3.10+, PEP8, Black 88, type hints, Google docstring |
| Test | pytest, AAA, `test_` prefix |
| Coverage | Domain ≥95%, Boundary ≥85%, global ≥80% |
| Architecture | ECB dependency direction |
| TDD | RED → GREEN(최소) → REFACTOR(계약 유지) |
| Forbidden | print(), bare except, RED 없이 구현, test weakening, magic literal |
| Dual-Track | UI Mock 허용; Logic Domain Mock 금지 |

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case | Component |
|---------------------|---------------|------------|---------------------|-----------|-----------|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-02, AC-FR01-03 | U-IN-02,03, IT-E01 | InputValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-FR01-04 | U-IN-04,05, IT-E02 | InputValidator |
| 값 범위 | BR-03 | FR-01 | AC-FR01-05 | U-IN-06,07 | InputValidator |
| 중복 금지 | BR-04 | FR-01 | AC-FR01-06 | U-IN-08, IT-E05 | InputValidator |
| Domain 0회 | BR-05 | FR-01 | AC-FR01-01~06, AC-FR01-08 | U-FLOW-02 | UIBoundary |
| null 입력 | — | FR-01 | AC-FR01-01 | U-IN-01 | InputValidator |
| 0-index 입력 | BR-19 | FR-01 | §12.1 | — | UIBoundary |
| row-major 첫 빈칸 | BR-06 | FR-02 | AC-FR02-01~04 | D-LOC-01,04,05 | EmptyCellLocator |
| second 빈칸 | BR-06a | FR-02 | AC-FR02-01~04 | D-LOC-01 | EmptyCellLocator |
| 누락 2개 | BR-07 | FR-03 | AC-FR03-01~03 | D-MIS-01,03 | MissingNumberFinder |
| 누락 오름차순 | BR-08 | FR-03 | AC-FR03-01~03 | D-MIS-01 | MissingNumberFinder |
| 0 제외 | BR-13 | FR-03,04 | AC-FR04-06 | D-VAL-06 | MissingNumberFinder |
| M=34 | BR-11 | FR-04 | AC-FR04-01 | D-VAL-01 | MagicConstant |
| 행/열/대각 | BR-09~11 | FR-04 | AC-FR04-01~06 | D-VAL-01~06 | MagicSquareValidator |
| Step A (G1) | BR-14 | FR-05 | AC-FR05-01 | D-SOL-01, IT-01 | TwoCellSolver |
| Step B (G2) | BR-15 | FR-05 | AC-FR05-02 | D-SOL-02, IT-03 | TwoCellSolver |
| Unsolvable (G3) | §13.2 | FR-05 | AC-FR05-03 | D-SOL-03, IT-E03 | TwoCellSolver |
| int[6] | BR-16 | FR-05 | AC-FR05-04 | U-OUT-01 | UIBoundary |
| 1-index 출력 | BR-12 | FR-05 | AC-FR05-05 | U-OUT-02 | UIBoundary |
| Success schema | BR-20 | FR-05 | AC-FR05-07 | U-OUT-01 | UIBoundary |
| E007 mapping | §13.2 | FR-02,03,05 | AC-FR02-05,06, AC-FR03-04, AC-FR05-08 | D-LOC-02, D-MIS-02 | ErrorMapper |
| 결정성 | BR-17 | — | NFR-04 | U-OUT-01 | System |
| 입력 불변 | BR-18 | — | NFR-05 | copy assert | Grid, TwoCellSolver |

---

## 22. Open Questions / Decision Needed

| ID | 항목 | 상태 |
|----|------|------|
| DN-01 | Report/01 I1~I12 vs Report/02 I1~I11 | PRD는 Report/02 SSOT |
| DN-02 | 호출 UI (CLI vs API) | Contract만 In-Scope |
| DN-03 | Data Layer Phase 2 | MVP Out-of-Scope |
| DN-04 | Gherkin 9건 backlog | v1.1 |
| DN-05 | `.mdc` rules 미존재 | `.cursorrules` SSOT |

---

## 23. Appendix

### 23.1 참고 문서

| 문서 | 경로 |
|------|------|
| Problem Definition | Report/01.MagicSquare_ProblemDefinition_Report.md |
| Dual-Track Design | Report/02.MagicSquare_DualTrack_TDD_Design_Report.md |
| Cursor Rules | Report/03, `.cursorrules` |
| User Journey | Report/05.MagicSquare_UserJourney_To_Scenario_Report.md |
| PRD Session Report | Report/06.MagicSquare_PRD_And_Review_Report.md |

### 23.2 AC → Test ID 전체 매핑

| AC ID | Test ID |
|-------|---------|
| AC-FR01-01 | U-IN-01 |
| AC-FR01-02 | U-IN-02, IT-E01 |
| AC-FR01-03 | U-IN-03 |
| AC-FR01-04 | U-IN-04, U-IN-05, IT-E02 |
| AC-FR01-05 | U-IN-06, U-IN-07 |
| AC-FR01-06 | U-IN-08, IT-E05 |
| AC-FR01-07 | U-FLOW-01 |
| AC-FR01-08 | U-FLOW-02 |
| AC-FR02-01 | D-LOC-01 |
| AC-FR02-02 | D-LOC-01 (G2) |
| AC-FR02-03~04 | D-LOC-04, D-LOC-05 |
| AC-FR02-05~06 | D-LOC-02, D-LOC-03 |
| AC-FR03-01 | D-MIS-01 |
| AC-FR03-02 | D-MIS-01 (G2) |
| AC-FR03-03 | D-MIS-03 |
| AC-FR03-04 | D-MIS-02 |
| AC-FR04-01~06 | D-VAL-01~06 |
| AC-FR05-01 | D-SOL-01, IT-01 |
| AC-FR05-02 | D-SOL-02, IT-03 |
| AC-FR05-03 | D-SOL-03, U-OUT-03, IT-E03 |
| AC-FR05-04~07 | U-OUT-01, U-OUT-02 |
| AC-FR05-08 | U-OUT-03 (E007 pattern) |

### 23.3 UX Rules (Report/02)

| ID | 규칙 |
|----|------|
| UX-01 | Success `data`는 6원소 배열; wrapper는 schema 계층만 |
| UX-02 | Error message 완전 일치 |
| UX-03 | 동일 입력 → 동일 출력 |
| UX-04 | 좌표 1-index; 0-index 외부 노출 금지 |
| UX-05 | Success/Failure schema 혼재 금지 |

### 23.4 Gherkin MVP (확정 4건)

- SC-DOM-SOL-001: G2 Step B → `[3,3,6,4,4,1]`
- SC-BND-VAL-001: empty count → E002
- SC-BND-VAL-002: duplicate → E005
- SC-BND-VAL-003: value 17 → E004

---

*본 PRD는 MagicSquare_1004 구현 전 SSOT이다. RED→GREEN→REFACTOR로 §10 FR 및 §21 Traceability Matrix를 충족해야 한다.*
