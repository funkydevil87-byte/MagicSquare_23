# 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.0 |
| 기준일 | 2026-05-29 |
| QA 실행 명령 | `python -m pytest tests/boundary/ -v` |
| 최종 실행 결과 | **24 ERROR**, **5 PASSED**, **0 FAILED** (RED 단계) |
| 관련 AC | AC-FR-01-01 (계약 위반 시 Domain 미호출) |
| 관련 테스트 | `tests/boundary/test_ac_fr_01_01_contract_violation.py` |

---

## 요약

Track A RED 테스트 29건 중 **24건**이 `boundary` fixture 설정 단계에서 `ModuleNotFoundError`로 중단된다.  
근본 원인은 **Boundary/Control 구현 모듈 부재**이며, 동일 원인으로 정상 실패 반환·경계값·격리·메시지 검증이 일괄 미충족 상태다.

---

## 결함 테이블

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-001 | Critical | AC-FR-01-01 | `python -m pytest tests/boundary/ -v` 실행 | Boundary 테스트 24건 실행·검증 가능 | `ModuleNotFoundError: No module named 'magicsquare.boundary.magic_square_boundary'` (fixture setup ERROR) | `src/magicsquare/boundary/magic_square_boundary.py` 미구현 | `MagicSquareBoundary` 모듈·클래스 생성 및 `solve()` 스켈레톤 추가 |
| DEF-002 | Critical | AC-FR-01-01 | `grid=None` 입력 후 `boundary.solve(grid)` 호출 (`TestNormalFailureReturn`) | `FailureResult(code="INVALID_SIZE", message="Grid must be 4x4.")` 반환 | DEF-001로 인해 `boundary` fixture 로드 실패 (테스트 미실행) | `MagicSquareBoundary.solve()` 미구현 | `grid is None` 분기에서 `FailureResult` 반환 |
| DEF-003 | Critical | AC-FR-01-01 | `grid=[]` 입력 후 `boundary.solve(grid)` 호출 (`TestBoundaryValues`) | `FailureResult` + `code="INVALID_SIZE"` | DEF-001로 인해 테스트 미실행 | 행 개수 검증 로직 부재 | `len(grid) != 4` 시 `INVALID_SIZE` 실패 반환 |
| DEF-004 | Critical | AC-FR-01-01 | `grid=[[]]*4` 입력 후 `boundary.solve(grid)` 호출 | `FailureResult` + `message="Grid must be 4x4."` | DEF-001로 인해 테스트 미실행 | 열 개수/jagged 검증 로직 부재 | 각 행 `len(row) != 4` 시 `INVALID_SIZE` 실패 반환 |
| DEF-005 | Critical | AC-FR-01-01 | `grid=3×4` (`GRID_3X4`) 입력 후 `boundary.solve(grid)` 호출 | `FailureResult` 반환 | DEF-001로 인해 테스트 미실행 | 4×4 크기 불변식(BR-01) 미적용 | 행·열 크기 검증 후 `INVALID_SIZE` 반환 |
| DEF-006 | Critical | AC-FR-01-01 | `grid=None` + `@patch(RESOLVE_PATCH)` 후 `boundary.solve(grid)` (`TestIsolationVerification`) | `MagicSquareSolver.resolve` **0회** 호출 | DEF-001로 인해 테스트 미실행; patch 대상 모듈도 부재 | `magicsquare.control.magic_square_solver` 미구현 | Control/Domain `resolve()` 생성 후 Boundary에서 검증 실패 시 호출 금지 |
| DEF-007 | High | AC-FR-01-01 | `grid in {None, [], [[]]*4, 3×4}` 각각에 대해 `failure.message` 비교 (`TestMessageIdentity`) | `message == "Grid must be 4x4."` (문자 단위 `==`) | DEF-001로 인해 테스트 미실행 | 실패 Message 상수·반환 경로 부재 | PRD §8.1 `INVALID_SIZE` 문구를 상수로 고정 후 반환 |
| DEF-008 | High | AC-FR-01-01 | `grid=None` 입력 후 반환 타입 확인 (`test_none_grid_failure_is_pydantic_model`) | `FailureResult` pydantic 모델 인스턴스 | DEF-001로 인해 테스트 미실행 | Boundary 실패 DTO 미정의 | `src/magicsquare/boundary/models.py`에 `FailureResult` 정의·반환 |
| DEF-009 | Medium | AC-FR-01-01 | `test_in_scope_failure_codes_only_invalid_size` 실행 | 4종 무효 grid 모두 `code="INVALID_SIZE"` | DEF-001로 인해 테스트 미실행 | 통합 실패 코드 매핑 부재 | 크기/null 계약 위반을 단일 `INVALID_SIZE`로 매핑 |
| DEF-010 | Medium | AC-FR-01-01 | PRD `docs/PRD_MagicSquare.md` §13.1 vs RED 테스트 계약 대조 | `grid=None` → `NULL_INPUT` / `입력이 null입니다` (AC-FR01-03) | 테스트는 `INVALID_SIZE` / `Grid must be 4x4.` 기대 | **요구사항·테스트 계약 불일치** (RED 스펙 vs PRD v1.1) | 제품 결정 후 PRD 또는 테스트 중 한쪽 계약으로 통일 |
| DEF-011 | Low | AC-FR-01-01 | 신규 환경에서 `pip install` 없이 `pytest tests/boundary/` 실행 | `pydantic` import 성공 | (과거) `ModuleNotFoundError: No module named 'pydantic'` 가능 | `pyproject.toml`에 테스트 의존성 미선언 | `[project.optional-dependencies] dev` 또는 `requirements-dev.txt`에 `pytest`, `pydantic`, `pytest-cov` 추가 |

