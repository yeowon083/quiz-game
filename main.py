import json
from pathlib import Path


STATE_FILE = Path("state.json")
LINE = "-" * 40


DEFAULT_QUIZZES = [
    {
        "question": "Python에서 값을 저장하기 위해 이름을 붙인 공간을 무엇이라고 하나요?",
        "choices": ["함수", "변수", "반복문", "주석"],
        "answer": 2,
    },
    {
        "question": "Python에서 여러 값을 순서대로 저장할 때 주로 사용하는 자료형은?",
        "choices": ["bool", "int", "list", "str"],
        "answer": 3,
    },
    {
        "question": "조건에 따라 다른 코드를 실행할 때 사용하는 키워드는?",
        "choices": ["if", "for", "def", "class"],
        "answer": 1,
    },
    {
        "question": "함수를 정의할 때 사용하는 Python 키워드는?",
        "choices": ["return", "import", "while", "def"],
        "answer": 4,
    },
    {
        "question": "객체를 만들기 위한 설계도 역할을 하는 문법은?",
        "choices": ["클래스", "딕셔너리", "문자열", "연산자"],
        "answer": 1,
    },
]


def make_default_state():
    """처음 실행할 때 사용할 기본 데이터를 만든다."""
    return {
        "quizzes": DEFAULT_QUIZZES.copy(),
        "best_score": None,
        "best_correct": 0,
        "best_total": 0,
    }


def is_valid_quiz(quiz):
    """저장 파일에서 읽은 퀴즈 데이터가 올바른지 확인한다."""
    if not isinstance(quiz, dict):
        return False

    question = quiz.get("question")
    choices = quiz.get("choices")
    answer = quiz.get("answer")

    return (
        isinstance(question, str)
        and question.strip() != ""
        and isinstance(choices, list)
        and len(choices) == 4
        and all(isinstance(choice, str) and choice.strip() for choice in choices)
        and isinstance(answer, int)
        and 1 <= answer <= 4
    )


def load_state():
    """state.json 파일을 읽고, 문제가 있으면 기본 데이터로 시작한다."""
    if not STATE_FILE.exists():
        print("저장 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
        return make_default_state()

    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            state = json.load(file)

        quizzes = state.get("quizzes", [])
        if not isinstance(quizzes, list) or not all(is_valid_quiz(quiz) for quiz in quizzes):
            raise ValueError

        state["quizzes"] = quizzes
        state["best_score"] = state.get("best_score")
        state["best_correct"] = state.get("best_correct", 0)
        state["best_total"] = state.get("best_total", 0)

        score = state["best_score"] if state["best_score"] is not None else 0
        print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(quizzes)}개, 최고점수 {score}점")
        return state
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        print("저장 파일을 읽을 수 없어 기본 퀴즈 데이터로 복구합니다.")
        return make_default_state()


def save_state(state):
    """현재 퀴즈와 최고 점수를 state.json에 저장한다."""
    try:
        with STATE_FILE.open("w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=4)
            file.write("\n")
    except OSError:
        print("데이터 저장 중 오류가 발생했습니다.")


def print_menu():
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


def get_number(prompt, minimum, maximum):
    """정해진 범위 안의 숫자를 입력받는다."""
    while True:
        try:
            text = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            print("입력이 중단되었습니다. 안전하게 종료합니다.")
            return None

        if text == "":
            print(f"잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")


def get_text(prompt):
    """빈 문자열이 아닌 글자를 입력받는다."""
    while True:
        try:
            text = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            print("입력이 중단되었습니다. 가능한 범위에서 저장 후 종료합니다.")
            return None

        if text:
            return text

        print("빈 입력은 사용할 수 없습니다. 다시 입력하세요.")


def print_quiz(quiz, number):
    print(LINE)
    print(f"[문제 {number}]")
    print(quiz["question"])
    print()

    for index, choice in enumerate(quiz["choices"], start=1):
        print(f"{index}. {choice}")

    print()


def play_quiz(state):
    quizzes = state["quizzes"]
    if not quizzes:
        print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return

    correct_count = 0

    print()
    print(f"퀴즈를 시작합니다! 총 {len(quizzes)}문제")

    for index, quiz in enumerate(quizzes, start=1):
        print_quiz(quiz, index)
        user_answer = get_number("정답 입력 (1-4): ", 1, 4)

        if user_answer is None:
            save_state(state)
            return

        if user_answer == quiz["answer"]:
            correct_count += 1
            print("정답입니다!")
        else:
            print(f"오답입니다. 정답은 {quiz['answer']}번입니다.")

    show_result(state, correct_count, len(quizzes))


def show_result(state, correct_count, total_count):
    score = round((correct_count / total_count) * 100)

    print("=" * 40)
    print(f"결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

    if state["best_score"] is None or score > state["best_score"]:
        state["best_score"] = score
        state["best_correct"] = correct_count
        state["best_total"] = total_count
        save_state(state)
        print("새로운 최고 점수입니다!")
    else:
        print(f"현재 최고 점수는 {state['best_score']}점입니다.")

    print("=" * 40)


def add_quiz(state):
    print()
    print("새로운 퀴즈를 추가합니다.")

    question = get_text("문제를 입력하세요: ")
    if question is None:
        save_state(state)
        return

    choices = []
    for index in range(1, 5):
        choice = get_text(f"선택지 {index}: ")
        if choice is None:
            save_state(state)
            return
        choices.append(choice)

    answer = get_number("정답 번호 (1-4): ", 1, 4)
    if answer is None:
        save_state(state)
        return

    state["quizzes"].append(
        {
            "question": question,
            "choices": choices,
            "answer": answer,
        }
    )
    save_state(state)
    print("퀴즈가 추가되었습니다!")


def list_quizzes(state):
    quizzes = state["quizzes"]
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    print()
    print(f"등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print(LINE)

    for index, quiz in enumerate(quizzes, start=1):
        print(f"[{index}] {quiz['question']}")

    print(LINE)


def show_best_score(state):
    if state["best_score"] is None:
        print("아직 퀴즈를 푼 기록이 없습니다.")
        return

    print(
        f"최고 점수: {state['best_score']}점 "
        f"({state['best_total']}문제 중 {state['best_correct']}문제 정답)"
    )


def main():
    state = load_state()

    while True:
        print_menu()
        menu = get_number("선택: ", 1, 5)

        if menu is None:
            save_state(state)
            break
        if menu == 1:
            play_quiz(state)
        elif menu == 2:
            add_quiz(state)
        elif menu == 3:
            list_quizzes(state)
        elif menu == 4:
            show_best_score(state)
        elif menu == 5:
            save_state(state)
            print("게임을 종료합니다.")
            break


if __name__ == "__main__":
    main()
