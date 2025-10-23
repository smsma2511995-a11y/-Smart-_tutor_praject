# core/notification_system.py
import schedule
import time
from threading import Thread
from datetime import datetime

class NotificationSystem:
    def __init__(self, progress_tracker):
        self.progress_tracker = progress_tracker
        self.running = False
        
    def start_daily_reminder(self):
        """بدء التذكيرات اليومية"""
        schedule.every().day.at("18:00").do(self.send_daily_reminder)
        schedule.every().hour().do(self.check_achievements)
        
        self.running = True
        reminder_thread = Thread(target=self.run_scheduler, daemon=True)
        reminder_thread.start()
    
    def run_scheduler(self):
        """تشغيل المجدول في الخلفية"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)
    
    def send_daily_reminder(self):
        """إرسال تذكير يومي"""
        progress = self.progress_tracker.get_progress_report()
        
        if progress["daily_streak"] > 0:
            message = f"🔔 حافظ على تسلسلك! لديك {progress['daily_streak']} يوم متتالي"
        else:
            message = "🔔 وقت المذاكرة! هل لديك سؤال اليوم؟"
        
        print(f"📢 إشعار: {message}")
        # يمكن إرسالها كإشعار في الواجهة
    
    def check_achievements(self):
        """فحص الإنجازات الجديدة"""
        # تنبيه بالإنجازات التي على وشك التحقق
        progress = self.progress_tracker.get_progress_report()
        
        if progress["total_questions"] == 49:
            print("🎯 أنت على بعد سؤال واحد من إنجاز 'سيد الأسئلة'!")
