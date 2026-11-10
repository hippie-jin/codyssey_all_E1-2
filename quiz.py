class Quiz:
    """퀴즈 한 개를 표현한다. 정답은 1~4 중 하나의 번호로 관리한다."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        """문제와 선택지를 출력한다."""
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, number):
        """입력한 번호가 정답이면 True를 반환한다."""
        return number == self.answer

    def to_dict(self):
        """JSON 저장을 위해 dict로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """dict에서 Quiz 객체를 만든다."""
        return cls(data["question"], data["choices"], data["answer"])
