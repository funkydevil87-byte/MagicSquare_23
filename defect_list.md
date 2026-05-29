# 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| 문서 버전 | 2.0 |
| 기준일 | 2026-05-29 |
| QA 실행 명령 | `python -m pytest -q` |
| 최종 실행 결과 | **65 passed**, **0 failed** (GREEN) |
| 커버리지 | `pytest --cov=src/magicsquare` — core **≥85%** (`screen/app.py` 제외) |

---

## 요약

Track A RED 시점 결함(DEF-001~011)은 **FR-01 전체 GREEN**, Track B GREEN, Boundary E2E, `test_u_*` 11건 GREEN으로 **해소**되었다.  
`InputValidator`는 PRD §13.1 Error Code 6종을 반환하며, 검증 실패 시 Control/Domain은 호출되지 않는다.

---

## 결함 상태 (회귀)

| ID | 상태 | 비고 |
|----|------|------|
| DEF-001~009 | **CLOSED** | `MagicSquareBoundary`, `InputValidator`, `FailureResult` 구현 |
| DEF-010 | **CLOSED** | `NULL_INPUT` 등 PRD §13.1 코드 도입 (`schemas.py` SSOT) |
| DEF-011 | **CLOSED** | `pyproject.toml` `[project.optional-dependencies] dev` |

---

## 회귀 확인 체크리스트

- [x] `python -m pytest -q` → **65 passed**
- [x] `grid=None` 시 `execute()` / `resolve()` **0회**
- [x] FR-01 빈칸·범위·중복 → `INVALID_EMPTY_COUNT` / `OUT_OF_RANGE` / `DUPLICATE_VALUE`
- [x] Boundary E2E — TD-01, G1, G3(UNSOLVABLE)
- [x] D-T22 — both-valid 시 Attempt 1 우선 (mocked validator)
- [x] README §7·§10·defect_list 동기화

---

## 문서 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | v1.0 — RED 24 ERROR |
| 2026-05-29 | v2.0 — FR-01·E2E·전체 GREEN 회귀 반영 |
