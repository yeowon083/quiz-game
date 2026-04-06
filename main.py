import json
from pathlib import Path


STATE_FILE = Path("state.json")
SEPARATOR = "=" * 40
LINE = "-" * 40


class InputTerminated(Exception):
    """사용자 입력이 Ctrl+C 또는 EOF로 종료된 상황을 나타낸다."""


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, number):
        print(LINE)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for idx, choice in enumerate(self.choices, start=1):
            print(f"{idx}. {choice}")
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
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제(question) 값이 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지(choices)는 4개여야 합니다.")
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(answer, int) or answer < 1 or answer > 4:
            raise ValueError("정답(answer)은 1~4 사이 정수여야 합니다.")

        return cls(question.strip(), [c.strip() for c in choices], answer)


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.best_correct = None
        self.best_total = None

    def get_default_quizzes(self):
        return [
            Quiz(
                "Python에서 변수는 무엇을 저장하기 위해 사용하나요?",
                ["함수 이름", "데이터 값", "반복 횟수만", "주석 내용"],
                2,
            ),
            Quiz(
                "다음 중 정수형(int) 값은 무엇인가요?",
                ["3.14", '"hello"', "42", "True"],
                3,
            ),
            Quiz(
                "조건에 따라 다른 코드를 실행할 때 사용하는 문법은?",
                ["for", "while", "if/elif/else", "def"],
                3,
            ),
            Quiz(
                "리스트(list)에 대한 설명으로 올바른 것은?",
                ["키-값 쌍으로만 저장한다", "순서가 있고 여러 값을 저장할 수 있다", "참/거짓만 저장한다", "숫자만 저장할 수 있다"],
                2,
            ),
            Quiz(
                "함수를 정의할 때 사용하는 키워드는?",
                ["class", "return", "def", "import"],
                3,
            ),
            Quiz(
                "클래스의 생성자 메서드 이름은 무엇인가요?",
                ["create", "__start__", "__init__", "self"],
                3,
            ),
        ]

    def input_number(self, prompt, min_value, max_value):
        range_message = f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이 숫자를 입력하세요."
        while True:
            try:
                raw = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                raise InputTerminated

            if not raw:
                print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
                continue

            try:
                value = int(raw)
            except ValueError:
                print(range_message)
                continue

            if value < min_value or value > max_value:
                print(range_message)
                continue

            return value

    def input_text(self, prompt):
        while True:
            try:
                text = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                raise InputTerminated

            if not text:
                print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

    def load_state(self):
        if not STATE_FILE.exists():
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.best_correct = None
            self.best_total = None
            print(f"📂 저장 파일이 없어 기본 퀴즈를 사용합니다. (퀴즈 {len(self.quizzes)}개)")
            return

        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            raw_quizzes = data.get("quizzes", [])
            quizzes = [Quiz.from_dict(item) for item in raw_quizzes]
            self.quizzes = quizzes

            best_score = data.get("best_score")
            best_correct = data.get("best_correct")
            best_total = data.get("best_total")

            self.best_score = best_score if isinstance(best_score, int) else None
            self.best_correct = best_correct if isinstance(best_correct, int) else None
            self.best_total = best_total if isinstance(best_total, int) else None

            print(
                "📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score if self.best_score is not None else '없음'})"
            )

            if not self.quizzes:
                print("ℹ️ 저장된 퀴즈가 없어 기본 퀴즈를 복구합니다.")
                self.quizzes = self.get_default_quizzes()
                self.save_state()

        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            print("⚠️ state.json 파일이 없거나 손상되었습니다. 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.best_correct = None
            self.best_total = None
            self.save_state()

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            with STATE_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 데이터를 저장하지 못했습니다. 파일 권한을 확인하세요.")

    def show_menu(self):
        print()
        print(SEPARATOR)
        print("        나만의 퀴즈 게임")
        print(SEPARATOR)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(SEPARATOR)

    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print()
        print(f"📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct_count = 0

        for idx, quiz in enumerate(self.quizzes, start=1):
            quiz.show(idx)
            user_answer = self.input_number("정답 입력 (1-4): ", 1, 4)
            if quiz.is_correct(user_answer):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다! 정답은 {quiz.answer}번입니다.")

        total = len(self.quizzes)
        score = int((correct_count / total) * 100)
        print()
        print(SEPARATOR)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total
            self.save_state()
            print("🎉 새로운 최고 점수입니다!")
        elif score == self.best_score:
            print("👏 최고 점수와 동일한 점수입니다!")
        else:
            print(f"ℹ️ 현재 최고 점수는 {self.best_score}점입니다.")
        print(SEPARATOR)

    def add_quiz(self):
        print()
        print("📌 새로운 퀴즈를 추가합니다.")
        question = self.input_text("문제를 입력하세요: ")
        choices = []
        for idx in range(1, 5):
            choice = self.input_text(f"선택지 {idx}: ")
            choices.append(choice)
        answer = self.input_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print()
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print(LINE)
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"[{idx}] {quiz.question}")
        print(LINE)

    def show_best_score(self):
        if self.best_score is None:
            print("ℹ️ 아직 퀴즈를 풀지 않았습니다.")
            return

        print("🏆 최고 점수 정보")
        print(
            f"- 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )

    def run(self):
        self.load_state()
        while True:
            self.show_menu()
            choice = self.input_number("선택: ", 1, 5)
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            else:
                self.save_state()
                print("👋 게임을 종료합니다. 데이터가 저장되었습니다.")
                break


def main():
    game = QuizGame()
    try:
        game.run()
    except InputTerminated:
        print("\n⚠️ 입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
        game.save_state()


if __name__ == "__main__":
    main()
