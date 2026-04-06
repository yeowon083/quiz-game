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
