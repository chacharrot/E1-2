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

        if not os.path.exists(self.file_path):
            self.quizzes = default_quizzes
            self.save_data()
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.quizzes = [Quiz(q['question'], q['choices'], q['answer']) for q in data.get('quizzes', [])]
                self.best_score = data.get('best_score', 0)
        except (json.JSONDecodeError, IOError):
            print("\n[알림] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
            self.quizzes = default_quizzes
            self.save_data()

    def save_data(self):
        """현재 상태를 JSON 파일로 저장합니다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"파일 저장 중 오류 발생: {e}")

    def get_safe_input(self, prompt, min_val=None, max_val=None):
        """공백 제거, 숫자 변환, 범위 체크를 포함한 안전한 입력 함수"""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("입력이 비어 있습니다. 다시 입력해주세요.")
                    continue
                
                val = int(user_input)
                if min_val is not None and max_val is not None:
                    if not (min_val <= val <= max_val):
                        print(f"{min_val}~{max_val} 사이의 숫자를 입력해주세요.")
                        continue
                return val
            except ValueError:
                print("숫자만 입력 가능합니다. 다시 시도하세요.")

    def play_quiz(self):
        if not self.quizzes:
            print("\n출제할 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
            return

        print("\n--- 퀴즈 게임 시작! ---")
        current_score = 0
        for i, q in enumerate(self.quizzes, 1):
            print(f"\nQ{i}. {q.question}")
            for idx, choice in enumerate(q.choices, 1):
                print(f"  {idx}) {choice}")
            
            answer = self.get_safe_input("정답 번호 선택: ", 1, 4)
            if answer == q.answer:
                print("정답입니다! ✨")
                current_score += 1
            else:
                print(f"아쉽네요. 정답은 {q.answer}번입니다.")

        print(f"\n게임 종료! 당신의 점수: {current_score}/{len(self.quizzes)}")
        if current_score > self.best_score:
            print(f"축하합니다! 최고 점수 경신! ({self.best_score} -> {current_score})")
            self.best_score = current_score
            self.save_data()
            
