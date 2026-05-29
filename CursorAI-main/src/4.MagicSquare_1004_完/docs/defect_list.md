# Magic Square 4×4 — 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **문서 ID** | DEF-MS-001 |
| **기준 AC** | AC-FR-01-01 |
| **관련 테스트** | `tests/boundary/test_ac_fr_01_01_*.py` |
| **관련 계획** | `docs/test_plan.md`, README §RED 단계 To-Do |
| **상태** | OPEN — RED 단계 (Boundary production 미구현) |
| **최종 갱신** | 2026-05-24 |

---

## 요약

| Severity | 건수 | 상태 |
|----------|------|------|
| Critical | 4 | OPEN |
| Major | 0 | — |
| Minor | 0 | — |
| Info | 1 | OPEN |

**재현 명령:**

```bash
cd /c/DEV/MagicSquare_1004
source .venv/Scripts/activate   # Windows Git Bash
python -m pytest tests/boundary/ -v
```

**현재 결과:** `2 errors during collection`, exit code **2**

---

## 결함 목록

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-001 | Critical | AC-FR-01-01 | `python -m pytest tests/boundary/ -v` 실행 | 13건 테스트 수집·실행; `grid=None` → `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `ModuleNotFoundError: No module named 'boundary'` (collection ERROR, 0건 실행) | `src/boundary/` ECB Boundary 패키지 **미생성** | `src/boundary/__init__.py` 및 하위 모듈 스켈레ton 생성 |
| DEF-002 | Critical | AC-FR-01-01 | `tests/boundary/test_ac_fr_01_01_input_validation.py:11` import | `from boundary.input_validator import InputValidator` 성공 | `ModuleNotFoundError: No module named 'boundary'` | `boundary.input_validator` 모듈 **미존재** | `InputValidator.validate()` 구현 — `None`/size 위반 시 `FailureResponse` 반환 |
| DEF-003 | Critical | AC-FR-01-01 | `tests/boundary/test_ac_fr_01_01_ui_boundary_flow.py:12~14` import | `FailureResponse`, `UIBoundary`, `SolvePartialMagicSquare` import 성공 | `ModuleNotFoundError: No module named 'boundary'` (연쇄: `control` 도 미존재) | `boundary.schemas`, `boundary.ui_boundary`, `control.solve_partial_magic_square` **미존재** | pydantic `FailureResponse`/`ErrorDetail`, `UIBoundary.solve()` early return, Control `resolve()` stub 생성 |
| DEF-004 | Critical | AC-FR-01-01 | `UIBoundary.solve(grid=None)` + mock `resolve()` (U-FLOW-02) | `resolve()` **0회** 호출; `type="ERROR"`, `code="INVALID_SIZE"` | 테스트 미도달 (import 단계 중단) | validate 실패 시 Domain 진입 차단 로직 **미구현** | `UIBoundary.solve()`에서 `InputValidator` 실패 시 즉시 반환; `resolve()` 호출 금지 |
| DEF-005 | Info | — | `python -m pytest --cov=src --cov-report=html` (Boundary ERROR 상태) | `htmlcov/index.html` 생성 | `htmlcov/` 폴더 미생성 | pytest collection ERROR(exit 2) → pytest-cov HTML 리포트 **미생성** | DEF-001~004 해소(GREEN) 후 동일 명령 재실행 |

---

## AC-FR-01-01 범위 외 (본 목록 미포함)

다음은 **의도적으로 결함으로 등록하지 않음** (후속 AC/FR 범위):

| 항목 | 사유 |
|------|------|
| AC-FR-01-02~05 (빈칸·값·중복) | RED/GREEN 범위 외 — 선제 구현 금지 |
| FR-02~05 Domain 로직 | Track B — Boundary 결함과 별도 |
| `AttributeError: 'NoneType'` (None 분기 누락) | **잠재 결함** — DEF-001~002 해소 후에도 GREEN 실패 시 DEF-006으로 승격 |

---

## 잠재 결함 (GREEN 진입 후 모니터링)

| ID | Severity | AC ID | 조건 | 기대값 | 잠재 실제값 | 근본 원인 (예상) | 수정 요약 (예상) |
|----|----------|-------|------|--------|-------------|------------------|------------------|
| DEF-006 | Critical | AC-FR-01-01 | DEF-001~002 수정 후 `validate(None)` 실행 | `FailureResponse`, `code="INVALID_SIZE"` | `AttributeError: 'NoneType' object has no attribute 'error'` | `grid is None` 분기 누락 | `if matrix is None: return _failure()` 추가 |

> DEF-006은 현재 로그에서 **미관측**. import ERROR 해소 후 assertion 실패 시 등록·승격.

---

## 수정 우선순위 (GREEN 최소 경로)

```
1. DEF-001  src/boundary/ 패키지 생성
2. DEF-002  InputValidator — None + size 분기
3. DEF-003  schemas + UIBoundary + Control stub
4. DEF-004  UIBoundary early return (resolve 0회)
5. DEF-005  GREEN 후 커버리지 HTML 재측정
```

---

## GREEN 확인 절차 (결함 해소 검증)

| # | 명령 | 기대 |
|---|------|------|
| 1 | `python -m pytest tests/boundary/ -v` | **13 passed**, exit 0 |
| 2 | `python -m pytest tests/entity/ -v` | **10 passed** (회귀 없음) |
| 3 | `python -m pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing` | Boundary 커버리지 측정 가능 |
| 4 | DEF-001~004 상태 | **CLOSED** |
| 5 | README 결함 체크리스트 2번째 항목 | 체크 |

---

## 변경 이력

| 날짜 | 변경 | 작성 |
|------|------|------|
| 2026-05-24 | 초版 — RED 단계 collection ERROR 4건 + Info 1건 등록 | QA Lead |

---

*본 문서는 RED 단계에서 발견된 결함을 추적합니다. GREEN 통과 후 DEF-001~004를 CLOSED로 갱신하고, 회귀 테스트 결과를 기록하세요.*
