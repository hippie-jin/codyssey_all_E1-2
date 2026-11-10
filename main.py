from default_quizzes import get_default_quizzes
from quiz import Quiz


def show_menu():
    """메뉴 화면을 출력한다."""
    print()
    print("=" * 40)
    print("      🎯 Python 이해 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def read_int(prompt, low, high):
    """low~high 사이의 정수를 입력받아 반환한다. 잘못된 입력이면 다시 묻는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 입력이 비어 있습니다.")
            continue
        try:
            number = int(text)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number


def read_text(prompt):
    """비어 있지 않은 문자열을 입력받아 반환한다. 빈 입력이면 다시 묻는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 입력이 비어 있습니다.")
            continue
        return text


def add_quiz(quizzes):
    """사용자에게 입력받아 새 Quiz를 quizzes에 추가한다."""
    print("\n📌 새로운 퀴즈를 추가합니다.\n")
    question = read_text("문제를 입력하세요: ")
    choices = []
    for i in range(1, 5):
        choices.append(read_text(f"선택지 {i}: "))
    answer = read_int("정답 번호 (1-4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("\n✅ 퀴즈가 추가되었습니다!")


def list_quizzes(quizzes):
    """등록된 퀴즈의 문제 목록을 출력한다."""
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return

    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("-" * 40)
    for number, quiz in enumerate(quizzes, start=1):
        print(f"[{number}] {quiz.question}")
    print("-" * 40)


def play_quiz(quizzes):
    """퀴즈를 모두 출제하고 정답 수를 반환한다. 퀴즈가 없으면 None을 반환한다."""
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return None

    print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")
    correct = 0
    for number, quiz in enumerate(quizzes, start=1):
        print("-" * 40)
        print(f"[문제 {number}]")
        quiz.show()
        answer = read_int("\n정답 입력: ", 1, 4)
        if quiz.is_correct(answer):
            print("✅ 정답입니다!")
            correct += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

    print("=" * 40)
    print(f"🏆 결과: {len(quizzes)}문제 중 {correct}문제 정답!")
    print("=" * 40)
    return correct


def main():
    quizzes = get_default_quizzes()
    try:
        while True:
            show_menu()
            choice = read_int("선택: ", 1, 5)
            if choice == 1:
                play_quiz(quizzes)
            elif choice == 2:
                add_quiz(quizzes)
            elif choice == 3:
                list_quizzes(quizzes)
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break
            else:
                print("(아직 구현되지 않았습니다)")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
