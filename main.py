import json
import os

# [클래스 1] 개별 퀴즈를 관리하는 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 사이의 정수

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

class QuizGame:
    def __init__(self):
        self.file_path = 'state.json'
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        """JSON 파일에서 데이터를 로드하거나 기본 데이터를 설정합니다."""
        default_quizzes = [
            Quiz("Python에서 리스트에 요소를 추가하는 함수는?", ["push()", "append()", "add()", "insert_at()"], 2),
            Quiz("Python의 논리형(Boolean) 값이 아닌 것은?", ["True", "False", "None", "둘 다 맞음"], 3),
            Quiz("문자열을 정수로 변환하는 함수는?", ["str()", "float()", "int()", "char()"], 3),
            Quiz("다음 중 가변(Mutable) 자료형은?", ["tuple", "str", "list", "int"], 3),
            Quiz("딕셔너리에서 키-값 쌍을 가져오는 메서드는?", ["items()", "keys()", "values()", "get()"], 1)
        ]