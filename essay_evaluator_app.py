# essay_evaluator_app.py (واجهة Gradio لتقييم المقالات)

import gradio as gr
# يجب أن يكون ملف writing_assistant.py في نفس المجلد
from writing_assistant import AdvancedEssayEvaluator 

# تهيئة مقيّم المقالات
evaluator = AdvancedEssayEvaluator()

LANGUAGES = {"arabic": "العربية", "english": "الإنجليزية", "french": "الفرنسية"}
LEVELS = ["beginner", "intermediate", "advanced"]

def get_prompts(level, language, category="عام"):
    """توليد مواضيع كتابة (Prompts)"""
    # نستخدم دالة generate_writing_prompts من الكلاس
    prompts = evaluator.generate_writing_prompts(level, language, category)
    if not prompts:
        return "لا تتوفر مواضيع حالياً لهذا المستوى/اللغة.", ""
    
    first_prompt = prompts[0]
    prompt_text = (
        f"**الموضوع:** {first_prompt['topic']}\n"
        f"**التعليمات:** {first_prompt['instructions']}\n"
        f"**الهدف:** {first_prompt['word_target']} كلمة\n"
        f"**الهيكل المقترح:** {', '.join(first_prompt['suggested_structure'])}"
    )
    return prompt_text, first_prompt['topic']

def evaluate_essay_ui(essay_text, language_name, topic, student_level_name):
    """دالة الواجهة لتقييم المقال"""
    if not essay_text or not topic:
        return "⚠️ الرجاء كتابة المقال وتحديد الموضوع.", "", ""
    
    # تحويل لغة العرض إلى كود داخلي
    lang_code = next((k for k, v in LANGUAGES.items() if v == language_name), 'arabic')
    level_code = next((k for k in LEVELS if k.startswith(student_level_name[:3].lower())), 'intermediate')

    try:
        evaluation = evaluator.evaluate_essay(
            essay_text=essay_text,
            language=lang_code,
            topic=topic,
            student_level=level_code
        )
        
        # تنسيق ملخص التقييم
        summary = (
            f"## 🎉 ملخص التقييم الشامل - {evaluation['overall_evaluation']['grade']} \n"
            f"**الدرجة:** {evaluation['overall_evaluation']['overall_score']:.1f} / 10\n"
            f"**نقاط القوة:** {', '.join(evaluation['overall_evaluation']['strengths'])}\n"
            f"**مجالات التحسين:** {', '.join(evaluation['overall_evaluation']['areas_for_improvement'])}\n"
        )
        
        # تنسيق التغذية الراجعة التفصيلية
        detailed_feedback = "## 📝 التغذية الراجعة المفصلة\n"
        for fb in evaluation['detailed_feedback']:
            detailed_feedback += f"**{fb['aspect']} ({fb['type']}):** {fb['message']} "
            if fb.get('suggestions'):
                detailed_feedback += f"**(اقتراحات: {', '.join(fb['suggestions'])})**\n"
            else:
                detailed_feedback += "\n"
        
        # تنسيق اقتراحات التحسين الشاملة
        improvement_suggestions = "## 💡 خطة التحسين\n"
        for item in evaluation['improvement_suggestions']:
            improvement_suggestions += (
                f"**التركيز:** {item['area']}\n"
                f"**اقتراح عملي:** {item['suggestion']}\n"
                f"**المصادر:** {', '.join(item['resources'])}\n\n"
            )
            
        return summary, detailed_feedback, improvement_suggestions
    
    except Exception as e:
        return f"❌ خطأ في عملية التقييم: {str(e)}", "", ""

# واجهة Gradio
with gr.Blocks(title="مقيّم المقالات المتقدم") as app_eval:
    gr.Markdown("## ✍️ مقيّم المقالات المتقدم للغات المختلفة")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ الإعدادات")
            
            lang_select = gr.Dropdown(
                label="اختر اللغة", 
                choices=list(LANGUAGES.values()), 
                value='العربية'
            )
            level_select = gr.Dropdown(
                label="اختر مستوى الطالب", 
                choices=['مبتدئ', 'متوسط', 'متقدم'], 
                value='متوسط'
            )
            topic_input = gr.Textbox(label="موضوع المقال (للتحديد)")

            btn_get_prompt = gr.Button("توليد موضوع مقترح")
            prompt_output = gr.Markdown(label="الموضوع المقترح")
            
            btn_get_prompt.click(
                get_prompts, 
                inputs=[level_select, lang_select, gr.State("عام")], # استخدام حالة ثابتة مؤقتاً للتصنيف
                outputs=[prompt_output, topic_input]
            )

        with gr.Column(scale=2):
            gr.Markdown("### 📝 اكتب مقالك هنا")
            essay_input = gr.Textbox(
                label="المقال", 
                lines=15, 
                placeholder="ابدأ بكتابة مقالك هنا..."
            )
            btn_evaluate = gr.Button("📈 تقييم المقال", variant="primary")

    with gr.Row():
        summary_output = gr.Markdown(label="ملخص التقييم")
        
    with gr.Row():
        feedback_output = gr.Markdown(label="التغذية الراجعة التفصيلية")
        
    with gr.Row():
        suggestions_output = gr.Markdown(label="خطة التحسين")
        
    btn_evaluate.click(
        evaluate_essay_ui, 
        inputs=[essay_input, lang_select, topic_input, level_select], 
        outputs=[summary_output, feedback_output, suggestions_output]
    )

# app_eval.launch()
