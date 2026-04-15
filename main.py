# 나만의 퀴즈 게임

# JSON 파일로 데이터를 저장하고 불러오기 위해 사용
import json

# 파일 경로를 다루기 쉽게 해주는 pathlib의 Path 클래스 사용
from pathlib import Path

# 게임 상태(퀴즈 목록, 최고 점수)를 저장할 파일 경로
STATE_FILE = Path("state.json")


# 기본 퀴즈 데이터 하나를 표현하는 클래스
class Quiz:
    """개별 퀴즈의 문제, 선택지, 정답을 관리한다."""

    # Quiz 객체가 만들어질 때 문제, 선택지, 정답을 저장
    def __init__(self, question, choices, answer):
        self.question = question   # 문제 문장
        self.choices = choices     # 선택지 목록
        self.answer = answer       # 정답 번호

    # 퀴즈 한 문제를 화면에 출력하는 메서드
    def display(self, number):
        print("-" * 40)
        print(f"📝 [문제 {number}]")
        print(self.question)
        print()

        # 선택지를 1번부터 번호를 붙여 출력
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    # 사용자가 입력한 답이 정답인지 확인하는 메서드
    def is_correct(self, user_answer):
        return user_answer == self.answer

    # Quiz 객체를 JSON에 저장할 수 있는 딕셔너리 형태로 변환
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    # 딕셔너리 데이터를 바탕으로 Quiz 객체를 다시 만드는 클래스 메서드
    @classmethod
    def from_dict(cls, data):
        # 딕셔너리에서 각 값 꺼내기
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]

        # 문제 데이터 검증:
        # 문자열이어야 하고, 공백만 있는 문자열이면 안 됨
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")

        # 선택지는 리스트여야 하고, 반드시 4개여야 함
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개의 목록이어야 합니다.")

        # 각 선택지가 문자열인지, 비어 있지 않은지 검사
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")

        # 정답은 1~4 사이의 정수여야 함
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1부터 4 사이의 숫자여야 합니다.")

        # 검증이 끝난 데이터를 이용해 Quiz 객체 생성 후 반환
        return cls(
            question.strip(),
            [choice.strip() for choice in choices],
            answer,
        )


# 프로그램 처음 실행 시 사용할 기본 퀴즈 목록 생성 함수
def create_default_quizzes():
    return [
        Quiz(
            "Python에서 값을 저장하기 위해 이름을 붙인 공간을 무엇이라고 하나요?",
            ["함수", "변수", "반복문", "주석"],
            2,
        ),
        Quiz(
            "Python에서 여러 값을 순서대로 저장할 때 주로 사용하는 자료형은?",
            ["bool", "int", "list", "str"],
            3,
        ),
        Quiz(
            "조건에 따라 다른 코드를 실행할 때 사용하는 키워드는?",
            ["if", "for", "def", "class"],
            1,
        ),
        Quiz(
            "함수를 정의할 때 사용하는 Python 키워드는?",
            ["return", "import", "while", "def"],
            4,
        ),
        Quiz(
            "객체를 만들기 위한 설계도 역할을 하는 문법은?",
            ["클래스", "딕셔너리", "문자열", "연산자"],
            1,
        ),
    ]


