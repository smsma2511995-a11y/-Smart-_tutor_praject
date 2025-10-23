# ui/kivy_interface.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.core.window import Window
import threading
import os

# إعدادات النافذة
Window.size = (1000, 700)
Window.minimum_width = 800
Window.minimum_height = 600

class EnhancedTutorApp(App):
    def __init__(self):
        super().__init__()
        self.tutor = None
        self.title = "SmartTutor Pro - النظام التعليمي الذكي"
    
    def build(self):
        # التصميم الرئيسي
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # شريط العنوان
        title_bar = BoxLayout(size_hint_y=0.1, spacing=10)
        title_label = Label(
            text="🎓 SmartTutor Pro",
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        title_bar.add_widget(title_label)
        main_layout.add_widget(title_bar)
        
        # شريط التحكم
        control_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        
        # اختيار المادة
        self.subject_spinner = Spinner(
            text='جميع المواد',
            values=['جميع المواد', 'الرياضيات', 'اللغة الإنجليزية', 'اللغة الفرنسية', 'العلوم', 'العربية', 'التاريخ'],
            size_hint=(0.25, 1),
            background_color=(0.3, 0.5, 0.9, 1)
        )
        
        # زر الوضع الذكي
        self.smart_btn = Button(
            text='الوضع الذكي: ✅',
            size_hint=(0.2, 1),
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.smart_btn.bind(on_press=self.toggle_smart_mode)
        
        # زر إضافة مستند
        add_doc_btn = Button(
            text='📁 إضافة مستند',
            size_hint=(0.15, 1),
            background_color=(0.9, 0.6, 0.2, 1)
        )
        add_doc_btn.bind(on_press=self.show_file_chooser)
        
        # زر المساعدة
        help_btn = Button(
            text='❓ مساعدة',
            size_hint=(0.1, 1),
            background_color=(0.8, 0.3, 0.8, 1)
        )
        help_btn.bind(on_press=self.show_help)
        
        control_bar.add_widget(self.subject_spinner)
        control_bar.add_widget(self.smart_btn)
        control_bar.add_widget(add_doc_btn)
        control_bar.add_widget(help_btn)
        
        main_layout.add_widget(control_bar)
        
        # منطقة الإدخال
        input_section = BoxLayout(size_hint_y=0.15, spacing=10)
        
        self.question_input = TextInput(
            hint_text='اكتب سؤالك هنا...\nيدعم العربية، الإنجليزية، والفرنسية',
            multiline=True,
            size_hint=(0.8, 1),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            font_size='16sp'
        )
        
        ask_btn = Button(
            text='🔍 اسأل',
            size_hint=(0.2, 1),
            background_color=(0.2, 0.5, 0.8, 1),
            font_size='18sp',
            bold=True
        )
        ask_btn.bind(on_press=self.ask_question)
        
        input_section.add_widget(self.question_input)
        input_section.add_widget(ask_btn)
        main_layout.add_widget(input_section)
        
        # منطقة النتائج
        results_section = BoxLayout(size_hint_y=0.67)
        
        self.results_label = Label(
            text='ستظهر الإجابات هنا...\n\n💡 يمكنك سؤال النظام عن:\n• شرح المفاهيم\n• حل المسائل\n• المقارنات\n• القواعد النحوية',
            size_hint_y=1,
            text_size=(None, None),
            halign='right',
            valign='top',
            font_size='16sp',
            color=(0.3, 0.3, 0.3, 1),
            markup=True
        )
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.results_label)
        results_section.add_widget(scroll_view)
        
        main_layout.add_widget(results_section)
        
        # تهيئة النظام
        self.initialize_system()
        
        return main_layout
    
    def initialize_system(self):
        """تهيئة النظام في الخلفية"""
        def init_thread():
            from main import SmartTutorPro
            self.tutor = SmartTutorPro()
            Clock.schedule_once(lambda dt: self.show_message("✅ النظام جاهز! يمكنك البدء في الأسئلة."))
        
        threading.Thread(target=init_thread, daemon=True).start()
        self.show_message("🔄 جاري تحميل النظام...")
    
    def toggle_smart_mode(self, instance):
        """تبديل الوضع الذكي"""
        if self.tutor:
            new_state = self.tutor.toggle_smart_mode()
            if new_state:
                instance.text = 'الوضع الذكي: ✅'
                self.show_message("✅ تم تفعيل الوضع الذكي")
            else:
                instance.text = 'الوضع الذكي: ❌'
                self.show_message("⚡ تم تفعيل البحث في المستندات فقط")
    
    def ask_question(self, instance):
        """معالجة السؤال"""
        question = self.question_input.text.strip()
        if not question:
            self.show_message("⚠️ يرجى كتابة سؤال أولاً")
            return
        
        if not self.tutor:
            self.show_message("🔄 النظام لم يكتمل التحميل بعد...")
            return
        
        # تعطيل الزر أثناء المعالجة
        instance.disabled = True
        instance.text = '🔄 جاري المعالجة...'
        
        # الحصول على المادة المختارة
        subject = None
        if self.subject_spinner.text != 'جميع المواد':
            subject_map = {
                'الرياضيات': 'math',
                'اللغة الإنجليزية': 'english',
                'اللغة الفرنسية': 'french', 
                'العلوم': 'science',
                'العربية': 'arabic',
                'التاريخ': 'history'
            }
            subject = subject_map.get(self.subject_spinner.text)
        
        # تشغيل المعالجة في thread منفصل
        threading.Thread(
            target=self.process_question_thread,
            args=(question, subject, instance),
            daemon=True
        ).start()
    
    def process_question_thread(self, question, subject, button):
        """معالجة السؤال في thread منفصل"""
        try:
            result = self.tutor.process_question(question, subject, self.tutor.smart_mode)
            
            # تحديث الواجهة في thread الرئيسي
            Clock.schedule_once(lambda dt: self.display_result(result, button, question), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(f"خطأ في المعالجة: {str(e)}", button), 0)
    
    def display_result(self, result, button, question):
        """عرض النتيجة"""
        # إعادة تمكين الزر
        button.disabled = False
        button.text = '🔍 اسأل'
        
        # تنسيق النتيجة
        result_text = f"""[b][size=18]❓ السؤال:[/size][/b]
{question}

[b][size=18]💡 الإجابة:[/size][/b]
{result['answer']}

[b]📊 معلومات الإجابة:[/b]
• نوع الإجابة: {result['type']}
• المصدر: {result['source']}
• المادة: {result['subject']}
• مستوى الثقة: {result['confidence']:.2f}

{'🎯' * 20}
"""
        
        self.results_label.text = result_text
    
    def show_file_chooser(self, instance):
        """عرض نافذة اختيار الملف"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        file_chooser = FileChooserListView(
            size_hint=(1, 0.8),
            filters=['*.pdf', '*.txt', '*.docx']
        )
        
        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        select_btn = Button(text='اختيار')
        cancel_btn = Button(text='إلغاء')
        
        def add_document(path):
            if file_chooser.selection:
                selected_file = file_chooser.selection[0]
                subject = self.subject_spinner.text
                if subject == 'جميع المواد':
                    subject = 'general'
                
                success, message = self.tutor.add_document(selected_file, subject)
                if success:
                    self.show_message(f"✅ {message}")
                else:
                    self.show_message(f"❌ {message}")
                
                popup.dismiss()
        
        select_btn.bind(on_press=lambda x: add_document(file_chooser.selection))
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        buttons_layout.add_widget(select_btn)
        buttons_layout.add_widget(cancel_btn)
        
        content.add_widget(file_chooser)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='اختر ملف لإضافته (PDF, TXT, DOCX)',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def show_help(self, instance):
        """عرض نافذة المساعدة"""
        help_text = """
🎓 [b]SmartTutor Pro - دليل الاستخدام[/b]

[b]💡 المميزات:[/b]
• دعم متعدد اللغات (عربي، إنجليزي، فرنسي)
• شرح المفاهيم التعليمية
• البحث في المستندات المضافة
• وضع ذكي متقدم

[b]🎯 أنواع الأسئلة المدعومة:[/b]
• "ما هو الجبر؟" - شرح المفاهيم
• "كيف أحل معادلة؟" - خطوات الحل  
• "قارن بين الجبر والهندسة" - المقارنات
• "What is algebra?" - أسئلة بالإنجليزية
• "Expliquez la grammaire" - أسئلة بالفرنسية

[b]📁 إضافة المستندات:[/b]
• اضغط على "إضافة مستند"
• اختر ملف PDF أو نصي
• اختر المادة المناسبة

[b]⚙️ الإعدادات:[/b]
• الوضع الذكي: يستخدم النموذج المصغر للإجابات الذكية
• البحث في المستندات: يبحث في المستندات المضافة فقط
"""
        
        content = BoxLayout(orientation='vertical', padding=20)
        help_label = Label(
            text=help_text,
            text_size=(None, None),
            halign='right',
            valign='top',
            markup=True
        )
        
        scroll = ScrollView()
        scroll.add_widget(help_label)
        content.add_widget(scroll)
        
        close_btn = Button(text='إغلاق', size_hint_y=0.1)
        popup = Popup(title='مساعدة', content=content, size_hint=(0.8, 0.8))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()
    
    def show_message(self, message):
        """عرض رسالة"""
        self.results_label.text = f"[size=18][b]{message}[/b][/size]"
    
    def show_error(self, error_message, button):
        """عرض خطأ"""
        button.disabled = False
        button.text = '🔍 اسأل'
        self.show_message(f"❌ {error_message}")

def main():
    """الدالة الرئيسية للتشغيل"""
    EnhancedTutorApp().run()

if __name__ == '__main__':
    main()
