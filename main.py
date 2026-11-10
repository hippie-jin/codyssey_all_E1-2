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


def main():
    try:
        while True:
            show_menu()
            choice = read_int("선택: ", 1, 5)
            if choice == 5:
                print("프로그램을 종료합니다.")
                break
            print("(아직 구현되지 않았습니다)")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
