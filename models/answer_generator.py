# models/answer_generator.py
class SmartAnswerGenerator:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.templates = self._load_smart_templates()
        self.examples = self._load_examples()
    
    def _load_smart_templates(self):
        return {
            "explanation": {
                "ar": """📚 **شرح {concept}**

{explanation_ar}

💡 **مثال توضيحي:**
{example_ar}

🎯 **التطبيق العملي:**
{application_ar}""",

                "en": """📚 **Explanation of {concept}**

{explanation_en}

💡 **Example:**
{example_en}

🎯 **Practical Application:**
{application_en}""",

                "fr": """📚 **Explication de {concept}**

{explanation_fr}

💡 **Exemple:**
{example_fr}

🎯 **Application Pratique:**
{application_fr}"""
            },
            
            "comparison": {
                "ar": """🔄 **المقارنة بين {concept1} و {concept2}**

{comparison_ar}

📊 **الفرق الرئيسي:**
{difference_ar}

💡 **مثال للمقارنة:**
{example_ar}""",

                "en": """🔄 **Comparison between {concept1} and {concept2}**

{comparison_en}

📊 **Main Difference:**
{difference_en}

💡 **Comparison Example:**
{example_en}""",

                "fr": """🔄 **Comparaison entre {concept1} et {concept2}**

{comparison_fr}

📊 **Différence Principale:**
{difference_fr}

💡 **Exemple de Comparaison:**
{example_fr}"""
            },
            
            "step_by_step": {
                "ar": """🎯 **خطوات الحل:**

{steps_ar}

📝 **الشرح التفصيلي:**
{explanation_ar}

💡 **نصيحة مهمة:**
{tip_ar}""",

                "en": """🎯 **Solution Steps:**

{steps_en}

📝 **Detailed Explanation:**
{explanation_en}

💡 **Important Tip:**
{tip_en}""",

                "fr": """🎯 **Étapes de Résolution:**

{steps_fr}

📝 **Explication Détaillée:**
{explanation_fr}

💡 **Conseil Important:**
{tip_fr}"""
            },
            
            "general": {
                "ar": """🤔 **سؤالك عن {subject_ar}**

{answer_ar}

📚 **لمزيد من التعلم:**
{suggestion_ar}""",

                "en": """🤔 **Your question about {subject_en}**

{answer_en}

📚 **For further learning:**
{suggestion_en}""",

                "fr": """🤔 **Votre question sur {subject_fr}**

{answer_fr}

📚 **Pour approfondir:**
{suggestion_fr}"""
            }
        }
    
    def _load_examples(self):
        return {
            "algebra": {
                "ar": {
                    "example": "مثال: حل المعادلة 2س + 5 = 11\nالحل: 2س = 6 ⇒ س = 3",
                    "application": "تستخدم المعادلات في حساب القيم المجهولة في الفيزياء والاقتصاد",
                    "steps": "1. عزل الحد المجهول\n2. تطبيق العمليات العكسية\n3. التحقق من الحل",
                    "tip": "تأكد من تطبيق نفس العملية على طرفي المعادلة"
                },
                "en": {
                    "example": "Example: Solve equation 2x + 5 = 11\nSolution: 2x = 6 ⇒ x = 3",
                    "application": "Equations are used to calculate unknown values in physics and economics",
                    "steps": "1. Isolate the unknown term\n2. Apply inverse operations\n3. Verify the solution",
                    "tip": "Make sure to apply the same operation to both sides of the equation"
                },
                "fr": {
                    "example": "Exemple: Résoudre l'équation 2x + 5 = 11\nSolution: 2x = 6 ⇒ x = 3",
                    "application": "Les équations sont utilisées pour calculer des valeurs inconnues en physique et économie",
                    "steps": "1. Isoler le terme inconnu\n2. Appliquer les opérations inverses\n3. Vérifier la solution",
                    "tip": "Assurez-vous d'appliquer la même opération des deux côtés de l'équation"
                }
            },
            "grammar": {
                "ar": {
                    "example": "الجملة: 'الطالب يذاكر الدرس'\nالإعراب: يذاكر: فعل مضارع مرفوع",
                    "application": "تستخدم القواعد في الكتابة الصحيحة والتحليل الأدبي",
                    "steps": "1. تحديد نوع الكلمة\n2. معرفة موقعها الإعرابي\n3. تطبيق القاعدة المناسبة",
                    "tip": "انتبه للحركات الإعرابية فهي مفتاح الإعراب الصحيح"
                },
                "en": {
                    "example": "Sentence: 'The student studies the lesson'\nAnalysis: studies: present tense verb",
                    "application": "Grammar is used in correct writing and literary analysis",
                    "steps": "1. Identify word type\n2. Determine grammatical position\n3. Apply appropriate rule",
                    "tip": "Pay attention to verb tenses and subject-verb agreement"
                },
                "fr": {
                    "example": "Phrase: 'L'étudiant étudie la leçon'\nAnalyse: étudie: verbe au présent",
                    "application": "La grammaire est utilisée dans l'écriture correcte et l'analyse littéraire",
                    "steps": "1. Identifier le type de mot\n2. Déterminer la position grammaticale\n3. Appliquer la règle appropriée",
                    "tip": "Attention à l'accord du verbe avec le sujet"
                }
            }
        }
    
    def generate_response(self, question, subject, source_language, target_language="ar"):
        """توليد إجابة ذكية باستخدام RAG المحسن"""
        
        question_type = self.detect_question_type(question, source_language)
        relevant_concepts = self.find_relevant_concepts(question, subject, source_language)
        
        if question_type == "explanation" and relevant_concepts:
            return self.generate_explanation(relevant_concepts[0], subject, target_language)
        elif question_type == "comparison" and len(relevant_concepts) >= 2:
            return self.generate_comparison(relevant_concepts[0], relevant_concepts[1], subject, target_language)
        elif question_type == "step_by_step":
            return self.generate_step_by_step(question, subject, target_language)
        else:
            return self.generate_general_answer(question, subject, target_language)
    
    def detect_question_type(self, question, language):
        question_lower = question.lower()
        
        explanation_words = {
            "ar": ["ما هو", "ما هي", "اشرح", "عرف", "مفهوم", "شرح", "ماذا يعني"],
            "en": ["what is", "explain", "define", "concept of", "describe", "meaning of"],
            "fr": ["qu'est-ce que", "expliquez", "définir", "concept de", "décrivez", "signification de"]
        }
        
        comparison_words = {
            "ar": ["قارن", "الفرق بين", "ما الفرق", "المقارنة", "اختلاف", "مقارنة"],
            "en": ["compare", "difference between", "what is the difference", "comparison", "different"],
            "fr": ["comparez", "différence entre", "quelle est la différence", "comparaison", "différent"]
        }
        
        step_words = {
            "ar": ["كيف", "طريقة", "خطوات", "حل", "طريقة حل", "كيفية"],
            "en": ["how", "method", "steps", "solve", "solution", "way to"],
            "fr": ["comment", "méthode", "étapes", "résoudre", "solution", "façon de"]
        }
        
        for word in explanation_words[language]:
            if word in question_lower:
                return "explanation"
        
        for word in comparison_words[language]:
            if word in question_lower:
                return "comparison"
        
        for word in step_words[language]:
            if word in question_lower:
                return "step_by_step"
        
        return "general"
    
    def find_relevant_concepts(self, question, subject, language):
        """إيجاد المفاهيم ذات الصلة باستخدام مطابقة ذكية"""
        relevant = []
        subject_data = self.kb.subjects.get(subject, {})
        
        question_words = set(question.lower().split())
        
        for concept_id, concept_data in subject_data.get("concepts", {}).items():
            # البحث في النص العربي للمفهوم
            concept_text = concept_data.get("ar", "").lower()
            concept_words = set(concept_text.split())
            
            # حساب التشابه باستخدام تقاطع الكلمات
            common_words = question_words & concept_words
            if len(common_words) >= 1:
                relevant.append(concept_id)
            
            # البحث في اسم المفهوم نفسه
            if concept_id in question.lower():
                relevant.append(concept_id)
        
        return list(set(relevant))[:3]  # إرجاع 3 مفاهيم فريدة كحد أقصى
    
    def generate_explanation(self, concept_id, subject, target_language):
        """توليد شرح مفصل مع أمثلة"""
        concept_data = self.kb.subjects[subject]["concepts"][concept_id]
        example_data = self.examples.get(concept_id, {}).get(target_language, {})
        
        return self.templates["explanation"][target_language].format(
            concept=concept_id,
            explanation_ar=concept_data.get("ar", ""),
            explanation_en=concept_data.get("en", ""),
            explanation_fr=concept_data.get("fr", ""),
            example_ar=example_data.get("example", "لا يوجد مثال متاح"),
            example_en=example_data.get("example", "No example available"),
            example_fr=example_data.get("example", "Aucun exemple disponible"),
            application_ar=example_data.get("application", "تطبيق عملي في الحياة اليومية"),
            application_en=example_data.get("application", "Practical application in daily life"),
            application_fr=example_data.get("application", "Application pratique dans la vie quotidienne")
        )
    
    def generate_general_answer(self, question, subject, target_language):
        """توليد إجابة عامة"""
        subject_data = self.kb.subjects.get(subject, {})
        
        return self.templates["general"][target_language].format(
            subject_ar=subject_data.get("name", {}).get("ar", subject),
            subject_en=subject_data.get("name", {}).get("en", subject),
            subject_fr=subject_data.get("name", {}).get("fr", subject),
            answer_ar="هذا سؤال مهم في هذه المادة. أنصحك بالتركيز على المبادئ الأساسية والممارسة المستمرة.",
            answer_en="This is an important question in this subject. I advise you to focus on basic principles and continuous practice.",
            answer_fr="C'est une question importante dans cette matière. Je vous conseille de vous concentrer sur les principes de base et la pratique continue.",
            suggestion_ar="جرب حل تمارين تطبيقية واطلب المساعدة من معلمك إذا needed.",
            suggestion_en="Try solving practical exercises and ask your teacher for help if needed.",
            suggestion_fr="Essayez de résoudre des exercices pratiques et demandez de l'aide à votre enseignant si nécessaire."
        )
