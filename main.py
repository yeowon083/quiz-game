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


def main():
    game = QuizGame()
    print(f"나만의 퀴즈 게임: 기본 퀴즈 {len(game.quizzes)}개")


if __name__ == "__main__":
    main()
