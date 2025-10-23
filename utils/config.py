# utils/config.py
import os
from pathlib import Path

class Config:
    """إعدادات التطبيق"""
    
    # المسارات
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    CORE_DIR = BASE_DIR / "core"
    UI_DIR = BASE_DIR / "ui"
    
    # إعدادات النموذج
    MODEL_CONFIG = {
        "vocab_size": 20000,
        "hidden_size": 128,
        "num_layers": 4,
        "num_heads": 4,
        "max_length": 256
    }
    
    # إعدادات المعالجة
    PROCESSING_CONFIG = {
        "chunk_size": 400,
        "chunk_overlap": 50,
        "top_k": 5,
        "min_confidence": 0.3
    }
    
    # اللغات المدعومة
    SUPPORTED_LANGUAGES = ["ar", "en", "fr"]
    
    # المواد المدعومة
    SUPPORTED_SUBJECTS = [
        "math", "science", "english", "french", "arabic",
        "physics", "chemistry", "history", "geography"
    ]
    
    @classmethod
    def setup_directories(cls):
        """إنشاء المجلدات اللازمة"""
        directories = [
            cls.DATA_DIR / "books",
            cls.DATA_DIR / "knowledge",
            cls.DATA_DIR / "embeddings",
            cls.DATA_DIR / "temp"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("✅ تم إنشاء الهيكل التنظيمي")

# تطبيق الإعدادات
Config.setup_directories()
