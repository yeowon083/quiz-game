import json
import random
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
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개의 목록이어야 합니다.")
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1부터 4 사이의 숫자여야 합니다.")

        return cls(
            question.strip(),
            [choice.strip() for choice in choices],
            answer,
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
        self.best_correct = 0
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
                self.play_quiz()
            elif menu == 2:
                self.add_quiz()
            elif menu == 3:
                self.list_quizzes()
            elif menu == 4:
                self.show_best_score()
            elif menu == 5:
                self.save()
                print("게임을 종료합니다.")
                break

    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }

        try:
            with STATE_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write("\n")
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
            self.best_correct = data.get("best_correct", 0)
            self.best_total = data.get("best_total", 0)
            score_text = self.best_score if self.best_score is not None else 0
            print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(self.quizzes)}개, 최고점수 {score_text}점")
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장 파일을 읽을 수 없어 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = create_default_quizzes()
            self.best_score = None
            self.best_correct = 0
            self.best_total = 0
            self.save()

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        quizzes = self.quizzes[:]
        random.shuffle(quizzes)
        correct_count = 0

        print()
        print(f"퀴즈를 시작합니다! 총 {len(quizzes)}문제")

        for index, quiz in enumerate(quizzes, start=1):
            quiz.display(index)
            answer = self.get_number_input("정답 입력 (1-4): ", 1, 4)

            if answer is None:
                self.save()
                return

            if quiz.is_correct(answer):
                correct_count += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        self.show_result(correct_count, len(quizzes))

    def show_result(self, correct_count, total_count):
        score = round((correct_count / total_count) * 100)
        print("=" * 40)
        print(f"결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total_count
            self.save()
            print("새로운 최고 점수입니다!")
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")
        print("=" * 40)

    def get_text_input(self, prompt):
        while True:
            try:
                value = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print()
                print("입력이 중단되었습니다. 가능한 범위에서 저장 후 종료합니다.")
                return None

            if value:
                return value

            print("빈 입력은 사용할 수 없습니다. 다시 입력하세요.")

    def add_quiz(self):
        print()
        print("새로운 퀴즈를 추가합니다.")

        question = self.get_text_input("문제를 입력하세요: ")
        if question is None:
            self.save()
            return

        choices = []
        for index in range(1, 5):
            choice = self.get_text_input(f"선택지 {index}: ")
            if choice is None:
                self.save()
                return
            choices.append(choice)

        answer = self.get_number_input("정답 번호 (1-4): ", 1, 4)
        if answer is None:
            self.save()
            return

        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print()
        print(f"등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)

    def show_best_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return

        print(
            f"최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