# 퀴즈 게임 전체 흐름을 관리하는 클래스
class QuizGame:
    """퀴즈 목록과 점수를 포함한 게임 흐름을 관리한다."""

    # QuizGame 객체가 만들어질 때 실행되는 초기화 메서드
    def __init__(self):
        # 기본 퀴즈 목록 불러오기
        self.quizzes = create_default_quizzes()

        # 최고 점수 관련 데이터 초기값 설정
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0

        # 저장된 파일이 있으면 불러오기
        self.load()

    # 메인 메뉴를 화면에 출력하는 메서드
    def display_menu(self):
        print()
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    # 숫자 입력을 안전하게 받는 메서드
    def get_number_input(self, prompt, minimum, maximum):
        while True:
            try:
                # 사용자 입력을 받고 양쪽 공백 제거
                raw_value = input(prompt).strip()

            # Ctrl+C 또는 입력 종료 같은 상황 처리
            except (KeyboardInterrupt, EOFError):
                print()
                print("입력이 중단되었습니다. 안전하게 종료합니다.")
                return None

            # 빈 입력이면 다시 입력 요청
            if raw_value == "":
                print(f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue

            try:
                # 문자열을 정수로 변환 시도
                value = int(raw_value)

            # 숫자로 바꿀 수 없으면 다시 입력 요청
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue

            # 범위 안의 숫자라면 반환
            if minimum <= value <= maximum:
                return value

            # 범위를 벗어나면 다시 입력 요청
            print(f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")

    # 게임의 전체 실행 흐름을 담당하는 메서드
    def run(self):
        while True:
            self.display_menu()
            menu = self.get_number_input("선택: ", 1, 5)

            # 입력이 중단되면 저장 후 종료
            if menu is None:
                self.save()
                break

            # 메뉴 번호에 따라 각각의 기능 실행
            if menu == 1:
                self.play_quiz()
            elif menu == 2:
                self.add_quiz()
            elif menu == 3:
                self.list_quizzes()
            elif menu == 4:
                self.show_best_score()
            elif menu == 5:
                self.save()
                print("👋 게임을 종료합니다.")
                break

    # 현재 게임 상태를 JSON 파일에 저장하는 메서드
    def save(self):
        # 저장할 데이터를 딕셔너리로 정리
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }

        try:
            # state.json 파일을 쓰기 모드로 열기
            with STATE_FILE.open("w", encoding="utf-8") as file:
                # JSON 형태로 저장
                json.dump(data, file, ensure_ascii=False, indent=4)

                # 파일 마지막 줄바꿈 추가
                file.write("\n")

        # 파일 저장 중 운영체제 관련 오류가 발생하면 메시지 출력
        except OSError:
            print("데이터 저장 중 오류가 발생했습니다.")

    # 저장된 JSON 파일을 읽어 게임 상태를 복구하는 메서드
    def load(self):
        # 저장 파일이 없으면 기본 퀴즈로 시작
        if not STATE_FILE.exists():
            print("저장 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
            return

        try:
            # state.json 파일을 읽기 모드로 열기
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            # 저장된 퀴즈 데이터를 Quiz 객체 목록으로 복원
            self.quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]

            # 최고 점수 정보 복원
            self.best_score = data.get("best_score")
            self.best_correct = data.get("best_correct", 0)
            self.best_total = data.get("best_total", 0)

            # 최고 점수가 없으면 0으로 표시하기 위한 문자열 처리
            score_text = self.best_score if self.best_score is not None else 0

            print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(self.quizzes)}개, 최고점수 {score_text}점")

        # 파일 손상, 형식 오류, 잘못된 데이터 등 예외 처리
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장 파일을 읽을 수 없어 기본 퀴즈 데이터로 복구합니다.")

            # 문제가 생기면 기본 상태로 되돌림
            self.quizzes = create_default_quizzes()
            self.best_score = None
            self.best_correct = 0
            self.best_total = 0

            # 복구된 상태를 다시 저장
            self.save()

    # 등록된 퀴즈를 순서대로 푸는 메서드
    def play_quiz(self):
        # 퀴즈가 없으면 안내 후 종료
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        # 맞힌 문제 개수 초기화
        correct_count = 0

        print()
        print(f"📝 퀴즈를 시작합니다! 총 {len(self.quizzes)}문제")

        # 퀴즈를 하나씩 출력하고 답 입력받기
        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            answer = self.get_number_input("정답 입력 (1-4): ", 1, 4)

            # 도중에 입력이 중단되면 저장 후 종료
            if answer is None:
                self.save()
                return

            # 정답 여부 판별
            if quiz.is_correct(answer):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        # 모든 문제를 다 풀면 결과 출력
        self.show_result(correct_count, len(self.quizzes))

    # 퀴즈 결과를 출력하고 최고 점수를 갱신하는 메서드
    def show_result(self, correct_count, total_count):
        # 점수를 100점 만점 기준으로 계산
        score = round((correct_count / total_count) * 100)

        print("=" * 40)
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

        # 최고 점수가 없거나, 이번 점수가 더 높으면 최고 점수 갱신
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total_count
            self.save()
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"🏆 현재 최고 점수는 {self.best_score}점입니다.")

        print("=" * 40)

    # 빈 문자열이 아닌 일반 텍스트 입력을 안전하게 받는 메서드
    def get_text_input(self, prompt):
        while True:
            try:
                # 사용자 입력을 받고 양쪽 공백 제거
                value = input(prompt).strip()

            # Ctrl+C 또는 입력 종료 처리
            except (KeyboardInterrupt, EOFError):
                print()
                print("입력이 중단되었습니다. 가능한 범위에서 저장 후 종료합니다.")
                return None

            # 비어 있지 않은 입력이면 반환
            if value:
                return value

            # 빈 입력이면 다시 입력 요청
            print("⚠️ 빈 입력은 사용할 수 없습니다. 다시 입력하세요.")

    # 새로운 퀴즈를 추가하는 메서드
    def add_quiz(self):
        print()
        print("📌 새로운 퀴즈를 추가합니다.")

        # 문제 입력받기
        question = self.get_text_input("문제를 입력하세요: ")
        if question is None:
            self.save()
            return

        # 선택지 4개 입력받기
        choices = []
        for index in range(1, 5):
            choice = self.get_text_input(f"선택지 {index}: ")
            if choice is None:
                self.save()
                return
            choices.append(choice)

        # 정답 번호 입력받기
        answer = self.get_number_input("정답 번호 (1-4): ", 1, 4)
        if answer is None:
            self.save()
            return

        # 새 퀴즈를 목록에 추가
        self.quizzes.append(Quiz(question, choices, answer))

        # 변경사항 저장
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")

    # 현재 등록된 퀴즈 목록을 출력하는 메서드
    def list_quizzes(self):
        # 퀴즈가 없으면 안내 메시지 출력
        if not self.quizzes:
            print("📋 등록된 퀴즈가 없습니다.")
            return

        print()
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)

        # 퀴즈 번호와 문제 제목 출력
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")

        print("-" * 40)

    # 최고 점수를 출력하는 메서드
    def show_best_score(self):
        # 아직 기록이 없으면 안내
        if self.best_score is None:
            print("🏆 아직 퀴즈를 푼 기록이 없습니다.")
            return

        # 최고 점수와 맞힌 문제 수 출력
        print(
            f"🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )


# 프로그램 시작 함수
def main():
    # QuizGame 객체 생성
    game = QuizGame()

    # 게임 실행
    game.run()


# 이 파일을 직접 실행했을 때만 main() 실행
if __name__ == "__main__":
    main()