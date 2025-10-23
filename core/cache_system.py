# core/cache_system.py
import pickle
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

class SmartCache:
    def __init__(self, cache_dir="data/cache", max_size_mb=100, ttl_hours=24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_size = max_size_mb * 1024 * 1024  # تحويل إلى بايت
        self.ttl = timedelta(hours=ttl_hours)
        
        self.clean_expired()
    
    def get_cache_key(self, question: str, subject: str = None) -> str:
        """إنشاء مفتاح فريد للسؤال"""
        content = f"{question}_{subject}" if subject else question
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get(self, question: str, subject: str = None):
        """استرجاع الإجابة من التخزين المؤقت"""
        cache_key = self.get_cache_key(question, subject)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)
            
            # فحص انتهاء الصلاحية
            if datetime.now() - cached_data['timestamp'] > self.ttl:
                cache_file.unlink()  # حذف الملف المنتهي
                return None
            
            return cached_data['answer']
        except:
            return None
    
    def set(self, question: str, answer: dict, subject: str = None):
        """حفظ الإجابة في التخزين المؤقت"""
        cache_key = self.get_cache_key(question, subject)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        cache_data = {
            'question': question,
            'subject': subject,
            'answer': answer,
            'timestamp': datetime.now()
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            
            # التحكم في حجم التخزين المؤقت
            self.manage_cache_size()
            
            return True
        except Exception as e:
            print(f"❌ فشل حفظ التخزين المؤقت: {e}")
            return False
    
    def manage_cache_size(self):
        """إدارة حجم التخزين المؤقت"""
        cache_files = list(self.cache_dir.glob("*.pkl"))
        
        if not cache_files:
            return
        
        # حساب الحجم الكلي
        total_size = sum(f.stat().st_size for f in cache_files)
        
        if total_size > self.max_size:
            # حذف الملفات الأقدم
            cache_files_sorted = sorted(cache_files, key=lambda f: f.stat().st_mtime)
            files_to_delete = cache_files_sorted[:len(cache_files_sorted) // 4]  # حذف 25% الأقدم
            
            for file in files_to_delete:
                file.unlink()
            
            print(f"🧹 تم تنظيف التخزين المؤقت، حذف {len(files_to_delete)} ملف")
    
    def clean_expired(self):
        """تنظيف الملفات المنتهية الصلاحية"""
        cache_files = list(self.cache_dir.glob("*.pkl"))
        now = datetime.now()
        expired_count = 0
        
        for cache_file in cache_files:
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                if now - cached_data['timestamp'] > self.ttl:
                    cache_file.unlink()
                    expired_count += 1
            except:
                cache_file.unlink()  # حذف الملف التالف
        
        if expired_count > 0:
            print(f"🧹 تم تنظيف {expired_count} ملف منتهي الصلاحية")
    
    def get_stats(self):
        """إحصائيات التخزين المؤقت"""
        cache_files = list(self.cache_dir.glob("*.pkl"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "total_files": len(cache_files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "hit_rate": self.calculate_hit_rate()
        }
