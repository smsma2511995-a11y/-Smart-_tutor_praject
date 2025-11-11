# models/lightweight_smart_ai.py - لقطة التهيئة والتحسين
import re

# ملاحظة: هذا الملف يحتوي على الجزء ذي الصلة بالتهيئة واستخراج المفهوم.
# افترضت وجود التعريفات للـ LightweightUnderstandingModel, SmartQuestionGenerator, LanguageCourseGenerator, SmartMemorizationSystem
# في أماكن أخرى من المشروع.

class LightweightSmartAI:
    def __init__(self, knowledge_base_path=None, enable_spaced_repetition=True):
        print("🧠 تهيئة الذكاء الاصطناعي التعليمي المتكامل...")
        
        # 🔧 إصلاح: تهيئة user_progress
        self.user_progress = {}
        self.conversation_memory = []
        self.review_schedule = {}
        
        # 1. تحميل مكونات الذكاء الاصطناعي الخفيف
        # ملاحظة: التأكد من استيراد/تعريف هذه الأصناف في المشروع
        self.understanding_model = LightweightUnderstandingModel()
        self.question_generator = SmartQuestionGenerator()
        self.language_course_generator = LanguageCourseGenerator()
        self.memorization_system = SmartMemorizationSystem()
        
        # 2. إعداد قاعدة المعرفة والذاكرة المتقدمة
        self.spaced_repetition_enabled = enable_spaced_repetition
        self.knowledge_base = self.load_enhanced_knowledge_base(knowledge_base_path)
        
        print("✅ الذكاء الاصطناعي المتكامل جاهز للعمل! (أوفلاين + مراجعة متباعدة)")

    # 🔧 إصلاح: تحسين استخراج المفاهيم من الأسئلة
    def extract_concept_from_question(self, question: str) -> str:
        """استخراج المفهوم من نص السؤال - النسخة المحسنة"""
        try:
            # قائمة بأنماط الأسئلة الشائعة
            patterns = [
                (r'ما تعريف\s+"([^"]+)"', 1),
                (r'ما تعريف\s+(.+)?', 1),
                (r'ما ترجمة\s+"([^"]+)"', 1),
                (r'ما ترجمة\s+(.+)?', 1),
                (r'ما معنى\s+"([^"]+)"', 1),
                (r'ما معنى\s+(.+)?', 1),
                (r'كيف\s+(.+)?', 1),
                (r'ما هي\s+(.+)?', 1)
            ]
            
            for pattern, group_idx in patterns:
                match = re.search(pattern, question)
                if match:
                    concept = match.group(group_idx).strip()
                    # تنظيف النتيجة
                    concept = re.sub(r'[؟
?]', '', concept)
                    if len(concept) > 2:  # تجاهل الكلمات القصيرة
                        return concept[:50]  # تقليل الطول
            
            # إذا لم نجد نمطاً مطابقاً، نأخذ أول كلمتين مهمتين
            words = question.split()
            important_words = [w for w in words if len(w) > 3 and w not in ['ما', 'هو', 'هي', 'كيف', 'لماذا']]
            if important_words:
                return ' '.join(important_words[:2])
            
            return "مفهوم عام"
        except Exception as e:
            print(f"⚠️ خطأ في استخراج المفهوم: {e}")
            return "مفهوم عام"