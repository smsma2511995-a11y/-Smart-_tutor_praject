# models/polyglot_tutor.py
import torch
import torch.nn as nn
from transformers import PreTrainedModel, PretrainedConfig
import json
import re
from typing import Dict, List, Optional
import numpy as np

from .polyglot_model import PolyglotTutorConfig, PolyglotTutorModel
from .knowledge_base import EducationalKnowledgeBase
from .answer_generator import SmartAnswerGenerator

class PolyglotEducationalAI:
    def __init__(self, model_path=None):
        # التهيئة الأساسية
        self.config = PolyglotTutorConfig()
        self.model = PolyglotTutorModel(self.config)
        self.knowledge_base = EducationalKnowledgeBase()
        self.answer_generator = SmartAnswerGenerator(self.knowledge_base)
        self.tokenizer = self.create_optimized_tokenizer()
        
        # وضع التقييم للنموذج
        self.model.eval()
        
        if model_path:
            self.load_model(model_path)
    
    def create_optimized_tokenizer(self):
        """إنشاء tokenizer مبسط وفعال"""
        vocab = {
            # الرموز الخاصة
            "[PAD]": 0, "[UNK]": 1, "[CLS]": 2, "[SEP]": 3, "[MASK]": 4,
        }
        
        # إضافة المفردات التعليمية الشائعة
        educational_terms = [
            # عربية
            "شرح", "مثال", "قاعدة", "نظرية", "قانون", "معادلة", "مسألة", 
            "حل", "إجابة", "سؤال", "جواب", "تحليل", "استنتاج", "تعريف",
            "مفهوم", "أساسي", "متقدم", "تمرين", "امتحان", "درس", "تعلم",
            "طالب", "معلم", "مدرسة", "جامعة", "تعليم", "دراسة", "بحث",
            
            # إنجليزية
            "explain", "example", "rule", "theory", "law", "equation", "problem",
            "solution", "answer", "question", "analysis", "conclusion", "definition",
            "concept", "basic", "advanced", "exercise", "exam", "lesson", "learn",
            "student", "teacher", "school", "university", "education", "study", "research",
            
            # فرنسية
            "expliquez", "exemple", "règle", "théorie", "loi", "équation", "problème",
            "solution", "réponse", "question", "analyse", "conclusion", "définition",
            "concept", "basique", "avancé", "exercice", "examen", "leçon", "apprendre",
            "étudiant", "professeur", "école", "université", "éducation", "étude", "recherche"
        ]
        
        # إضافة الكلمات الأساسية
        base_words = [
            # عربية
            "ال", "في", "من", "على", "إلى", "مع", "ما", "هو", "هي", "كان", 
            "يكون", "كانت", "أنا", "أنت", "هو", "هي", "نحن", "هم", "هذا", "هذه",
            "ذلك", "تلك", "أين", "متى", "كيف", "لماذا", "كم", "أي", "كل", "بعض",
            
            # إنجليزية
            "the", "is", "are", "what", "how", "why", "when", "where", "who",
            "I", "you", "he", "she", "we", "they", "it", "this", "that", "these",
            "those", "which", "all", "some", "any", "many", "few", "much", "little",
            
            # فرنسية
            "le", "la", "est", "que", "comment", "pourquoi", "quand", "où", "qui",
            "je", "tu", "il", "elle", "nous", "vous", "ils", "ce", "cette", "ces",
            "tout", "quelque", "aucun", "plusieurs", "peu", "beaucoup", "très"
        ]
        
        # دمج كل المفردات
        all_terms = educational_terms + base_words
        current_index = len(vocab)
        
        for term in all_terms:
            if term not in vocab:
                vocab[term] = current_index
                current_index += 1
        
        # إضافة أرقام
        for i in range(10):
            vocab[str(i)] = current_index + i
        
        return vocab
    
    def preprocess_text(self, text):
        """معالجة النص بشكل فعال"""
        if not text or not text.strip():
            return [self.tokenizer["[CLS]"], self.tokenizer["[SEP]"]]
        
        words = text.split()
        tokens = [self.tokenizer["[CLS]"]]
        
        for word in words:
            # تنظيف الكلمة وإزالة الرموز غير المرغوبة
            clean_word = ''.join(c for c in word if c.isalnum() or c in [' ', '-', '_', '.', '?', '!']).strip()
            if clean_word:
                # تحويل إلى حروف صغيرة للتقليل من حجم المفردات
                clean_word_lower = clean_word.lower()
                token = self.tokenizer.get(clean_word_lower, self.tokenizer["[UNK]"])
                tokens.append(token)
        
        # تقليم النص إذا كان أطول من الطول المسموح
        max_length = self.config.max_position_embeddings - 1  # احتياطي لـ [SEP]
        if len(tokens) > max_length:
            tokens = tokens[:max_length]
        
        tokens.append(self.tokenizer["[SEP]"])
        return tokens
    
    def ask_question(self, question, target_language="ar"):
        """الوظيفة الرئيسية لطرح الأسئلة"""
        if not question or not question.strip():
            return {
                "answer": "يرجى كتابة سؤال واضح.",
                "detected_language": "unknown",
                "detected_subject": "general",
                "target_language": target_language,
                "confidence": 0.0
            }
        
        try:
            # كشف اللغة والمادة
            source_language = self.knowledge_base.detect_language(question)
            subject = self.knowledge_base.detect_subject(question, source_language)
            
            # معالجة السؤال
            tokens = self.preprocess_text(question)
            input_ids = torch.tensor([tokens])
            
            # إنشاء قناع الانتباه
            attention_mask = (input_ids != self.tokenizer["[PAD]"]).float()
            
            # تحديد لغة الإدخال
            lang_id = torch.tensor([self.knowledge_base.language_codes.get(source_language, 0)])
            
            # الحصول على تنبؤات النموذج
            with torch.no_grad():
                outputs = self.model(input_ids, attention_mask=attention_mask, language_id=lang_id)
            
            # توليد الإجابة باستخدام النظام الذكي
            answer = self.answer_generator.generate_response(
                question, subject, source_language, target_language
            )
            
            return {
                "answer": answer,
                "detected_language": source_language,
                "detected_subject": subject,
                "target_language": target_language,
                "confidence": self._calculate_confidence(outputs, question)
            }
            
        except Exception as e:
            print(f"❌ خطأ في معالجة السؤال: {e}")
            return {
                "answer": "عذراً، حدث خطأ في معالجة سؤالك. يرجى المحاولة مرة أخرى.",
                "detected_language": "unknown",
                "detected_subject": "general",
                "target_language": target_language,
                "confidence": 0.0
            }
    
    def _calculate_confidence(self, outputs, question):
        """حساب ثقة النموذج في الإجابة"""
        try:
            # حساب الثقة من تنبؤات اللغة والمادة
            lang_probs = torch.softmax(outputs['language_logits'], dim=-1)
            subject_probs = torch.softmax(outputs['subject_logits'], dim=-1)
            
            lang_confidence = torch.max(lang_probs).item()
            subject_confidence = torch.max(subject_probs).item()
            
            # متوسط مرجح للثقة
            confidence = (lang_confidence * 0.4) + (subject_confidence * 0.6)
            
            # ضبط الثقة بناءً على طول السؤال وتعقيده
            question_complexity = min(len(question.split()) / 20, 1.0)  # تعقيد بناءً على عدد الكلمات
            adjusted_confidence = confidence * (0.7 + 0.3 * question_complexity)
            
            return min(0.95, adjusted_confidence)
            
        except Exception:
            return 0.7  # ثقة افتراضية في حالة الخطأ
    
    def save_model(self, path):
        """حفظ النموذج مع التكميم لتقليل الحجم"""
        try:
            # استخدام float16 لتقليل حجم الملف
            state_dict_fp16 = {k: v.half() for k, v in self.model.state_dict().items()}
            
            torch.save({
                'model_state_dict': state_dict_fp16,
                'config': self.config,
                'tokenizer': self.tokenizer
            }, path)
            
            # حساب وحجم النموذج
            model_size = sum(p.numel() for p in self.model.parameters())
            file_size_mb = model_size * 2 / 1024 / 1024  # float16 = 2 bytes per parameter
            
            print(f"✅ تم حفظ النموذج بنجاح!")
            print(f"📊 حجم المعلمات: {model_size:,} معلمة")
            print(f"💾 الحجم التقريبي للملف: {file_size_mb:.1f} ميجابايت")
            
            return True
            
        except Exception as e:
            print(f"❌ فشل في حفظ النموذج: {e}")
            return False
    
    def load_model(self, path):
        """تحميل النموذج"""
        try:
            checkpoint = torch.load(path, map_location='cpu')
            self.model.load_state_dict(checkpoint['model_state_dict'])
            print("✅ تم تحميل النموذج بنجاح!")
        except Exception as e:
            print(f"❌ فشل في تحميل النموذج: {e}")

# دالة مساعدة للاختبار السريع
def test_polyglot_ai():
    """اختبار سريع للنموذج"""
    print("🧪 بدء اختبار النموذج التعليمي...")
    
    ai = PolyglotEducationalAI()
    
    test_questions = [
        "What is algebra?",
        "ما هي قواعد اللغة الإنجليزية؟",
        "Expliquez la grammaire française",
        "كيف أحل معادلة رياضية؟",
        "ما الفرق بين الجبر والهندسة؟"
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"❓ السؤال: {question}")
        
        result = ai.ask_question(question, "ar")
        
        print(f"🌐 اللغة المكتشفة: {result['detected_language']}")
        print(f"📚 المادة المكتشفة: {result['detected_subject']}")
        print(f"🎯 لغة الإجابة: {result['target_language']}")
        print(f"📊 مستوى الثقة: {result['confidence']:.2f}")
        print(f"💡 الإجابة:\n{result['answer']}")
    
    # حفظ النموذج
    ai.save_model("mini_polyglot_tutor.pth")

if __name__ == "__main__":
    test_polyglot_ai()
