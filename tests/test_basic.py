# tests/test_basic.py
import unittest
import sys
import os
from pathlib import Path

# إضافة المسار الرئيسي
sys.path.append(str(Path(__file__).parent.parent))

class TestBasicFunctionality(unittest.TestCase):
    
    def setUp(self):
        """تهيئة قبل كل اختبار"""
        from models.polyglot_tutor import PolyglotEducationalAI
        self.ai = PolyglotEducationalAI()
    
    def test_language_detection(self):
        """اختبار كشف اللغة"""
        test_cases = [
            ("ما هو الجبر؟", "ar"),
            ("What is algebra?", "en"),
            ("Qu'est-ce que l'algèbre?", "fr")
        ]
        
        for text, expected_lang in test_cases:
            with self.subTest(text=text):
                result = self.ai.ask_question(text)
                self.assertEqual(result['detected_language'], expected_lang)
    
    def test_subject_detection(self):
        """اختبار كشف المادة"""
        test_cases = [
            ("ما هو الجبر؟", "math"),
            ("كيف أتعلم الإنجليزية؟", "english"),
            ("شرح القواعد الفرنسية", "french")
        ]
        
        for text, expected_subject in test_cases:
            with self.subTest(text=text):
                result = self.ai.ask_question(text)
                self.assertEqual(result['detected_subject'], expected_subject)
    
    def test_response_generation(self):
        """اختبار توليد الإجابة"""
        questions = [
            "ما هو الجبر؟",
            "What is mathematics?",
            "Expliquez les maths"
        ]
        
        for question in questions:
            with self.subTest(question=question):
                result = self.ai.ask_question(question)
                self.assertIsInstance(result, dict)
                self.assertIn('answer', result)
                self.assertIn('confidence', result)
                self.assertGreater(len(result['answer']), 10)

class TestDocumentProcessor(unittest.TestCase):
    
    def setUp(self):
        from core.document_processor import DocumentProcessor
        self.processor = DocumentProcessor()
    
    def test_text_chunking(self):
        """اختبار تقسيم النص"""
        test_text = "هذا نص طويل يحتاج إلى تقسيم إلى أجزاء أصغر. كل جزء يجب أن يكون مناسباً للمعالجة."
        
        chunks = self.processor.chunk_text(test_text, size=20, overlap=5)
        
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)
        
        for chunk in chunks:
            self.assertIsInstance(chunk, str)
            self.assertGreater(len(chunk), 0)

if __name__ == '__main__':
    unittest.main()
