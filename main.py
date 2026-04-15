"""퀴즈 게임 실행 파일입니다."""

from quiz_game import QuizGame


def main():
    """QuizGame 객체를 만들고 게임을 시작합니다."""
    game = QuizGame()
    game.run()


# 이 파일을 직접 실행할 때만 게임을 시작합니다.
# 다른 파일에서 import할 때는 자동으로 실행되지 않습니다.
if __name__ == "__main__":
    main()
