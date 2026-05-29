# Prompting

4×4 Magic Square 워크플로를 **대화형으로 재현**하기 위한 프롬프트 모음.

## 파일

| 파일 | 설명 | 산출 Report |
|------|------|-------------|
| [01.MagicSquare_InteractivePrompt_Transcript.md](./01.MagicSquare_InteractivePrompt_Transcript.md) | STEP 0~7 문제 정의, Export Prompt, 대화 원문 | [01](../Report/01.MagicSquare_ProblemDefinition_Report.md) |
| [02.MagicSquare_DualTrack_TDD_Prompt_Transcript.md](./02.MagicSquare_DualTrack_TDD_Prompt_Transcript.md) | Phase A~B Dual-Track TDD 설계, Export Prompt, 통합 Turn 인덱스 | [02](../Report/02.MagicSquare_DualTrack_TDD_Design_Report.md) |
| [03.MagicSquare_CursorRules_Prompt_Transcript.md](./03.MagicSquare_CursorRules_Prompt_Transcript.md) | Cursor Rules 설계·`.cursorrules`·ECB User Entity, Export Prompt | [03](../Report/03.MagicSquare_CursorRules_And_FirstEntity_Report.md) |

## 전체 워크플로

```
01 Transcript (STEP 1~6)
    → Report/01 문제 정의
    → (선택) 02 Phase A: TDD 설계 실행 프롬프트
02 Transcript Phase B (Dual-Track 설계)
    → Report/02 Dual-Track TDD 설계
    → 03 Transcript (Cursor Rules + 첫 Entity)
03 Transcript
    → Report/03 Cursor Rules + User Entity
    → (다음) Domain RED (D-VAL-01~) — 별도 Transcript 예정
```

## 빠른 시작

### 문제 정의 (01)

1. **「0. 역할 설정」** 전달
2. **STEP 1**부터 순서대로 진행
3. STEP 6 후 **Export — Report** → `Report/01` 확인

### Dual-Track TDD 설계 (02)

1. `Report/01` 완료 확인
2. **Phase B — STEP 1** User Prompt 전달 (또는 STEP 2-A~D 분할)
3. **Export — Report** → `Report/02` 확인

### Cursor Rules 및 첫 Entity (03)

1. `Report/02` 완료 확인
2. **STEP 1** Cursor Rule 설계 (파일 생성 금지)
3. **STEP 2~5** `.cursorrules` 작성·검토·완성
4. **STEP 6** (선택) ECB User Entity + pytest
5. **Export — Report** → `Report/03` 확인

## Export Prompt 모음

| 목적 | User Prompt |
|------|-------------|
| 문제 정의 보고서 | `지금까지 작업한 내용을 Report 폴더에 보고서로 내보내줘` |
| Dual-Track 설계 보고서 | `Report 폴더에 보고서를 작성해줘.` |
| Cursor Rules 보고서 | `Report 폴더에 보고서 생성해줘` |
| Transcript 저장 | `현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompting 폴더에 Export transcript 해줘` |

## 관련

- [../Report/01.MagicSquare_ProblemDefinition_Report.md](../Report/01.MagicSquare_ProblemDefinition_Report.md)
- [../Report/02.MagicSquare_DualTrack_TDD_Design_Report.md](../Report/02.MagicSquare_DualTrack_TDD_Design_Report.md)
- [../Report/03.MagicSquare_CursorRules_And_FirstEntity_Report.md](../Report/03.MagicSquare_CursorRules_And_FirstEntity_Report.md)
