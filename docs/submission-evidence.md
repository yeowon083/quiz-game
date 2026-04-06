# 제출 증빙 문서

## 1. 저장소 정보
- GitHub URL: `https://github.com/yeowon083/quiz-game`
- 기본 브랜치: `main`

## 2. 실행 및 기능 증빙
아래 스크린샷으로 실제 동작을 확인할 수 있습니다.

- 메뉴 화면: `docs/screenshots/menu.png`
- 퀴즈 추가: `docs/screenshots/add-quiz.png`
- 퀴즈 목록: `docs/screenshots/quiz-list.png`
- 퀴즈 플레이: `docs/screenshots/play-quiz.png`
- 결과/점수: `docs/screenshots/result-score.png`
- 최고 점수 확인: `docs/screenshots/best-score.png`
- 개발환경: `docs/screenshots/env-python-git.png`
- Git 로그 그래프: `docs/screenshots/git-log-graph.png`

## 3. 요구사항별 구현 근거
### 3-1. 메뉴 및 기능 동작
- 메뉴 출력/선택: `QuizGame.show_menu`, `QuizGame.run`
- 퀴즈 풀기: `QuizGame.play_quiz`
- 퀴즈 추가: `QuizGame.add_quiz`
- 퀴즈 목록: `QuizGame.show_quiz_list`
- 점수 확인: `QuizGame.show_best_score`

### 3-2. 입력 예외 처리
- 숫자 입력 검증: `QuizGame.input_number`
  - 앞뒤 공백 제거
  - 빈 입력 처리
  - 숫자 변환 실패 처리
  - 허용 범위 벗어남 처리
- 텍스트 입력 검증: `QuizGame.input_text`
  - 빈 입력 처리
- 안전 종료 처리:
  - `KeyboardInterrupt`, `EOFError` 발생 시 `InputTerminated`로 처리 후 저장 종료

### 3-3. 데이터 영속성
- 상태 파일: 프로젝트 루트 `state.json`
- 저장: `QuizGame.save_state`
- 불러오기: `QuizGame.load_state`
- 파일 손상/누락 대응:
  - 파일 없음: 기본 퀴즈로 초기화
  - JSON 손상/형식 오류: 기본 퀴즈로 복구
- 최고 점수 검증:
  - `QuizGame._sanitize_best_score_fields`

### 3-4. 기본 퀴즈 개수
- 기본 퀴즈 데이터: `QuizGame.get_default_quizzes`
- 현재 기본 문제 수: 6개 (요구사항 5개 이상 충족)

## 4. Git 요구사항 증빙
### 4-1. 커밋 수
- 확인 명령: `git rev-list --count HEAD`
- 현재 커밋 수: 10개 이상

### 4-2. 브랜치/병합
- 작업 브랜치 생성 및 병합 기록 존재
- 확인 명령: `git log --oneline --graph --decorate --all`

### 4-3. clone/pull 실습
- 실습 흐름: README 7번 항목
- 실습 반영 문구: README 하단 `clone 실습 반영: 2026-04-06`

## 5. 코드 구조/설계 설명
1. `Quiz`는 “문제 단위 데이터 + 판정 로직”만 담당한다.
2. `QuizGame`은 “입력/출력/진행/저장”의 오케스트레이션을 담당한다.
3. 입력 검증을 공통 함수(`input_number`, `input_text`)로 분리해 중복을 줄였다.
4. 파일 저장/불러오기를 메서드로 분리해 게임 로직과 영속 로직의 결합을 낮췄다.
5. 종료 지점(정상 종료/비정상 종료)에서 저장을 호출해 데이터 유실 가능성을 줄였다.

## 6. 핵심 기술 적용 이유
1. 클래스 사용 이유: 데이터 모델(`Quiz`)과 프로그램 흐름(`QuizGame`)의 책임 분리를 위해.
2. JSON 사용 이유: 사람이 읽기 쉽고, 리스트/딕셔너리 구조를 그대로 저장할 수 있어서.
3. 예외 처리 이유: 사용자 입력 오류, 파일 손상, 강제 종료 상황에서도 프로그램 지속성을 위해.
4. 브랜치 사용 이유: 메인 안정성을 유지한 상태로 기능/문서 작업을 분리하기 위해.
5. 커밋 분리 이유: 기능 단위 변경 이력을 명확히 남겨 추적성과 리뷰 가능성을 높이기 위해.

## 7. 심층 질문 대응
1. 데이터 저장 방식의 한계:
   - JSON 단일 파일 구조라 동시 수정/대용량 확장에 약함.
2. 파일 손상 대응:
   - `load_state`에서 예외를 잡고 기본 퀴즈로 복구 후 재저장해 실행 가능 상태를 유지함.
3. 요구사항 변경 시 수정 범위:
   - 문제 삭제 기능: `QuizGame`에 삭제 메서드 추가 + 메뉴 연결.
   - 점수 히스토리 확장: `save_state/load_state` 스키마 확장 + 점수 출력 메서드 갱신.
