# models/language_course_generator.py - النسخة المحسنة
import json
import random
import re
from pathlib import Path
from typing import Dict, List, Any
import sqlite3

class LanguageCourseGenerator:
    def __init__(self, database_path=None):
        self.supported_languages = ['english', 'french']
        self.difficulty_levels = ['beginner', 'intermediate', 'advanced']
        
        # 🔧 إصلاح: تهيئة user_progress
        self.user_progress = {}
        
        # قاعدة بيانات المفردات الأساسية (محسنة)
        self.vocabulary_db = self.initialize_vocabulary_database(database_path)
        
        # هياكل الدروس النموذجية
        self.lesson_templates = {
            'vocabulary': self.generate_vocabulary_lesson,
            'grammar': self.generate_grammar_lesson,
            'conversation': self.generate_conversation_lesson,
            'reading': self.generate_reading_lesson,
            'listening': self.generate_listening_lesson
        }
        
        print("📚 نظام توليد الدروس اللغوية جاهز!")
    
    def initialize_vocabulary_database(self, db_path):
        """تهيئة قاعدة بيانات المفردات الأساسية (محسنة)"""
        if db_path and Path(db_path).exists():
            return self.load_vocabulary_from_db(db_path)
        
        # قاعدة بيانات افتراضية شاملة - مع إصلاح الفرنسية
        vocabulary = {
            'english': {
                'beginner': [
                    {'word': 'hello', 'translation': 'مرحباً', 'category': 'greetings', 'example': 'Hello, how are you?'},
                    {'word': 'goodbye', 'translation': 'مع السلامة', 'category': 'greetings', 'example': 'Goodbye, see you tomorrow!'},
                    {'word': 'please', 'translation': 'من فضلك', 'category': 'politeness', 'example': 'Please help me.'},
                    {'word': 'thank you', 'translation': 'شكراً', 'category': 'politeness', 'example': 'Thank you very much.'},
                    {'word': 'yes', 'translation': 'نعم', 'category': 'basics', 'example': 'Yes, I understand.'},
                    {'word': 'no', 'translation': 'لا', 'category': 'basics', 'example': 'No, thank you.'},
                    {'word': 'water', 'translation': 'ماء', 'category': 'food_drink', 'example': 'I want water.'},
                    {'word': 'food', 'translation': 'طعام', 'category': 'food_drink', 'example': 'The food is delicious.'},
                    {'word': 'house', 'translation': 'منزل', 'category': 'places', 'example': 'My house is big.'},
                    {'word': 'family', 'translation': 'عائلة', 'category': 'family', 'example': 'I love my family.'}
                ],
                'intermediate': [
                    {'word': 'environment', 'translation': 'بيئة', 'category': 'nature', 'example': 'We must protect the environment.'},
                    {'word': 'technology', 'translation': 'تكنولوجيا', 'category': 'modern', 'example': 'Technology is advancing quickly.'},
                    {'word': 'education', 'translation': 'تعليم', 'category': 'academic', 'example': 'Education is important for everyone.'},
                    {'word': 'communication', 'translation': 'اتصال', 'category': 'social', 'example': 'Good communication is key.'},
                    {'word': 'development', 'translation': 'تطور', 'category': 'general', 'example': 'The development of the city is remarkable.'}
                ]
            },
            'french': {
                'beginner': [
                    # 🔧 إصلاح: المسافات والتشكيل في الفرنسية
                    {'word': 'bonjour', 'translation': 'مرحباً', 'category': 'greetings', 'example': 'Bonjour, comment ça va?'},
                    {'word': 'au revoir', 'translation': 'مع السلامة', 'category': 'greetings', 'example': 'Au revoir, à demain!'},
                    {'word': "s'il vous plaît", 'translation': 'من فضلك', 'category': 'politeness', 'example': "S'il vous plaît, aidez-moi."},
                    {'word': 'merci', 'translation': 'شكراً', 'category': 'politeness', 'example': 'Merci beaucoup.'},
                    {'word': 'oui', 'translation': 'نعم', 'category': 'basics', 'example': 'Oui, je comprends.'},
                    {'word': 'non', 'translation': 'لا', 'category': 'basics', 'example': 'Non, merci.'},
                    {'word': 'eau', 'translation': 'ماء', 'category': 'food_drink', 'example': "Je veux de l'eau."},
                    {'word': 'nourriture', 'translation': 'طعام', 'category': 'food_drink', 'example': 'La nourriture est délicieuse.'},
                    {'word': 'maison', 'translation': 'منزل', 'category': 'places', 'example': 'Ma maison est grande.'},
                    {'word': 'famille', 'translation': 'عائلة', 'category': 'family', 'example': "J'aime ma famille."}
                ],
                'intermediate': [
                    {'word': 'environnement', 'translation': 'بيئة', 'category': 'nature', 'example': "Nous devons protéger l'environnement."},
                    {'word': 'technologie', 'translation': 'تكنولوجيا', 'category': 'modern', 'example': 'La technologie avance rapidement.'},
                    {'word': 'éducation', 'translation': 'تعليم', 'category': 'academic', 'example': "L'éducation est importante pour tous."},
                    {'word': 'communication', 'translation': 'اتصال', 'category': 'social', 'example': 'Une bonne communication est essentielle.'},
                    {'word': 'développement', 'translation': 'تطور', 'category': 'general', 'example': 'Le développement de la ville est remarquable.'}
                ]
            }
        }
        
        return vocabulary
    
    def load_vocabulary_from_db(self, db_path):
        """تحميل المفردات من قاعدة بيانات SQLite"""
        # يمكن التوسع في المستقبل لاستخدام قاعدة بيانات حقيقية
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # جلب البيانات من الجدول
            cursor.execute("SELECT language, level, word, translation, category, example FROM vocabulary")
            rows = cursor.fetchall()
            
            vocabulary = {}
            for row in rows:
                language, level, word, translation, category, example = row
                if language not in vocabulary:
                    vocabulary[language] = {}
                if level not in vocabulary[language]:
                    vocabulary[language][level] = []
                
                vocabulary[language][level].append({
                    'word': word,
                    'translation': translation,
                    'category': category,
                    'example': example
                })
            
            conn.close()
            return vocabulary
        except Exception as e:
            print(f"⚠️ خطأ في تحميل قاعدة البيانات: {e}")
            return {}
    
    def generate_wrong_translations(self, correct_translation: str, vocabulary: List[Dict], count: int = 3) -> List[str]:
        """توليد ترجمات خاطئة للاختيار من متعدد - النسخة المحسنة"""
        
        # 🔧 إصلاح: جمع جميع الترجمات المتاحة بأمان
        all_translations = []
        for v in vocabulary:
            if 'translation' in v and v['translation'] != correct_translation:
                all_translations.append(v['translation'])
        
        # 🔧 إصلاح: استخدام min() لمنع أخطاء random.sample
        available_count = min(len(all_translations), count)
        
        if available_count > 0:
            wrong_answers = random.sample(all_translations, available_count)
        else:
            wrong_answers = []
        
        # 🔧 إصلاح: إذا لم تكن هناك ترجمات كافية، نبحث في قاعدة البيانات الكاملة
        if len(wrong_answers) < count:
            additional_translations = self.get_additional_translations(correct_translation, count - len(wrong_answers))
            wrong_answers.extend(additional_translations)
        
        # 🔧 إصلاح: إذا ما زلنا بحاجة للمزيد، نستخدم ترجمات افتراضية
        while len(wrong_answers) < count:
            wrong_answers.append(f"ترجمة {len(wrong_answers) + 1}")
        
        # خلط الإجابات عشوائياً
        random.shuffle(wrong_answers)
        return wrong_answers[:count]
    
    def get_additional_translations(self, correct_translation: str, needed_count: int) -> List[str]:
        """الحصول على ترجمات إضافية من قاعدة البيانات الكاملة"""
        additional = []
        
        try:
            for language in self.vocabulary_db.values():
                for level_words in language.values():
                    for word_data in level_words:
                        if (word_data.get('translation') and 
                            word_data['translation'] != correct_translation and
                            word_data['translation'] not in additional):
                            additional.append(word_data['translation'])
                            if len(additional) >= needed_count:
                                return additional
        except Exception as e:
            print(f"⚠️ خطأ في البحث عن ترجمات إضافية: {e}")
        
        return additional
    
    def get_vocabulary_for_lesson(self, language: str, level: str, count: int) -> List[Dict]:
        """الحصول على مفردات للدرس - النسخة المحسنة"""
        try:
            if (language in self.vocabulary_db and 
                level in self.vocabulary_db[language]):
                
                all_words = self.vocabulary_db[language][level]
                
                # 🔧 إصلاح: استخدام min() لمنع أخطاء random.sample
                available_count = min(len(all_words), count)
                
                if available_count > 0:
                    return random.sample(all_words, available_count)
                else:
                    return []
            return []
        except Exception as e:
            print(f"⚠️ خطأ في جلب المفردات: {e}")
            return []
    
    def extract_concepts_from_question(self, question: str) -> List[str]:
        """استخراج المفاهيم من السؤال - النسخة المحسنة"""
        try:
            concepts = []
            
            # أنماط للتعرف على المفاهيم في الأسئلة
            patterns = [
                r'ما تعريف\s+(.+)',
                r'ما ترجمة\s+(.+)',
                r'ما معنى\s+(.+)',
                r'كيف\s+(.+)',
                r'ما هي\s+(.+)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, question)
                for match in matches:
                    # تنظيف النتيجة
                    concept = match.strip().replace('؟', '').replace('"', '').split()[0]
                    if len(concept) > 2:  # تجاهل الكلمات القصيرة
                        concepts.append(concept)
            
            return concepts[:3]  # إرجاع أول 3 مفاهيم فقط
        except Exception as e:
            print(f"⚠️ خطأ في استخراج المفاهيم: {e}")
            return []

    # باقي الدوال تبقى كما هي مع تطبيق نفس مبدأ الحماية
    def generate_vocabulary_exercises(self, vocabulary: List[Dict], language: str) -> List[Dict]:
        """توليد تمارين المفردات - النسخة المحسنة"""
        exercises = []
        
        try:
            # تمرين الترجمة
            if vocabulary:
                # 🔧 إصلاح: استخدام min() لمنع الأخطاء
                available_words = min(3, len(vocabulary))
                selected_words = random.sample(vocabulary, available_words) if vocabulary else []
                
                for word in selected_words:
                    exercises.append({
                        'type': 'translation',
                        'question': f"ما ترجمة كلمة '{word['word']}' إلى العربية؟",
                        'options': self.generate_wrong_translations(word['translation'], vocabulary),
                        'correct_answer': word['translation'],
                        'explanation': f"الكلمة '{word['word']}' تعني '{word['translation']}'. مثال: {word['example']}"
                    })
            
            # تمرين اختيار الكلمة المناسبة
            if len(vocabulary) >= 3:
                correct_word = random.choice(vocabulary)
                sentence = correct_word['example'].replace(correct_word['word'], '______')
                
                # 🔧 إصلاح: استخدام min() لأخذ العينات
                option_count = min(3, len(vocabulary))
                options = [v['word'] for v in random.sample(vocabulary, option_count)]
                
                exercises.append({
                    'type': 'fill_blank',
                    'question': f"أكمل الجملة: {sentence}",
                    'options': options,
                    'correct_answer': correct_word['word'],
                    'explanation': f"الجملة الصحيحة: {correct_word['example']}"
                })
            
            return exercises
        except Exception as e:
            print(f"⚠️ خطأ في توليد التمارين: {e}")
            return []

# اختبار النظام المحسن
def test_improved_system():
    print("🧪 اختبار النظام المحسن...")
    
    generator = LanguageCourseGenerator()
    
    # اختبار دالة الترجمات الخاطئة المحسنة
    test_vocab = [
        {'word': 'hello', 'translation': 'مرحباً'},
        {'word': 'goodbye', 'translation': 'مع السلامة'}
    ]
    
    wrong_translations = generator.generate_wrong_translations('مرحباً', test_vocab, 3)
    print(f"✅ الترجمات الخاطئة المتولدة: {wrong_translations}")
    
    # اختبار استخراج المفاهيم
    test_question = "ما تعريف المعادلات التربيعية؟"
    concepts = generator.extract_concepts_from_question(test_question)
    print(f"✅ المفاهيم المستخرجة: {concepts}")
    
    # اختبار جلب المفردات
    vocab = generator.get_vocabulary_for_lesson('english', 'beginner', 5)
    print(f"✅ المفردات المجلوبة: {len(vocab)} كلمة")

if __name__ == "__main__":
    test_improved_system()