import json
import os
from pathlib import Path

from default_quizzes import get_default_quizzes
from input_utils import read_int, read_text
from quiz import Quiz

# 실행 위치와 상관없이 프로젝트 루트(이 파일이 있는 폴더)에 저장한다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"


def is_valid_quiz_data(data):
    """dict가 Quiz로 만들 수 있는 올바른 형태인지 확인한다."""
    if not isinstance(data, dict):
        return False
    question = data.get("question")
    choices = data.get("choices")
    answer = data.get("answer")
    if not isinstance(question, str) or question.strip() == "":
        return False
    if not isinstance(choices, list) or len(choices) != 4:
        return False
    if not all(isinstance(c, str) and c.strip() != "" for c in choices):
        return False
    # bool은 int의 하위 타입이므로 따로 제외한다.
    if not isinstance(answer, int) or isinstance(answer, bool) or not 1 <= answer <= 4:
        return False
    return True


def is_valid_best_score(best):
    """최고 점수가 None이거나 올바른 기록(dict)인지 확인한다."""
    if best is None:
        return True
    if not isinstance(best, dict):
        return False
    for key in ("score", "correct", "total"):
        value = best.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            return False
    return True


class QuizGame:
    """퀴즈 게임 전체(퀴즈 목록, 최고 점수, 메뉴)를 관리한다."""

    def __init__(self):
        self.quizzes = []
        self.best_score = None  # {"score": 점수, "correct": 정답 수, "total": 문제 수}
        self.load_state()

    def use_defaults(self):
        """기본 퀴즈와 초기 점수 상태로 되돌린다."""
        self.quizzes = get_default_quizzes()
        self.best_score = None

    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다. 없거나 손상되면 기본값을 쓴다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("🆕 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.use_defaults()
            return
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.use_defaults()
            return
        except OSError as error:
            print(f"⚠️ 저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다. ({error})")
            self.use_defaults()
            return

        quiz_data = data.get("quizzes") if isinstance(data, dict) else None
        best = data.get("best_score") if isinstance(data, dict) else None
        if (
            not isinstance(quiz_data, list)
            or not all(is_valid_quiz_data(item) for item in quiz_data)
            or not is_valid_best_score(best)
        ):
            print("⚠️ 저장 파일의 형식이 올바르지 않아 기본 퀴즈로 복구합니다.")
            self.use_defaults()
            return

        self.quizzes = [Quiz.from_dict(item) for item in quiz_data]
        self.best_score = best
        best_text = "없음" if best is None else f"{best['score']}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")

    def save_state(self):
        """퀴즈와 최고 점수를 state.json에 저장한다. 실패해도 프로그램은 계속 실행된다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        temp_file = STATE_FILE.with_name(STATE_FILE.name + ".tmp")
        try:
            # 임시 파일에 먼저 쓰고 교체해, 저장 도중 꺼져도 기존 파일이 손상되지 않게 한다.
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            os.replace(temp_file, STATE_FILE)
        except OSError as error:
            print(f"⚠️ 저장에 실패했습니다. ({error})")

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
            self.save_state()

    def add_quiz(self):
        """사용자에게 입력받아 새 Quiz를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(read_text(f"선택지 {i}: "))
        answer = read_int("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
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
            print("\n입력이 중단되어 저장 후 안전하게 종료합니다.")
        self.save_state()
