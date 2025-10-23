# utils/feedback_system.py
import json
from datetime import datetime
from pathlib import Path

class FeedbackSystem:
    def __init__(self):
        self.feedback_file = Path("data/feedback.json")
        self.feedback_file.parent.mkdir(exist_ok=True)
        self.load_feedback()
    
    def load_feedback(self):
        """تحميل التقييمات السابقة"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                self.feedbacks = json.load(f)
        except:
            self.feedbacks = []
    
    def add_feedback(self, question: str, answer: str, rating: int, comments: str = ""):
        """إضافة تقييم جديد"""
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "rating": rating,  # 1-5
            "comments": comments,
            "improved": False
        }
        
        self.feedbacks.append(feedback)
        self.save_feedback()
        
        # إذا كان التقييم منخفضاً، طلب التحسين
        if rating < 3:
            self.suggest_improvement(feedback)
    
    def suggest_improvement(self, feedback):
        """اقتراح تحسين للإجابات الضعيفة"""
        print(f"🔧 يحتاج تحسين: {feedback['question']}")
        # يمكن ربط هذا بالنموذج لتحسين الإجابات المستقبلية
    
    def get_analytics(self):
        """إحصائيات الأداء"""
        if not self.feedbacks:
            return {"total": 0, "average_rating": 0}
        
        total = len(self.feedbacks)
        average_rating = sum(f['rating'] for f in self.feedbacks) / total
        
        return {
            "total_feedbacks": total,
            "average_rating": round(average_rating, 2),
            "excellent": len([f for f in self.feedbacks if f['rating'] >= 4]),
            "needs_improvement": len([f for f in self.feedbacks if f['rating'] <= 2])
        }
    
    def save_feedback(self):
        """حفظ التقييمات"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedbacks, f, ensure_ascii=False, indent=2)

# دمج نظام التقييم في الواجهة
def add_feedback_to_ui():
    """إضافة أزرار التقييم في الواجهة"""
    feedback_html = """
    <BoxLayout orientation='horizontal' size_hint_y=0.1>
        <Label text='كيف كانت الإجابة؟' size_hint_x=0.4>
        <Button text='👍' on_press=lambda x: rate_answer(5)>
        <Button text='😐' on_press=lambda x: rate_answer(3)>
        <Button text='👎' on_press=lambda x: rate_answer(1)>
    </BoxLayout>
    """
    return feedback_html
