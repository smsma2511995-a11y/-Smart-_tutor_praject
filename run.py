# run.py - بديل محسن لـ main.py
#!/usr/bin/env python3
"""
SmartTutor Pro - ملف التشغيل الرئيسي
تشغيل سريع ومباشر بدون تعقيد
"""

import os
import sys
from pathlib import Path

# إضافة المسارات
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def main():
    print("🚀 SmartTutor Pro - النظام التعليمي الذكي")
    print("=" * 50)
    
    try:
        # استيراد المكونات
        from models.polyglot_tutor import PolyglotEducationalAI
        from core.document_processor import DocumentProcessor
        
        print("✅ تم تحميل المكونات بنجاح")
        
        # اختبار سريع
        ai = PolyglotEducationalAI()
        
        print("\n🎯 جاهز للاستخدام! اختر الوضع:")
        print("1. الوضع التفاعلي (أوامر)")
        print("2. الواجهة الرسومية")
        print("3. اختبار سريع")
        
        choice = input("\nاختر (1/2/3): ").strip()
        
        if choice == "1":
            run_interactive_mode(ai)
        elif choice == "2":
            run_gui_mode()
        elif choice == "3":
            run_quick_test(ai)
        else:
            print("❌ اختيار غير صحيح")
            
    except Exception as e:
        print(f"❌ خطأ في التحميل: {e}")
        print("\n🔧 حاول تثبيت المتطلبات أولاً:")
        print("pip install -r requirements.txt")

def run_interactive_mode(ai):
    """الوضع التفاعلي"""
    print("\n🎯 الوضع التفاعلي - اكتب 'خروج' للخروج")
    print("-" * 40)
    
    while True:
        question = input("\n❓ سؤالك: ").strip()
        
        if question.lower() in ['خروج', 'exit', 'quit']:
            break
            
        if not question:
            continue
            
        print("🔄 جاري المعالجة...")
        result = ai.ask_question(question)
        
        print(f"\n💡 الإجابة:")
        print(f"📚 المادة: {result['detected_subject']}")
        print(f"🌐 اللغة: {result['detected_language']}")
        print(f"📊 الثقة: {result['confidence']:.2f}")
        print(f"\n{result['answer']}")
        print("-" * 50)

def run_gui_mode():
    """تشغيل الواجهة الرسومية"""
    try:
        from ui.kivy_interface import EnhancedTutorApp
        print("🎨 جاري تحميل الواجهة الرسومية...")
        app = EnhancedTutorApp()
        app.run()
    except Exception as e:
        print(f"❌ خطأ في تحميل الواجهة: {e}")

def run_quick_test(ai):
    """اختبار سريع للنظام"""
    print("\n🧪 اختبار سريع للنظام...")
    
    test_questions = [
        "ما هو الجبر؟",
        "What is algebra?",
        "Expliquez les mathématiques",
        "كيف أحل معادلة؟"
    ]
    
    for question in test_questions:
        print(f"\n🔍 اختبار: {question}")
        result = ai.ask_question(question)
        print(f"✅ المادة: {result['detected_subject']}")
        print(f"✅ اللغة: {result['detected_language']}")
        print(f"📝 الإجابة: {result['answer'][:100]}...")

if __name__ == "__main__":
    main()
