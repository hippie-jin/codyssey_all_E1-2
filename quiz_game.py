from default_quizzes import get_default_quizzes
from input_utils import read_int, read_text
from quiz import Quiz


class QuizGame:
    """퀴즈 게임 전체(퀴즈 목록, 최고 점수, 메뉴)를 관리한다."""

    def __init__(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None  # {"score": 점수, "correct": 정답 수, "total": 문제 수}

    def show_menu(self):
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

    def play_quiz(self):
        """퀴즈를 모두 출제하고 정답 수를 반환한다. 퀴즈가 없으면 None을 반환한다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return None

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
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
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {correct}문제 정답!")
        print("=" * 40)
        return correct

    def record_result(self, correct):
        """정답 수로 점수를 계산해 출력하고, 최고 점수보다 높으면 갱신한다."""
        total = len(self.quizzes)
        record = {"score": correct * 100 // total, "correct": correct, "total": total}
        print(f"📊 점수: {record['score']}점")
        if self.best_score is None or record["score"] > self.best_score["score"]:
            self.best_score = record
            print("🎉 새로운 최고 점수입니다!")

    def add_quiz(self):
        """사용자에게 입력받아 새 Quiz를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(read_text(f"선택지 {i}: "))
        answer = read_int("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈의 문제 목록을 출력한다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def show_best(self):
        """최고 점수를 출력한다. 아직 푼 적이 없으면 안내한다."""
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다.")
            return
        best = self.best_score
        print(f"\n🏆 최고 점수: {best['score']}점 ({best['total']}문제 중 {best['correct']}문제 정답)")

    def run(self):
        """메뉴 루프를 실행한다."""
        try:
            while True:
                self.show_menu()
                choice = read_int("선택: ", 1, 5)
                if choice == 1:
                    correct = self.play_quiz()
                    if correct is not None:
                        self.record_result(correct)
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_best()
                else:
                    print("프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 안전하게 종료합니다.")
