# Python Basics Quiz Game

## 1. 프로젝트 개요
Python 기초 개념(변수, 자료형, 조건문, 반복문, 함수, 클래스)을 문제로 다루는 콘솔 퀴즈 게임입니다.  
사용자는 메뉴를 통해 퀴즈를 풀고, 새 문제를 추가하고, 문제 목록과 최고 점수를 확인할 수 있습니다.

## 2. 퀴즈 주제 선정 이유
퀴즈 주제를 **파이썬 기초**로 선정한 이유는 학습 초반에 반드시 익혀야 하는 핵심 문법을 반복 점검하기 좋기 때문입니다.  
직접 문제를 풀고 추가하는 과정에서 문법 이해와 기억을 동시에 강화할 수 있습니다.

## 3. 실행 방법
1. Python 3.10 이상이 설치되어 있는지 확인합니다.
2. 프로젝트 루트에서 아래 명령어를 실행합니다.

```bash
python3 main.py
```

## 4. 기능 목록
- `퀴즈 풀기`: 저장된 퀴즈를 순서대로 출제하고 정답/오답을 판정합니다.
- `퀴즈 추가`: 문제, 선택지 4개, 정답 번호를 입력해 새 퀴즈를 저장합니다.
- `퀴즈 목록`: 현재 저장된 모든 퀴즈의 문제 문장을 확인합니다.
- `점수 확인`: 최고 점수와 당시 정답 개수를 확인합니다.
- `종료`: 현재 상태를 저장하고 프로그램을 안전하게 종료합니다.
- `예외 처리`: 빈 입력, 숫자 변환 실패, 범위 밖 입력, `Ctrl+C`, `EOF`를 처리합니다.

## 5. 파일 구조
```text
quiz-game/
├── main.py        # Quiz, QuizGame 클래스 및 전체 실행 로직
├── state.json     # 퀴즈/점수 영속 데이터 파일(자동 생성/갱신)
├── README.md
└── .gitignore
```

## 6. 데이터 파일 설명
- 경로: 프로젝트 루트의 `state.json`
- 역할: 퀴즈 목록과 최고 점수 정보를 저장하여 재실행 시 복원
- 인코딩: UTF-8
- 주요 필드:
  - `quizzes`: 퀴즈 객체 배열
  - `best_score`: 최고 점수(점수 단위)
  - `best_correct`: 최고 점수 달성 시 정답 수
  - `best_total`: 최고 점수 달성 시 전체 문제 수

예시 스키마:

```json
{
    "quizzes": [
        {
            "question": "Python의 창시자는?",
            "choices": ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"],
            "answer": 1
        }
    ],
    "best_score": 80,
    "best_correct": 4,
    "best_total": 5
}
```

## 7. Git 실습 기록 가이드
아래 흐름으로 `clone`, `checkout`, `merge`, `pull`을 기록할 수 있습니다.

```bash
# 브랜치 생성/작업/병합
git checkout -b feature/play-options
git checkout main
git merge --no-ff feature/play-options

# 저장소 복제 실습
cd ..
git clone https://github.com/yeowon083/quiz-game.git quiz-game-clone
cd quiz-game-clone
# README 한 줄 수정 후
git add README.md
git commit -m "Docs: clone 저장소에서 README 한 줄 추가"
git push origin main

# 원래 로컬로 돌아와 pull
cd ../quiz-game
git pull origin main
```

- clone 실습 반영: 2026-04-06

## 8. 개발 환경
- Python 3.10 이상
- Git
- VSCode (권장)

## 9. 제출 체크리스트
- GitHub 저장소 URL 제출
- 개발 환경 설정 스크린샷 첨부 (Python 버전, Git 설정 등)
- 실행 결과 스크린샷 첨부 (퀴즈 추가/목록/플레이/점수 화면)
- `git log --oneline --graph` 결과 스크린샷 첨부

## 10. 제출 증빙 링크
- 저장소 URL: `https://github.com/yeowon083/quiz-game`
- 요구사항 충족 근거 문서: `docs/submission-evidence.md`
- 스크린샷 파일:
  - `docs/screenshots/env-python-git.png`
  - `docs/screenshots/menu.png`
  - `docs/screenshots/add-quiz.png`
  - `docs/screenshots/quiz-list.png`
  - `docs/screenshots/play-quiz.png`
  - `docs/screenshots/result-score.png`
  - `docs/screenshots/best-score.png`
  - `docs/screenshots/git-log-graph.png`

