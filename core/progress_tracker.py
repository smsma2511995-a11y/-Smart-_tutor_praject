# core/progress_tracker.py
import json
from datetime import datetime, timedelta
from pathlib import Path

class ProgressTracker:
    def __init__(self):
        self.progress_file = Path("data/progress.json")
        self.progress_file.parent.mkdir(exist_ok=True)
        self.load_progress()
    
    def load_progress(self):
        """تحميل بيانات التقدم"""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                self.progress = json.load(f)
        except:
            self.progress = {
                "subjects": {},
                "daily_streak": 0,
                "last_activity": None,
                "total_questions": 0,
                "achievements": []
            }
    
    def record_activity(self, subject: str, question_type: str, confidence: float):
        """تسجيل نشاط المستخدم"""
        today = datetime.now().date().isoformat()
        
        # تحديث المادة
        if subject not in self.progress["subjects"]:
            self.progress["subjects"][subject] = {
                "questions_asked": 0,
                "average_confidence": 0,
                "last_activity": today
            }
        
        subject_data = self.progress["subjects"][subject]
        subject_data["questions_asked"] += 1
        subject_data["average_confidence"] = (
            (subject_data["average_confidence"] * (subject_data["questions_asked"] - 1) + confidence) 
            / subject_data["questions_asked"]
        )
        subject_data["last_activity"] = today
        
        # تحديد التسلسل اليومي
        if self.progress["last_activity"] != today:
            last_activity = datetime.fromisoformat(self.progress["last_activity"]).date() if self.progress["last_activity"] else None
            today_date = datetime.now().date()
            
            if last_activity and (today_date - last_activity).days == 1:
                self.progress["daily_streak"] += 1
            elif not last_activity or (today_date - last_activity).days > 1:
                self.progress["daily_streak"] = 1
            
            self.progress["last_activity"] = today
        
        self.progress["total_questions"] += 1
        
        # فحص الإنجازات
        self.check_achievements()
        
        self.save_progress()
    
    def check_achievements(self):
        """فحص الإنجازات المحققة"""
        achievements = [
            {
                "id": "first_question",
                "name": "السؤال الأول",
                "description": "طرح أول سؤال",
                "condition": lambda p: p["total_questions"] >= 1,
                "unlocked": False
            },
            {
                "id": "question_master",
                "name": "سيد الأسئلة", 
                "description": "طرح 50 سؤال",
                "condition": lambda p: p["total_questions"] >= 50,
                "unlocked": False
            },
            {
                "id": "week_streak",
                "name": "مثابر أسبوعي",
                "description": "7 أيام متتالية من النشاط",
                "condition": lambda p: p["daily_streak"] >= 7,
                "unlocked": False
            }
        ]
        
        for achievement in achievements:
            if (achievement["id"] not in self.progress["achievements"] and 
                achievement["condition"](self.progress)):
                self.progress["achievements"].append(achievement["id"])
                print(f"🎉 إنجاز مفتوح: {achievement['name']}!")
    
    def get_progress_report(self):
        """تقرير مفصل عن التقدم"""
        total_subjects = len(self.progress["subjects"])
        favorite_subject = max(
            self.progress["subjects"].items(), 
            key=lambda x: x[1]["questions_asked"]
        )[0] if total_subjects > 0 else "لا يوجد"
        
        return {
            "total_questions": self.progress["total_questions"],
            "daily_streak": self.progress["daily_streak"],
            "subjects_studied": total_subjects,
            "favorite_subject": favorite_subject,
            "achievements_count": len(self.progress["achievements"]),
            "subjects_detail": self.progress["subjects"]
        }
    
    def save_progress(self):
        """حفظ بيانات التقدم"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
