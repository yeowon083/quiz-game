"""퀴즈 한 문제를 표현하는 모듈입니다."""


class Quiz:
    """개별 퀴즈의 문제, 선택지, 정답을 관리합니다."""

    def __init__(self, question, choices, answer):
        # 문제로 보여 줄 문장입니다.
        self.question = question
        # 사용자가 고를 수 있는 4개의 선택지입니다.
        self.choices = choices
        # 정답 번호입니다. 화면의 선택지 번호와 맞추기 위해 1부터 4까지 사용합니다.
        self.answer = answer

    def display(self, number):
        """퀴즈 번호와 함께 문제와 선택지를 화면에 출력합니다."""
        print("-" * 40)
        print(f"📝 [문제 {number}]")
        print(self.question)
        print()

        # 선택지를 1번부터 보여 주기 위해 enumerate의 start 값을 1로 지정합니다.
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 입력한 답이 정답인지 확인합니다."""
        return user_answer == self.answer

    def to_dict(self):
        """Quiz 객체를 JSON 저장이 가능한 딕셔너리로 변환합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리 데이터를 검증한 뒤 Quiz 객체로 복원합니다."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]

        # 저장 파일이 손상되었을 때 잘못된 값으로 객체가 만들어지지 않도록 검증합니다.
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개의 목록이어야 합니다.")
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1부터 4 사이의 숫자여야 합니다.")

        # 저장된 문자열의 앞뒤 공백을 정리한 뒤 객체를 생성합니다.
        return cls(
            question.strip(),
            [choice.strip() for choice in choices],
            answer,
        )