---

## 영향 받는 테스트 (ERROR 24건)

| 테스트 클래스 | ERROR 수 | 대표 결함 ID |
|---------------|:--------:|--------------|
| `TestNormalFailureReturn` | 5 | DEF-001, DEF-002, DEF-008 |
| `TestBoundaryValues` | 5 | DEF-001, DEF-003~DEF-005 |
| `TestIsolationVerification` | 5 | DEF-001, DEF-006 |
| `TestMessageIdentity` | 8 | DEF-001, DEF-007 |
| `TestScopeLimitation` (통합) | 1 | DEF-001, DEF-009 |

### 통과 중인 테스트 (범위 제한 메타 검증, 5건)

- `test_module_source_excludes_null_input_error_code`
- `test_module_source_excludes_invalid_empty_count_cases`
- `test_module_source_excludes_out_of_range_value_cases`
- `test_module_source_excludes_duplicate_value_cases`
- `test_module_ast_excludes_fr_02_to_fr_05_domain_imports`

> 구현 부재와 무관하게 **테스트 스위트 범위**만 검증하므로 GREEN으로 표시됨. AC-FR-01-01 기능 검증 완료로 간주하지 않음.

---

## 수정 우선순위 (QA 권고)

1. **DEF-001** — `MagicSquareBoundary` 모듈 생성 (다수 ERROR 해소)
2. **DEF-006** — `MagicSquareSolver.resolve` 스텁 + Boundary 단락
3. **DEF-002~DEF-005, DEF-007~DEF-009** — null/크기 실패 반환 및 Message 고정
4. **DEF-010** — PRD vs RED 계약 정합성 결정
5. **DEF-011** — 개발 의존성 문서화

---

## 회귀 확인 체크리스트 (수정 후)

- [ ] `python -m pytest tests/boundary/ -v` → **29 passed**, 0 error
- [ ] `grid=None` 시 `resolve()` mock **0회** (`assert_not_called`)
- [ ] DEF-010 계약 통일 여부 PRD/README 반영
- [ ] README §7 결함 목록 — 회귀 테스트 통과 체크

---

## 문서 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | RED 실행 결과 기반 초판 작성 (24 ERROR) |
