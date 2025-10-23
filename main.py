# main.py
#!/usr/bin/env python3
"""
SmartTutor Pro - النظام التعليمي الذكي المتكامل
إصدار متعدد اللغات بحجم مصغر (20 ميجا)
"""

import os
import sys
from pathlib import Path

# إضافة المسارات للمكتبات
sys.path.append(str(Path(__file__).parent))

from models.polyglot_tutor import PolyglotEducationalAI
from core.document_processor import DocumentProcessor
from ui.kivy_interface import EnhancedTutorApp

class SmartTutorPro:
    """النظام التعليمي الذكي المتكامل"""
    
    def __init__(self):
        self.ai_model = PolyglotEducationalAI()
        self.doc_processor = DocumentProcessor()
        self.smart_mode = True
        
        print("🚀 تم تحميل SmartTutor Pro بنجاح!")
        print("📚 النظام جاهز للتعلم متعدد اللغات")
    
    def process_question(self, question: str, subject: str = None, use_smart_ai: bool = True):
        """معالجة السؤال باستخدام النظام المدمج"""
        
        # استخدام النموذج الذكي إذا كان مفعلاً
        if use_smart_ai and self.smart_mode:
            try:
                smart_result = self.ai_model.ask_question(question)
                
                if smart_result.get('confidence', 0) > 0.6:
                    return {
                        'type': 'smart_ai',
                        'answer': smart_result['answer'],
                        'confidence': smart_result['confidence'],
                        'subject': smart_result['detected_subject'],
                        'language': smart_result['detected_language'],
                        'source': 'polyglot_ai'
                    }
            except Exception as e:
                print(f"⚠️ النموذج الذكي غير متاح: {e}")
        
        # البحث في المستندات
        doc_results = self.doc_processor.search_documents(question, subject)
        if doc_results:
            best_result = doc_results[0]
            return {
                'type': 'document_search',
                'answer': best_result['content'],
                'confidence': best_result['score'],
                'subject': best_result.get('subject', subject or 'general'),
                'source': 'document_corpus'
            }
        
        # الإجابة الافتراضية
        return {
            'type': 'fallback',
            'answer': "أحتاج إلى مزيد من المعلومات للإجابة على سؤالك. يمكنك:\n• توضيح سؤالك\n• إضافة مواد تعليمية\n• تغيير صيغة السؤال",
            'confidence': 0.1,
            'subject': subject or 'general',
            'source': 'fallback'
        }
    
    def add_document(self, file_path: str, subject: str = "general"):
        """إضافة مستند جديد"""
        return self.doc_processor.add_document(file_path, subject)
    
    def toggle_smart_mode(self):
        """تبديل الوضع الذكي"""
        self.smart_mode = not self.smart_mode
        return self.smart_mode

def run_cli_demo():
    """تشغيل نسخة CLI للاختبار"""
    print("🎯 SmartTutor Pro - الوضع التفاعلي")
    print("=" * 50)
    
    tutor = SmartTutorPro()
    
    while True:
        print("\n" + "="*50)
        question = input("❓ اكتب سؤالك (أو 'exit' للخروج): ").strip()
        
        if question.lower() in ['exit', 'quit', 'خروج']:
            break
        
        if not question:
            continue
        
        print("🔄 جاري المعالجة...")
        result = tutor.process_question(question)
        
        print(f"\n💡 الإجابة ({result['type']}):")
        print(f"📚 المادة: {result['subject']}")
        print(f"📊 الثقة: {result['confidence']:.2f}")
        print(f"🔍 المصدر: {result['source']}")
        print(f"\n{result['answer']}")

def run_gui():
    """تشغيل الواجهة الرسومية"""
    app = EnhancedTutorApp()
    app.run()

if __name__ == "__main__":
    print("🎓 SmartTutor Pro - النظام التعليمي الذكي")
    print("1. الوضع التفاعلي (CLI)")
    print("2. الواجهة الرسومية (GUI)")
    
    choice = input("اختر الوضع (1 أو 2): ").strip()
    
    if choice == "1":
        run_cli_demo()
    else:
        run_gui()