## 11. 코드 구조 및 설계 설명
### 11-1. 클래스 책임 분리
- `Quiz` 클래스는 문제 단위 데이터(`question`, `choices`, `answer`)와 정답 판정(`is_correct`)을 담당합니다.
- `QuizGame` 클래스는 메뉴 출력, 입력 검증, 게임 진행, 상태 저장/복구를 담당합니다.

### 11-2. 로직 분리 기준
- 입력 처리(검증): `input_number`, `input_text`
- 게임 진행: `show_menu`, `play_quiz`, `add_quiz`, `show_quiz_list`, `show_best_score`, `run`
- 데이터 저장/불러오기: `save_state`, `load_state`, `_sanitize_best_score_fields`

### 11-3. state.json 읽기/쓰기 흐름
1. 프로그램 시작 시 `run()`에서 `load_state()`를 호출해 상태를 복원합니다.
2. 퀴즈 추가/최고 점수 갱신/종료 시 `save_state()`를 호출해 상태를 저장합니다.
3. 비정상 입력 종료(`Ctrl+C`, `EOF`) 시에도 `main()`에서 저장 후 종료합니다.

### 11-4. 안전 종료 처리
- 입력 단계에서 `KeyboardInterrupt`, `EOFError`를 `InputTerminated`로 변환합니다.
- `main()`에서 `InputTerminated`를 처리하여 안내 메시지 출력 후 `save_state()`를 호출합니다.

### 11-5. 커밋 단위와 메시지 규칙
- 커밋은 기능 단위(`Feat`), 수정 단위(`Fix`), 구조 개선(`Refactor`), 문서화(`Docs`)로 분리했습니다.
- 커밋 메시지는 “무엇을 왜 바꿨는지”가 드러나도록 작성했습니다.

## 12. 핵심 기술 원리 적용 설명
### 12-1. 클래스 사용 이유
- 문제 모델과 게임 제어 흐름을 분리해 코드 변경 시 영향 범위를 줄이기 위해 클래스 구조를 사용했습니다.
- 함수만으로 구현하면 상태와 책임이 섞이기 쉬워 유지보수가 어려워집니다.

### 12-2. JSON 사용 이유
- Python의 리스트/딕셔너리 구조를 그대로 저장하기 쉽고, 사람이 읽고 검증하기 쉽습니다.
- 텍스트 기반이라 버전 관리(Git)에서 변경 추적이 용이합니다.

### 12-3. try/except 필요성
- 파일 없음(첫 실행), 파일 손상(JSON 파싱 실패), 권한/입출력 오류(OSError) 같은 실패 케이스가 실제로 발생할 수 있습니다.
- 예외 처리가 없으면 프로그램이 즉시 종료되므로, 예외 처리로 기본 데이터 복구/안전 종료를 보장했습니다.

### 12-4. 브랜치 분리/병합 이유
- 브랜치는 메인 안정성을 유지하면서 작업을 분리하기 위해 사용합니다.
- 병합(merge)은 분리된 작업을 메인 이력에 통합하는 과정이며, `git log --graph`로 추적 가능합니다.

## 13. 심층 인터뷰 대응
### 13-1. state.json 구조 설계 이유
- `quizzes`는 문제 목록, `best_score/best_correct/best_total`은 최고 기록을 저장합니다.
- 학습 목표(문제 저장 + 최고 점수 유지)에 필요한 최소 필드만 사용해 구조를 단순화했습니다.

### 13-2. 데이터 증가 시 한계
- JSON 단일 파일 구조는 데이터가 매우 커지거나 동시 수정이 많아질 때 비효율적입니다.
- 규모가 커지면 DB(예: SQLite)로 전환하는 것이 적합합니다.

### 13-3. 파싱 실패 시 대응
- `load_state()`에서 `json.JSONDecodeError`, `ValueError`, `TypeError`, `OSError`를 처리합니다.
- 실패 시 기본 퀴즈를 복구해 프로그램이 실행 불가 상태가 되지 않도록 했습니다.

### 13-4. 요구사항 변경 시 수정 지점
- 문제 삭제 기능 추가: `main.py`의 메뉴(`show_menu`/`run`)와 삭제 메서드 추가, `save_state()` 연동이 필요합니다.
- 점수 히스토리 추가: `state.json` 스키마 확장 + `save_state/load_state/show_best_score` 수정이 필요합니다.
