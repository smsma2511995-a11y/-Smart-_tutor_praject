# core/document_processor.py
import os
import sqlite3
import json
import re
import time
from pathlib import Path
from threading import Thread
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Tuple

try:
    import fitz  # PyMuPDF
except ImportError:
    print("⚠️ تنبيه: PyMuPDF غير مثبت. سيتم تعطيل معالجة PDF.")
    fitz = None

import requests
from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class DocumentProcessor:
    def __init__(self, base_dir: str = "smarttutor_data"):
        self.base_dir = Path(base_dir)
        self.setup_directories()
        
        # إعداد النموذج للتضمينات
        self.model_name = "all-MiniLM-L6-v2"
        self.model = SentenceTransformer(self.model_name)
        
        # إعدادات
        self.chunk_size = 400
        self.chunk_overlap = 50
        self.top_k = 5
        self.online_enabled = True
        
        # التخزين في الذاكرة
        self.ram_embs = {}
        self.ram_chunks = {}
        self.ram_knowledge = {}
        
        print("✅ تم تهيئة معالج المستندات بنجاح")
    
    def setup_directories(self):
        """إنشاء المجلدات اللازمة"""
        dirs = [
            self.base_dir / "books",
            self.base_dir / "embeddings", 
            self.base_dir / "knowledge",
            self.base_dir / "database"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.base_dir / "database" / "metadata.db"
        self.init_database()
    
    def init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, path TEXT, subject TEXT,
                num_chunks INTEGER, emb_file TEXT, chunks_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS qna (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT, answer TEXT, subject TEXT,
                confidence REAL, meta TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """استخراج النص من ملف PDF"""
        if fitz is None:
            return ""
        
        try:
            doc = fitz.open(pdf_path)
            text_parts = []
            
            for page in doc:
                try:
                    text = page.get_text()
                    if text.strip():
                        text_parts.append(text)
                except Exception:
                    continue
            
            doc.close()
            return "\n".join(text_parts)
            
        except Exception as e:
            print(f"❌ خطأ في استخراج النص من PDF: {e}")
            return ""
    
    def read_text_file(self, file_path: str) -> str:
        """قراءة ملف نصي"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print(f"❌ خطأ في قراءة الملف النصي: {e}")
                return ""
        except Exception as e:
            print(f"❌ خطأ في قراءة الملف: {e}")
            return ""
    
    def chunk_text(self, text: str, size: int = None, overlap: int = None) -> List[str]:
        """تقسيم النص إلى أجزاء"""
        if not text:
            return []
        
        size = size or self.chunk_size
        overlap = overlap or self.chunk_overlap
        
        text = text.replace('\r', '').strip()
        chunks = []
        i = 0
        text_length = len(text)
        
        while i < text_length:
            end = min(i + size, text_length)
            chunk = text[i:end].strip()
            
            if len(chunk) > 30:  # تجاهل القطع القصيرة جداً
                chunks.append(chunk)
            
            i = max(end - overlap, end)
            if i == end:  # تجنب التكرار اللانهائي
                break
        
        return chunks
    
    def safe_filename(self, text: str) -> str:
        """إنشاء اسم ملف آمن"""
        safe = re.sub(r'[^\w\s\-_.]', '_', text)
        return safe[:120]
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """إنشاء تضمينات للنصوص"""
        if not texts:
            return np.array([])
        
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.astype(np.float32)
    
    def add_document(self, file_path: str, subject: str = "general") -> Tuple[bool, str]:
        """إضافة مستند جديد للنظام"""
        file_path = Path(file_path)
        if not file_path.exists():
            return False, "الملف غير موجود"
        
        # استخراج النص بناءً على نوع الملف
        if file_path.suffix.lower() == '.pdf':
            text = self.extract_text_from_pdf(str(file_path))
        else:
            text = self.read_text_file(str(file_path))
        
        if not text.strip():
            return False, "لا يمكن استخراج نص من الملف"
        
        # تقسيم النص إلى أجزاء
        chunks = self.chunk_text(text)
        if not chunks:
            return False, "لا يمكن تقسيم النص إلى أجزاء مناسبة"
        
        # إنشاء التضمينات
        embeddings = self.embed_texts(chunks)
        
        # حفظ البيانات
        title = self.safe_filename(file_path.stem)
        
        # حفظ في الذاكرة
        self.ram_embs[title] = embeddings
        self.ram_chunks[title] = chunks
        
        # حفظ في قاعدة البيانات
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO books (title, path, subject, num_chunks)
            VALUES (?, ?, ?, ?)
        ''', (title, str(file_path), subject, len(chunks)))
        
        conn.commit()
        conn.close()
        
        # استخراج المفاهيم
        self.extract_and_save_concepts(chunks, subject, title)
        
        return True, f"تمت إضافة المستند: {title} ({len(chunks)} جزء)"
    
    def extract_and_save_concepts(self, chunks: List[str], subject: str, source: str):
        """استخراج وحفظ المفاهيم من النص"""
        # أخذ عينة من القطع للتحليل
        sample_chunks = chunks[:min(20, len(chunks))]
        sample_text = "\n".join(sample_chunks)
        
        # استخراج الجمل المرشحة كلمفات
        sentences = re.split(r'[.\n!?؛؟]+', sample_text)
        candidates = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            words = sentence.split()
            if 3 <= len(words) <= 25:  # جمل معقولة الطول
                candidates.append(sentence[:200])  # تقليل الطول
        
        # إزالة التكرارات
        unique_candidates = list(set(candidates))
        
        # حفظ المفاهيم
        if subject not in self.ram_knowledge:
            self.ram_knowledge[subject] = {}
        
        for concept in unique_candidates:
            if concept not in self.ram_knowledge[subject]:
                self.ram_knowledge[subject][concept] = {
                    "explain": concept,
                    "weight": 1,
                    "sources": [source]
                }
            else:
                self.ram_knowledge[subject][concept]["weight"] += 1
                if source not in self.ram_knowledge[subject][concept]["sources"]:
                    self.ram_knowledge[subject][concept]["sources"].append(source)
    
    def search_documents(self, question: str, subject: str = None, top_k: int = None) -> List[Dict]:
        """البحث في المستندات عن إجابة للسؤال"""
        top_k = top_k or self.top_k
        
        # تضمين السؤال
        question_embedding = self.model.encode([question], convert_to_numpy=True)
        
        results = []
        
        # البحث في القطع المخزنة
        for title, embeddings in self.ram_embs.items():
            if embeddings.shape[0] == 0:
                continue
            
            # حساب التشابه
            similarities = cosine_similarity(question_embedding, embeddings)[0]
            
            # الحصول على أفضل النتائج
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            for idx in top_indices:
                if idx < len(self.ram_chunks[title]):
                    results.append({
                        'type': 'document',
                        'title': title,
                        'subject': subject or 'general',
                        'score': float(similarities[idx]),
                        'content': self.ram_chunks[title][idx],
                        'source': 'document_corpus'
                    })
        
        # البحث في قاعدة المعرفة
        if subject and subject in self.ram_knowledge:
            knowledge_items = list(self.ram_knowledge[subject].items())
            if knowledge_items:
                concepts = [item[0] for item in knowledge_items]
                concept_embeddings = self.model.encode(concepts, convert_to_numpy=True)
                
                concept_similarities = cosine_similarity(question_embedding, concept_embeddings)[0]
                top_concept_indices = np.argsort(concept_similarities)[::-1][:top_k]
                
                for idx in top_concept_indices:
                    concept, data = knowledge_items[idx]
                    results.append({
                        'type': 'concept',
                        'title': concept,
                        'subject': subject,
                        'score': float(concept_similarities[idx]),
                        'content': data['explain'],
                        'source': 'knowledge_base'
                    })
        
        # ترتيب النتائج حسب التشابه
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def fetch_web_content(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """جلب محتوى من الويب"""
        if not self.online_enabled:
            return None, "الوضع الأونلاين معطل"
        
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "SmartTutor/1.0"})
            if response.status_code != 200:
                return None, f"خطأ في جلب المحتوى: {response.status_code}"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # استخراج العنوان
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "محتوى ويب"
            
            # استخراج المحتوى الرئيسي
            article = soup.find('article')
            if article:
                content = article.get_text(separator='\n')
            else:
                # محاولة استخراج من الفقرات
                paragraphs = soup.find_all('p')
                content = '\n'.join([p.get_text() for p in paragraphs if p.get_text().strip()])
            
            if not content.strip():
                return None, "لا يوجد محتوى نصي في الصفحة"
            
            return content, title
            
        except Exception as e:
            return None, f"خطأ في جلب المحتوى: {e}"

# اختبار النظام
def test_document_processor():
    """اختبار نظام معالجة المستندات"""
    print("🧪 اختبار معالجة المستندات...")
    
    processor = DocumentProcessor()
    
    # اختبار إضافة مستند نصي بسيط
    test_content = """
    الجبر هو فرع من فروع الرياضيات الذي يتعامل مع الرموز والمتغيرات.
    في الجبر، نستخدم الحروف لتمثيل الأعداد المجهولة.
    المعادلة الأساسية في الجبر هي: س + ٢ = ٥، حيث س = ٣.
    
    الهندسة تدرس الأشكال والفضاء والعلاقات بينهما.
    من الأشكال الأساسية في الهندسة: المربع، والمستطيل، والمثلث.
    """
    
    # حفظ محتوى الاختبار في ملف
    test_file = "test_document.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # إضافة المستند
    success, message = processor.add_document(test_file, "math")
    print(f"نتيجة الإضافة: {message}")
    
    if success:
        # اختبار البحث
        results = processor.search_documents("ما هو الجبر؟", "math")
        print(f"عدد النتائج: {len(results)}")
        
        for i, result in enumerate(results, 1):
            print(f"نتيجة {i}: {result['content'][:100]}...")
    
    # تنظيف
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_document_processor()
