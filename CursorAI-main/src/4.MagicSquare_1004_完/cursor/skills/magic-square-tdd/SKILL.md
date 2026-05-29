---
name: magic-square-tdd
description: >-
  MagicSquare_1004 4×4 부분 마방진 프로젝트의 Dual-Track TDD·ECB 아키텍처 개발 가이드.
  RED/GREEN/REFACTOR 사이클, Logic Track vs UI Contract Track, 테스트 ID(D-*, U-*),
  Golden Master, 입출력 계약(E001~E007)을 다룬다.
  src/, tests/, Report/, 마방진, ECB, TDD, pytest, 리팩터링, Golden Master 작업 시 사용.
---

# MagicSquare TDD 개발 스킬

## 응답 시작 선언 (필수)

코드·테스트를 제안하기 전에 한 줄로 선언한다:

```
Phase: red|green|refactor | Layer: entity|control|boundary | Track: logic|ui
```

## SSOT 문서

| 문서 | 용도 |
|------|------|
| `.cursorrules` | 코딩·TDD·ECB 규칙 (최우선) |
| `Report/01.MagicSquare_ProblemDefinition_Report.md` | 문제 정의·계약 |
| `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md` | Dual-Track 설계·불변식 I1~I11 |
| `docs/PRD_MagicSquare.md` | PRD·성공 기준 |
| `tests/golden_master_expected.txt` | Golden Master 기대 출력 |

상세 테스트 ID·에러 코드·컴포넌트 매핑은 [reference.md](reference.md) 참조.

---

## TDD 워크플로우

### RED — 실패 테스트 먼저

```
Task Progress:
- [ ] Report/tests에서 대응 테스트 ID(D-*, U-*) 확인
- [ ] 대상 레이어·트랙 결정
- [ ] AAA 패턴으로 실패 테스트 작성
- [ ] pytest 실행 → RED(실패) 확인
- [ ] production 코드 작성 금지
```

- Logic Track: `tests/entity/` 또는 `tests/control/` — **Domain Mock 금지**
- UI Track: `tests/boundary/` — Control/Entity Mock **허용**
- 실패 원인은 "미구현" 또는 "기대 동작 미충족"이어야 함

### GREEN — 최소 구현

- 현재 RED 테스트를 통과시키는 **최소 코드만** 작성
- `pytest`로 대상 테스트 GREEN 확인
- 리팩터링·추가 기능·불필요한 추상화 **금지**

### REFACTOR — 구조 개선

- **전체 pytest GREEN** 상태에서만 진행
- 동작·공개 API·E001~E007 계약 **불변**
- ECB 레이어 경계·SRP 강화 방향
- 커버리지 **80% 이상** 유지

---

## ECB 아키텍처

```
boundary/  →  control/  →  entity/
(UI, 검증)     (유스케이스)   (도메인)
```

| 레이어 | 경로 | 책임 | 금지 |
|--------|------|------|------|
| **entity** | `src/entity/` | Grid, VO, Domain Service, I1~I11 | boundary/control import, E001~E005 처리 |
| **control** | `src/control/` | SolvePartialMagicSquare 오케스트레이션 | 입출력 검증, UI 문자열 |
| **boundary** | `src/boundary/` | InputValidator, ErrorMapper, UIBoundary | Domain 알고리즘 직접 구현 |

**허용 import**: `boundary→control`, `boundary→entity(VO 변환)`, `control→entity`
**금지 import**: `entity→*`, `control→boundary`

---

## Dual-Track 규칙

| Track | 테스트 경로 | Mock | 검증 대상 |
|-------|-------------|------|-----------|
| Logic | `tests/entity/`, `tests/control/` | Domain Mock **금지** | 순수 도메인·유스케이스 |
| UI Contract | `tests/boundary/` | Control/Entity Mock **허용** | E001~E007, int[6] 직렬화, Domain 격리 |

테스트 파일명 패턴:
- Logic: `test_d_val_01_*`, `test_d_loc_01_*`, `test_d_mis_01_*`, `test_d_sol_01_*`
- UI: `test_u_in_*`, `test_u_out_*`, `test_u_flow_*`, `test_ac_fr_*`

---

## 도메인 핵심 계약 (요약)

**입력**: 4×4 `int[][]`, 빈칸 `0` 정확히 2개, 값 `0` 또는 `1~16`, 0 제외 중복 금지

**출력**: `int[6] = [r1,c1,n1,r2,c2,n2]`, 좌표 **1-index**

**해결 전략** (TwoCellSolver):
1. Step A: `(smaller→firstEmpty, larger→secondEmpty)` → 성공 시 `(n1,n2)=(smaller,larger)`
2. Step B: `(larger→firstEmpty, smaller→secondEmpty)` → 성공 시 `(n1,n2)=(larger,smaller)`
3. 둘 다 실패 → `UnsolvableDomainError` → Boundary E006

**상수 SSOT**: `src/entity/value_objects/magic_constant.py`의 `MagicConstant` (M=34). 리터럴 34/16 산재 금지.

---

## pytest 명령

```bash
pytest                          # 전체
pytest tests/entity             # Logic Track
pytest tests/boundary           # UI Track
pytest tests/control            # Control 유스케이스
pytest tests/test_gm_01_magic_square_golden_master.py  # Golden Master
pytest --cov=src --cov-report=term-missing  # 커버리지
```

---

## Golden Master

- 시나리오: `tests/golden_master_scenarios.py`
- 기대값: `tests/golden_master_expected.txt`
- 재생성: `python scripts/generate_golden_master.py`
- GREEN/REFACTOR 후 Golden Master 회귀 확인 권장

---

## 금지 패턴

| 패턴 | 대안 |
|------|------|
| RED 없이 `src/` production 코드 | 테스트 먼저 → RED 확인 |
| assert 완화·skip·xfail·Mock 남용 | production 코드 수정 |
| `print()` 디버깅 | pytest assertion, `logging` + caplog |
| 하드코oded 34/16 | `MagicConstant` SSOT |
| `except:` / bare `except Exception` | 구체적 Domain 예외 → Error schema |
| entity→boundary/control import | 의존성 방향 준수 |

---

## 코드 스타일

- Python 3.10+, PEP8, Black (88 cols)
- 모든 public 함수: **type hints + Google docstring**
- import: 표준 → 서드파티 → 로컬 (그룹 간 빈 줄)
- 테스트: AAA 패턴, `test_` 접두사

---

## 응답 형식

작업 완료 시 아래 순서로 보고:

1. **Phase & Layer & Track**
2. **대상 테스트 ID** (D-* / U-*)
3. **코드 변경** (파일 경로)
4. **ECB 준수 확인**
5. **pytest 결과** (명령, PASS/FAIL)
6. **변경 파일 목록**
7. **⚠ TDD 위반 경고** (해당 시)

---

## Agent 위임

레이어별 전문 Agent는 `.cursor/agents/`에 정의됨:

| Agent | 담당 |
|-------|------|
| `backend-developer` | entity, control (Logic Track) |
| `frontend-developer` | boundary UI (PyQt6) |
| `quality-assurance-engineer` | 커버리지·Golden Master·회귀 |

레이어에 맞는 Agent 프롬프트를 참조하되, 본 스킬의 TDD·ECB 규칙이 우선한다.
