import json
from pathlib import Path


STATE_FILE = Path("state.json")


class Quiz:
    """개별 퀴즈의 문제, 선택지, 정답을 관리한다."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number):
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
        )


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


class QuizGame:
    """퀴즈 목록과 점수를 포함한 게임 흐름을 관리한다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_total = 0
        self.load()

    def display_menu(self):
        print()
        print("=" * 40)
        print("        나만의 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def get_number_input(self, prompt, minimum, maximum):
        while True:
            try:
                raw_value = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print()
                print("입력이 중단되었습니다. 안전하게 종료합니다.")
                return None

            if raw_value == "":
                print(f"잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue

            try:
                value = int(raw_value)
            except ValueError:
                print(f"잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue

            if minimum <= value <= maximum:
                return value

            print(f"잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")

    def run(self):
        while True:
            self.display_menu()
            menu = self.get_number_input("선택: ", 1, 5)

            if menu is None:
                self.save()
                break
            if menu == 1:
                print("퀴즈 풀기 기능은 준비 중입니다.")
            elif menu == 2:
                print("퀴즈 추가 기능은 준비 중입니다.")
            elif menu == 3:
                print("퀴즈 목록 기능은 준비 중입니다.")
            elif menu == 4:
                print("점수 확인 기능은 준비 중입니다.")
            elif menu == 5:
                self.save()
                print("게임을 종료합니다.")
                break

    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_total": self.best_total,
        }

        try:
            with STATE_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("데이터 저장 중 오류가 발생했습니다.")

    def load(self):
        if not STATE_FILE.exists():
            print("저장 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
            return

        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]
            self.best_score = data.get("best_score")
            self.best_total = data.get("best_total", 0)
            print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(self.quizzes)}개")
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            print("저장 파일을 읽을 수 없어 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = create_default_quizzes()
            self.best_score = None
            self.best_total = 0
            self.save()


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
