# utils/helpers.py
import re
import json
import logging
from typing import List, Dict, Any
from pathlib import Path

def setup_logging():
    """إعداد نظام التسجيل"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('smarttutor.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def safe_filename(text: str, max_length: int = 120) -> str:
    """إنشاء اسم ملف آمن من النص"""
    # إزالة الرموز غير الآمنة
    safe_text = re.sub(r'[^\w\s\-_.]', '_', text)
    # إزالة المسافات الزائدة
    safe_text = re.sub(r'\s+', '_', safe_text)
    # تقليل الطول
    return safe_text[:max_length]

def load_json(file_path: Path) -> Dict[str, Any]:
    """تحميل ملف JSON مع معالجة الأخطاء"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"خطأ في تحميل {file_path}: {e}")
        return {}

def save_json(data: Dict[str, Any], file_path: Path) -> bool:
    """حفظ بيانات إلى ملف JSON"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logging.error(f"خطأ في حفظ {file_path}: {e}")
        return False

def format_confidence(confidence: float) -> str:
    """تنسيق مستوى الثقة"""
    if confidence > 0.8:
        return "🟢 عالي"
    elif confidence > 0.5:
        return "🟡 متوسط"
    else:
        return "🔴 منخفض"

def clean_text(text: str) -> str:
    """تنظيف النص وإزالة الرموز غير المرغوبة"""
    if not text:
        return ""
    
    # إزالة الرموز الخاصة
    cleaned = re.sub(r'[^\w\s\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\.\?\!\,]', '', text)
    # إزالة المسافات الزائدة
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def detect_file_type(file_path: Path) -> str:
    """كشف نوع الملف"""
    extensions = {
        '.pdf': 'pdf',
        '.txt': 'text',
        '.docx': 'word',
        '.doc': 'word'
    }
    return extensions.get(file_path.suffix.lower(), 'unknown')
