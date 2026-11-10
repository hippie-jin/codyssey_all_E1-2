from quiz import Quiz


def get_default_quizzes():
    """기본 퀴즈 목록(주제: Python의 이해)을 Quiz 객체 리스트로 반환한다."""
    return [
        Quiz(
            "Python에서 정수를 나타내는 자료형은?",
            ["int", "str", "bool", "list"],
            1,
        ),
        Quiz(
            "키(key)와 값(value)을 쌍으로 저장하는 자료형은?",
            ["list", "str", "dict", "bool"],
            3,
        ),
        Quiz(
            "올바른 입력이 올 때까지처럼, 반복 횟수를 모르고 조건이 참인 동안 반복할 때 알맞은 문장은?",
            ["for", "if", "def", "while"],
            4,
        ),
        Quiz(
            "함수가 계산한 결과를 호출한 곳으로 돌려줄 때 사용하는 키워드는?",
            ["print", "input", "return", "break"],
            3,
        ),
        Quiz(
            "클래스로 객체가 만들어질 때 자동으로 실행되는 초기화 메서드는?",
            ["__main__", "__init__", "__name__", "__file__"],
            2,
        ),
        Quiz(
            'int("abc")를 실행하면 발생하는 예외는?',
            ["ValueError", "TypeError", "KeyError", "IndexError"],
            1,
        ),
    ]
