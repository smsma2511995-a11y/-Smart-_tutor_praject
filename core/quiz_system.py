# core/quiz_system.py
import random
from typing import List, Dict
from datetime import datetime

class QuizSystem:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.quizzes = self.load_quizzes()
    
    def load_quizzes(self):
        """تحميل بنك الأسئلة"""
        return {
            "math": [
                {
                    "question": "ما هو حل المعادلة: 2س + 5 = 15؟",
                    "options": ["س = 5", "س = 10", "س = 7.5", "س = 8"],
                    "correct": 0,
                    "explanation": "2س + 5 = 15 → 2س = 10 → س = 5"
                },
                {
                    "question": "ما هي مساحة المربع الذي طول ضلعه 6 سم؟",
                    "options": ["24 سم²", "36 سم²", "30 سم²", "42 سم²"],
                    "correct": 1,
                    "explanation": "مساحة المربع = الضلع × الضلع = 6 × 6 = 36 سم²"
                }
            ],
            "science": [
                {
                    "question": "ما هو العنصر الكيميائي الذي رمزه O؟",
                    "options": ["ذهب", "أوكسجين", "فضة", "حديد"],
                    "correct": 1,
                    "explanation": "O هو رمز عنصر الأوكسجين"
                }
            ]
        }
    
    def generate_quiz(self, subject: str, difficulty: str = "medium", num_questions: int = 5):
        """توليد اختبار تلقائي"""
        if subject not in self.quizzes:
            return None
        
        questions = random.sample(self.quizzes[subject], min(num_questions, len(self.quizzes[subject])))
        
        quiz = {
            "subject": subject,
            "difficulty": difficulty,
            "questions": questions,
            "timestamp": datetime.now().isoformat(),
            "user_score": 0,
            "total_score": len(questions)
        }
        
        return quiz
    
    def evaluate_quiz(self, quiz: Dict, user_answers: List[int]):
        """تقييم الإجابات"""
        correct_count = 0
        results = []
        
        for i, (question, user_answer) in enumerate(zip(quiz["questions"], user_answers)):
            is_correct = user_answer == question["correct"]
            if is_correct:
                correct_count += 1
            
            results.append({
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": question["correct"],
                "is_correct": is_correct,
                "explanation": question["explanation"]
            })
        
        quiz["user_score"] = correct_count
        quiz["percentage"] = (correct_count / len(quiz["questions"])) * 100
        
        return {
            "quiz": quiz,
            "results": results,
            "feedback": self.generate_feedback(quiz["percentage"])
        }
    
    def generate_feedback(self, percentage: float):
        """توليد تعليق على الأداء"""
        if percentage >= 90:
            return "ممتاز! 👏 لديك فهم رائع للمادة"
        elif percentage >= 70:
            return "جيد جداً! 👍 مستواك جيد"
        elif percentage >= 50:
            return "ليس سيئاً! 💪 تحتاج لمزيد من الممارسة"
        else:
            return "يحتاج تحسين! 📚 راجع الدروس مرة أخرى"
