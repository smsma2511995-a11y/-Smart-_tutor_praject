#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مساعد الكتابة وتقييم المقالات للغات المختلفة
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class AdvancedEssayEvaluator:
    """مقيم المقالات المتقدم للغات المختلفة"""
    
    def __init__(self):
        self.language_rules = self._initialize_language_rules()
        self.grading_rubrics = self._initialize_grading_rubrics()
        self.feedback_templates = self._initialize_feedback_templates()
        self.plagiarism_patterns = self._initialize_plagiarism_patterns()
    
    # الدوال الافتراضية لتحميل القواعد (للحفاظ على قابلية التنفيذ)
    def _load_arabic_grammar_rules(self): return []
    def _load_arabic_style_guidelines(self): return []
    def _load_arabic_common_errors(self) -> List[Tuple[str, str, str]]:
        return [
            (r'هاذا\b', 'هذا', 'خطأ في كتابة هذا'),
            (r'إلى\s+أن\s+لن', 'إلى ألا', 'خطأ في حروف الجر'),
        ]
    def _load_english_grammar_rules(self): return []
    def _load_english_style_guidelines(self): return []
    def _load_english_common_errors(self) -> List[Tuple[str, str, str]]:
        return [
            (r'\bthats\b', "that's", 'Missing apostrophe'),
            (r'\bthere\s+are\s+much\b', "there are many", 'Wrong quantifier'),
        ]
    def _load_french_grammar_rules(self): return []
    def _load_french_style_guidelines(self): return []
    def _load_french_common_errors(self) -> List[Tuple[str, str, str]]:
        return []
    
    def _initialize_language_rules(self) -> Dict:
        """تهيئة قواعد اللغة للغات المختلفة"""
        return {
            'arabic': {
                'grammar_rules': self._load_arabic_grammar_rules(),
                'style_guidelines': self._load_arabic_style_guidelines(),
                'common_errors': self._load_arabic_common_errors()
            },
            'english': {
                'grammar_rules': self._load_english_grammar_rules(),
                'style_guidelines': self._load_english_style_guidelines(),
                'common_errors': self._load_english_common_errors()
            },
            'french': {
                'grammar_rules': self._load_french_grammar_rules(),
                'style_guidelines': self._load_french_style_guidelines(),
                'common_errors': self._load_french_common_errors()
            }
        }
    
    def _initialize_grading_rubrics(self) -> Dict:
        """تهيئة معايير التقييم"""
        return {
            'content_organization': {
                'excellent': {'score': 10, 'criteria': ['واضح', 'منظم', 'مترابط']},
                'good': {'score': 8, 'criteria': ['جيد', 'منظم جزئياً']},
                'fair': {'score': 6, 'criteria': ['مقبول', 'ضعيف الترابط']},
                'poor': {'score': 4, 'criteria': ['غير منظم', 'غير واضح']}
            },
            'language_use': {
                'excellent': {'score': 10, 'criteria': ['سليم', 'متنوع', 'فصيح']},
                'good': {'score': 8, 'criteria': ['جيد', 'أخطاء قليلة']},
                'fair': {'score': 6, 'criteria': ['مقبول', 'أخطاء متوسطة']},
                'poor': {'score': 4, 'criteria': ['ضعيف', 'أخطاء كثيرة']}
            },
            'vocabulary': {
                'excellent': {'score': 10, 'criteria': ['غني', 'مناسب', 'دقيق']},
                'good': {'score': 8, 'criteria': ['جيد', 'مناسب']},
                'fair': {'score': 6, 'criteria': ['محدود', 'متكرر']},
                'poor': {'score': 4, 'criteria': ['ضعيف', 'غير مناسب']}
            },
            'creativity': {
                'excellent': {'score': 10, 'criteria': ['مبدع', 'أصيل', 'جذاب']},
                'good': {'score': 8, 'criteria': ['جيد', 'مقبول']},
                'fair': {'score': 6, 'criteria': ['عادي', 'تقليدي']},
                'poor': {'score': 4, 'criteria': ['ضعيف', 'ممل']}
            }
        }
    
    def _initialize_feedback_templates(self) -> Dict:
        """تهيئة قوالب التغذية الراجعة"""
        return {
            'positive': [
                "أحسنت! {aspect} ممتاز.",
                "مجهود رائع في {aspect}.",
                "تحسن ملحوظ في {aspect}."
            ],
            'constructive': [
                "يمكن تحسين {aspect} عن طريق {suggestion}.",
                "انتبه إلى {aspect} وحاول {suggestion}.",
                "لتحسين {aspect}، جرب {suggestion}."
            ],
            'corrective': [
                "هناك خطأ في {aspect}، والصحيح هو {correction}.",
                "يحتاج {aspect} إلى تصحيح: {correction}.",
                "لتصحيح {aspect}: {correction}."
            ]
        }
    
    def _initialize_plagiarism_patterns(self) -> List[str]:
        """تهيئة أنماط الانتحال"""
        return [
            r"https?://[^\s]+",  # روابط
            r"©\s*\d{4}",  # حقوق نشر
            r"المصدر:",  # إشارات المصادر
        ]
    
    def evaluate_essay(self, essay_text: str, language: str, topic: str, 
                      student_level: str) -> Dict:
        """تقييم المقال بشكل شامل"""
        
        # التحليل الأساسي
        basic_analysis = self._analyze_essay_basics(essay_text, language)
        
        # التحقق من الانتحال
        plagiarism_check = self._check_plagiarism(essay_text)
        
        # التحليل اللغوي
        language_analysis = self._analyze_language(essay_text, language)
        
        # تقييم المحتوى
        content_evaluation = self._evaluate_content(essay_text, topic, language)
        
        # التقييم الشامل
        overall_evaluation = self._calculate_overall_evaluation(
            basic_analysis, language_analysis, content_evaluation, student_level
        )
        
        # توليد التغذية الراجعة
        detailed_feedback = self._generate_detailed_feedback(
            overall_evaluation, language_analysis, content_evaluation, student_level
        )
        
        return {
            'essay_topic': topic,
            'language': language,
            'student_level': student_level,
            'evaluation_date': datetime.now().isoformat(),
            'basic_analysis': basic_analysis,
            'plagiarism_check': plagiarism_check,
            'language_analysis': language_analysis,
            'content_evaluation': content_evaluation,
            'overall_evaluation': overall_evaluation,
            'detailed_feedback': detailed_feedback,
            'improvement_suggestions': self._generate_improvement_suggestions(overall_evaluation)
        }
    
    def _analyze_essay_basics(self, essay_text: str, language: str) -> Dict:
        """التحليل الأساسي للمقال"""
        words = essay_text.split()
        sentences = re.split(r'[.!?]', essay_text)
        paragraphs = essay_text.split('\n\n')
        
        # تنظيف القوائم الفارغة
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'average_sentence_length': len(words) / max(1, len(sentences)),
            'average_paragraph_length': len(words) / max(1, len(paragraphs)),
            'reading_level': self._assess_reading_level(words, sentences, language)
        }
    
    def _assess_reading_level(self, words: List[str], sentences: List[str], language: str) -> str:
        """تقييم مستوى القراءة"""
        avg_sentence_length = len(words) / max(1, len(sentences))
        avg_word_length = sum(len(word) for word in words) / max(1, len(words))
        
        if language == 'arabic':
            if avg_sentence_length < 10 and avg_word_length < 5:
                return 'مبتدئ'
            elif avg_sentence_length < 15 and avg_word_length < 6:
                return 'متوسط'
            else:
                return 'متقدم'
        else:
            if avg_sentence_length < 12 and avg_word_length < 5:
                return 'beginner'
            elif avg_sentence_length < 18 and avg_word_length < 6:
                return 'intermediate'
            else:
                return 'advanced'
    
    def _check_plagiarism(self, essay_text: str) -> Dict:
        """التحقق من الانتحال"""
        plagiarism_indicators = []
        
        for pattern in self.plagiarism_patterns:
            matches = re.findall(pattern, essay_text)
            if matches:
                plagiarism_indicators.extend(matches)
        
        return {
            'plagiarism_detected': len(plagiarism_indicators) > 0,
            'suspicious_elements': plagiarism_indicators,
            'originality_score': max(0, 10 - len(plagiarism_indicators)),
            'recommendation': 'تأكد من كتابة المحتوى بأسلوبك الخاص' if plagiarism_indicators else 'ممتاز - المحتوى أصلي'
        }
    
    def _analyze_language(self, essay_text: str, language: str) -> Dict:
        """التحليل اللغوي للمقال"""
        language_rules = self.language_rules.get(language, {})
        
        return {
            'grammar_analysis': self._analyze_grammar(essay_text, language),
            'vocabulary_analysis': self._analyze_vocabulary(essay_text, language),
            'style_analysis': self._analyze_style(essay_text, language),
            'common_errors_found': self._detect_common_errors(essay_text, language),
            'language_complexity': self._assess_language_complexity(essay_text, language)
        }
    
    def _analyze_grammar(self, essay_text: str, language: str) -> Dict:
        """تحليل القواعد النحوية"""
        # محاكاة التحليل النحوي
        grammar_issues = []
        
        if language == 'arabic':
            # كشف أخطاء شائعة في العربية
            arabic_errors = [
                (r'هاذا\b', 'هذا', 'خطأ في كتابة هذا'),
                (r'إلى\s+أن\s+لن', 'إلى ألا', 'خطأ في حروف الجر'),
                (r'الذين\s+هم', 'الذين', 'زيادة ضمير'),
            ]
            
            for pattern, correction, description in arabic_errors:
                if re.search(pattern, essay_text):
                    grammar_issues.append({
                        'issue': description,
                        'correction': correction,
                        'severity': 'medium'
                    })
        
        return {
            'grammar_score': max(0, 10 - len(grammar_issues)),
            'issues_found': grammar_issues,
            'issues_count': len(grammar_issues),
            'assessment': 'جيد' if len(grammar_issues) < 3 else 'يحتاج تحسين'
        }
    
    def _analyze_vocabulary(self, essay_text: str, language: str) -> Dict:
        """تحليل المفردات"""
        words = essay_text.split()
        unique_words = set(words)
        
        # حساب تنوع المفردات
        vocabulary_diversity = len(unique_words) / len(words) if words else 0
        
        # تحديد مستوى المفردات
        if vocabulary_diversity > 0.7:
            level = 'متقدم'
        elif vocabulary_diversity > 0.5:
            level = 'متوسط'
        else:
            level = 'محدود'
        
        return {
            'total_words': len(words),
            'unique_words': len(unique_words),
            'vocabulary_diversity': vocabulary_diversity,
            'vocabulary_level': level,
            'repetition_ratio': 1 - vocabulary_diversity
        }
    
    def _analyze_style(self, essay_text: str, language: str) -> Dict:
        """تحليل الأسلوب"""
        sentences = re.split(r'[.!?]', essay_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # تحليل تنوع طول الجمل
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # تقييم تنوع الأساليب
        style_variety = self._assess_style_variety(essay_text, language)
        
        return {
            'average_sentence_length': avg_sentence_length,
            'sentence_variety': min(1.0, len(set(sentence_lengths)) / len(sentence_lengths)) if sentence_lengths else 0,
            'style_consistency': 'جيد',
            'coherence_score': 8.0,
            'style_assessment': style_variety
        }
    
    def _assess_style_variety(self, essay_text: str, language: str) -> str:
        """تقييم تنوع الأسلوب"""
        # محاكاة تقييم تنوع الأسلوب
        stylistic_elements = [
            'استخدام الأسئلة البلاغية',
            'التشبيهات والاستعارات',
            'التنوع في بدايات الجمل'
        ]
        
        detected_elements = []
        for element in stylistic_elements:
            if element in essay_text[:500]:  # البحث في الجزء الأول
                detected_elements.append(element)
        
        if len(detected_elements) >= 2:
            return 'متنوع'
        elif len(detected_elements) >= 1:
            return 'متوسط'
        else:
            return 'محدود'
    
    def _detect_common_errors(self, essay_text: str, language: str) -> List[Dict]:
        """كشف الأخطاء الشائعة"""
        common_errors = self.language_rules.get(language, {}).get('common_errors', [])
        detected_errors = []
        
        for error_pattern, correction, description in common_errors:
            matches = re.finditer(error_pattern, essay_text)
            for match in matches:
                detected_errors.append({
                    'error': description,
                    'location': match.start(),
                    'correction': correction,
                    'example': match.group()
                })
        
        return detected_errors[:10]  # حد أقصى 10 أخطاء
    
    def _assess_language_complexity(self, essay_text: str, language: str) -> Dict:
        """تقييم تعقيد اللغة"""
        words = essay_text.split()
        sentences = re.split(r'[.!?]', essay_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # حساب مؤشرات التعقيد
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        complex_word_ratio = sum(1 for word in words if len(word) > 6) / len(words) if words else 0
        
        complexity_score = (avg_word_length * 0.3 + avg_sentence_length * 0.4 + complex_word_ratio * 0.3) * 2
        
        return {
            'complexity_score': complexity_score,
            'level': 'بسيط' if complexity_score < 5 else 'متوسط' if complexity_score < 8 else 'معقد',
            'indicators': {
                'average_word_length': avg_word_length,
                'average_sentence_length': avg_sentence_length,
                'complex_word_ratio': complex_word_ratio
            }
        }
    
    def _evaluate_content(self, essay_text: str, topic: str, language: str) -> Dict:
        """تقييم محتوى المقال"""
        return {
            'topic_relevance': self._assess_topic_relevance(essay_text, topic),
            'content_organization': self._assess_organization(essay_text),
            'argument_strength': self._assess_argument_strength(essay_text),
            'supporting_evidence': self._assess_supporting_evidence(essay_text),
            'originality': self._assess_originality(essay_text)
        }
    
    def _assess_topic_relevance(self, essay_text: str, topic: str) -> Dict:
        """تقييم صلة المحتوى بالموضوع"""
        topic_keywords = topic.split()
        relevance_score = 0
        
        for keyword in topic_keywords:
            if keyword.lower() in essay_text.lower():
                relevance_score += 2
        
        max_score = len(topic_keywords) * 2
        normalized_score = min(10, (relevance_score / max_score) * 10) if max_score > 0 else 5
        
        return {
            'score': normalized_score,
            'assessment': 'مرتبط' if normalized_score >= 7 else 'جزئي' if normalized_score >= 5 else 'ضعيف',
            'missing_keywords': [kw for kw in topic_keywords if kw.lower() not in essay_text.lower()]
        }
    
    def _assess_organization(self, essay_text: str) -> Dict:
        """تقييم تنظيم المحتوى"""
        paragraphs = essay_text.split('\n\n')
        
        # تحليل هيكل المقال
        has_introduction = len(paragraphs) > 0 and len(paragraphs[0].split()) >= 30
        has_conclusion = len(paragraphs) > 1 and len(paragraphs[-1].split()) >= 20
        paragraph_transitions = self._check_paragraph_transitions(paragraphs)
        
        organization_score = 0
        if has_introduction:
            organization_score += 3
        if has_conclusion:
            organization_score += 3
        organization_score += min(4, paragraph_transitions)
        
        return {
            'score': organization_score,
            'has_introduction': has_introduction,
            'has_conclusion': has_conclusion,
            'paragraph_transitions': paragraph_transitions,
            'structure_assessment': 'جيد' if organization_score >= 7 else 'متوسط' if organization_score >= 5 else 'ضعيف'
        }
    
    def _check_paragraph_transitions(self, paragraphs: List[str]) -> int:
        """فحص انتقالات الفقرات"""
        transition_indicators = [
            'أيضاً', 'بالإضافة', 'علاوة على', 'من ناحية أخرى',
            'في المقابل', 'بالمثل', 'نتيجة لذلك', 'باختصار'
        ]
        
        transition_count = 0
        for i in range(1, len(paragraphs)):
            first_sentence = paragraphs[i].split('.')[0] if '.' in paragraphs[i] else paragraphs[i]
            if any(transition in first_sentence for transition in transition_indicators):
                transition_count += 1
        
        return min(4, transition_count)
    
    def _assess_argument_strength(self, essay_text: str) -> Dict:
        """تقييم قوة الحجج"""
        argument_indicators = [
            'لأن', 'بسبب', 'نتيجة', 'يدل على', 'يؤكد',
            'يبرهن', 'يظهر', 'يدعم', 'يشير إلى'
        ]
        
        argument_count = sum(1 for indicator in argument_indicators if indicator in essay_text)
        
        return {
            'score': min(10, argument_count * 2),
            'argument_indicators_count': argument_count,
            'assessment': 'قوي' if argument_count >= 5 else 'متوسط' if argument_count >= 3 else 'ضعيف'
        }
    
    def _assess_supporting_evidence(self, essay_text: str) -> Dict:
        """تقييم الأدلة الداعمة"""
        evidence_indicators = [
            'على سبيل المثال', 'مثلاً', 'كذلك', 'كما',
            'إحصائية', 'دراسة', 'بحث', 'تقرير'
        ]
        
        evidence_count = sum(1 for indicator in evidence_indicators if indicator in essay_text)
        
        return {
            'score': min(10, evidence_count * 2),
            'evidence_indicators_count': evidence_count,
            'assessment': 'غني' if evidence_count >= 4 else 'متوسط' if evidence_count >= 2 else 'محدود'
        }
    
    def _assess_originality(self, essay_text: str) -> Dict:
        """تقييم الأصالة"""
        common_phrases = [
            'في الوقت الحاضر', 'في عصرنا هذا', 'لا شك أن',
            'جدير بالذكر', 'من المعروف أن', 'يعتبر من'
        ]
        
        common_phrase_count = sum(1 for phrase in common_phrases if phrase in essay_text)
        originality_score = max(0, 10 - common_phrase_count)
        
        return {
            'score': originality_score,
            'common_phrases_count': common_phrase_count,
            'assessment': 'مبدع' if originality_score >= 8 else 'متوسط' if originality_score >= 6 else 'تقليدي'
        }
    
    def _calculate_overall_evaluation(self, basic_analysis: Dict, language_analysis: Dict,
                                   content_evaluation: Dict, student_level: str) -> Dict:
        """حساب التقييم الشامل"""
        # أوزان التقييم
        weights = {
            'content': 0.4,
            'language': 0.4,
            'organization': 0.2
        }
        
        # حساب الدرجات
        content_score = content_evaluation['topic_relevance']['score'] * 0.3 + \
                      content_evaluation['argument_strength']['score'] * 0.3 + \
                      content_evaluation['supporting_evidence']['score'] * 0.2 + \
                      content_evaluation['originality']['score'] * 0.2
        
        language_score = language_analysis['grammar_analysis']['grammar_score'] * 0.4 + \
                        language_analysis['vocabulary_analysis']['vocabulary_diversity'] * 10 * 0.3 + \
                        language_analysis['style_analysis']['coherence_score'] * 0.3
        
        organization_score = content_evaluation['content_organization']['score']
        
        # التقييم الشامل
        overall_score = (content_score * weights['content'] + 
                        language_score * weights['language'] + 
                        organization_score * weights['organization'])
        
        # تحديد المستوى بناءً على درجة الطالب
        level_benchmarks = {
            'beginner': (6, 8, 10),
            'intermediate': (7, 9, 10),
            'advanced': (8, 9.5, 10)
        }
        
        good, excellent, perfect = level_benchmarks.get(student_level, (7, 9, 10))
        
        if overall_score >= excellent:
            grade = 'ممتاز'
        elif overall_score >= good:
            grade = 'جيد جداً'
        elif overall_score >= good - 2:
            grade = 'جيد'
        else:
            grade = 'مقبول'
        
        return {
            'overall_score': overall_score,
            'grade': grade,
            'content_score': content_score,
            'language_score': language_score,
            'organization_score': organization_score,
            'strengths': self._identify_strengths(content_evaluation, language_analysis),
            'areas_for_improvement': self._identify_improvement_areas(content_evaluation, language_analysis)
        }
    
    def _identify_strengths(self, content_evaluation: Dict, language_analysis: Dict) -> List[str]:
        """تحديد نقاط القوة"""
        strengths = []
        
        if content_evaluation['topic_relevance']['score'] >= 8:
            strengths.append('الالتزام بالموضوع')
        if content_evaluation['argument_strength']['score'] >= 8:
            strengths.append('قوة الحجج')
        if language_analysis['vocabulary_analysis']['vocabulary_level'] == 'متقدم':
            strengths.append('غنى المفردات')
        if language_analysis['grammar_analysis']['issues_count'] <= 2:
            strengths.append('دقة اللغة')
        
        return strengths if strengths else ['مجهود مشكور']
    
    def _identify_improvement_areas(self, content_evaluation: Dict, language_analysis: Dict) -> List[str]:
        """تحديد مجالات التحسين"""
        improvements = []
        
        if content_evaluation['topic_relevance']['score'] < 6:
            improvements.append('التركيز على الموضوع')
        if content_evaluation['argument_strength']['score'] < 6:
            improvements.append('تعزيز الحجج')
        if language_analysis['grammar_analysis']['issues_count'] > 5:
            improvements.append('تحسين القواعد')
        if content_evaluation['content_organization']['score'] < 6:
            improvements.append('تنظيم المحتوى')
        
        return improvements if improvements else ['مواصلة التحسن']
    
    def _generate_detailed_feedback(self, overall_evaluation: Dict, language_analysis: Dict,
                                 content_evaluation: Dict, student_level: str) -> List[Dict]:
        """توليد تغذية راجعة تفصيلية"""
        feedback = []
        
        # تغذية راجعة عن المحتوى
        content_feedback = {
            'aspect': 'المحتوى',
            'type': 'constructive',
            'message': self._generate_content_feedback(content_evaluation),
            'suggestions': self._generate_content_suggestions(content_evaluation)
        }
        feedback.append(content_feedback)
        
        # تغذية راجعة عن اللغة
        language_feedback = {
            'aspect': 'اللغة',
            'type': 'constructive',
            'message': self._generate_language_feedback(language_analysis),
            'suggestions': self._generate_language_suggestions(language_analysis)
        }
        feedback.append(language_feedback)
        
        # تغذية راجعة عن التنظيم
        organization_feedback = {
            'aspect': 'التنظيم',
            'type': 'constructive',
            'message': self._generate_organization_feedback(content_evaluation),
            'suggestions': self._generate_organization_suggestions(content_evaluation)
        }
        feedback.append(organization_feedback)
        
        # تغذية راجعة عامة
        overall_feedback = {
            'aspect': 'الأداء العام',
            'type': 'positive' if overall_evaluation['overall_score'] >= 7 else 'constructive',
            'message': f"التقييم العام: {overall_evaluation['grade']}",
            'suggestions': ['استمر في التميز'] if overall_evaluation['overall_score'] >= 8 else ['واصل التحسن']
        }
        feedback.append(overall_feedback)
        
        return feedback
    
    def _generate_content_feedback(self, content_evaluation: Dict) -> str:
        """توليد تغذية راجعة عن المحتوى"""
        relevance = content_evaluation['topic_relevance']
        arguments = content_evaluation['argument_strength']
        
        if relevance['score'] >= 8 and arguments['score'] >= 8:
            return "محتوى ممتاز ومرتبط بشكل جيد بالموضوع مع حجج قوية."
        elif relevance['score'] >= 6 and arguments['score'] >= 6:
            return "المحتوى جيد ولكن يمكن تعزيز الحجج والأدلة."
        else:
            return "المحتوى يحتاج إلى مزيد من التركيز على الموضوع وتقوية الحجج."
    
    def _generate_language_feedback(self, language_analysis: Dict) -> str:
        """توليد تغذية راجعة عن اللغة"""
        grammar = language_analysis['grammar_analysis']
        vocabulary = language_analysis['vocabulary_analysis']
        
        if grammar['grammar_score'] >= 8 and vocabulary['vocabulary_level'] == 'متقدم':
            return "استخدام ممتاز للغة مع مفردات غنية ودقة نحوية."
        elif grammar['grammar_score'] >= 6 and vocabulary['vocabulary_level'] == 'متوسط':
            return "اللغة جيدة ولكن هناك مجال لتحسين الدقة النحوية وتنويع المفردات."
        else:
            return "اللغة تحتاج إلى تحسين في القواعد النحوية وتوسيع المفردات."
    
    def _generate_organization_feedback(self, content_evaluation: Dict) -> str:
        """توليد تغذية راجعة عن التنظيم"""
        organization = content_evaluation['content_organization']
        
        if organization['score'] >= 8:
            return "تنظيم ممتاز للمحتوى مع انتقالات سلسة بين الأفكار."
        elif organization['score'] >= 6:
            return "التنظيم جيد ولكن يمكن تحسين انتقالات الفقرات."
        else:
            return "الهيكل التنظيمي يحتاج إلى تحسين مع التركيز على المقدمة والخاتمة."
    
    def _generate_content_suggestions(self, content_evaluation: Dict) -> List[str]:
        """توليد اقتراحات للمحتوى"""
        suggestions = []
        
        if content_evaluation['topic_relevance']['score'] < 7:
            suggestions.append("ركز أكثر على الموضوع الرئيسي وتجنب الحشو.")
        
        if content_evaluation['argument_strength']['score'] < 7:
            suggestions.append("أضف المزيد من الحجج المنطقية لدعم وجهة نظرك.")
        
        if content_evaluation['supporting_evidence']['score'] < 7:
            suggestions.append("استخدم أمثلة وأدلة ملموسة لدعم argumentsك.")
        
        return suggestions if suggestions else ["استمر في الأسلوب الحالي"]
    
    def _generate_language_suggestions(self, language_analysis: Dict) -> List[str]:
        """توليد اقتراحات للغة"""
        suggestions = []
        
        if language_analysis['grammar_analysis']['issues_count'] > 3:
            suggestions.append("راجع القواعد النحوية الأساسية.")
        
        if language_analysis['vocabulary_analysis']['vocabulary_diversity'] < 0.6:
            suggestions.append("حاول استخدام مفردات أكثر تنوعاً.")
        
        return suggestions if suggestions else ["اللغة جيدة، حافظ على هذا المستوى"]
    
    def _generate_organization_suggestions(self, content_evaluation: Dict) -> List[str]:
        """توليد اقتراحات للتنظيم"""
        suggestions = []
        
        organization = content_evaluation['content_organization']
        
        if not organization['has_introduction']:
            suggestions.append("أضف مقدمة واضحة تقدم الموضوع.")
        
        if not organization['has_conclusion']:
            suggestions.append("اختتم المقال بخاتمة تلخص النقاط الرئيسية.")
        
        if organization['paragraph_transitions'] < 2:
            suggestions.append("استخدم كلمات انتقالية لربط الفقرات.")
        
        return suggestions if suggestions else ["الهيكل التنظيمي جيد"]
    
    def _generate_improvement_suggestions(self, overall_evaluation: Dict) -> List[Dict]:
        """توليد اقتراحات تحسين شاملة"""
        suggestions = []
        
        for area in overall_evaluation['areas_for_improvement']:
            if 'الموضوع' in area:
                suggestions.append({
                    'area': 'الالتزام بالموضوع',
                    'suggestion': 'اقرأ الموضوع بعناية وخطط للنقاط الرئيسية قبل الكتابة',
                    'resources': ['دورة الكتابة المركزة', 'تمارين تحديد الفكرة الرئيسية']
                })
            elif 'الحجج' in area:
                suggestions.append({
                    'area': 'تقوية الحجج',
                    'suggestion': 'استخدم أدلة وأمثلة ملموسة لدعم argumentsك',
                    'resources': ['دورة التفكير النقدي', 'تمارين بناء الحجج']
                })
            elif 'القواعد' in area:
                suggestions.append({
                    'area': 'تحسين القواعد',
                    'suggestion': 'راجع القواعد النحوية الأساسية واطلب التغذية الراجعة',
                    'resources': ['مرجع القواعد النحوية', 'تمارين القواعد التفاعلية']
                })
        
        return suggestions
    
    def generate_writing_prompts(self, student_level: str, language: str, 
                               topic_category: str) -> List[Dict]:
        """توليد مواضيع كتابة مخصصة"""
        prompt_templates = {
            'beginner': [
                {
                    'topic': 'وصف شخص أعجبك',
                    'instructions': 'صف شخصية أعجبتك مع ذكر الصفات والأسباب',
                    'word_target': 150,
                    'suggested_structure': ['مقدمة', 'صفات', 'أسباب الإعجاب', 'خاتمة']
                },
                {
                    'topic': 'يوم لا تنساه',
                    'instructions': 'اكتب عن يوم مميز في حياتك',
                    'word_target': 200,
                    'suggested_structure': ['مقدمة', 'أحداث اليوم', 'لماذا هو مميز', 'خاتمة']
                }
            ],
            'intermediate': [
                {
                    'topic': 'أهمية القراءة',
                    'instructions': 'ناقش فوائد القراءة وأثرها على الفرد والمجتمع',
                    'word_target': 300,
                    'suggested_structure': ['مقدمة', 'فوائد فردية', 'فوائد مجتمعية', 'خاتمة']
                },
                {
                    'topic': 'التكنولوجيا وتأثيرها',
                    'instructions': 'حلل إيجابيات وسلبيات التكنولوجيا في حياتنا',
                    'word_target': 350,
                    'suggested_structure': ['مقدمة', 'إيجابيات', 'سلبيات', 'توازن', 'خاتمة']
                }
            ],
            'advanced': [
                {
                    'topic': 'التنمية المستدامة',
                    'instructions': 'ناقش مفهوم التنمية المستدامة وتحديات تطبيقها',
                    'word_target': 500,
                    'suggested_structure': ['مقدمة', 'تعريف', 'تحديات', 'حلول', 'خاتمة']
                },
                {
                    'topic': 'دور الشباب في المجتمع',
                    'instructions': 'حلل مسؤوليات الشباب وتأثيرهم في بناء المجتمع',
                    'word_target': 450,
                    'suggested_structure': ['مقدمة', 'مسؤوليات', 'تأثير', 'تحديات', 'خاتمة']
                }
            ]
        }
        
        return prompt_templates.get(student_level, prompt_templates['intermediate'])

# اختبار مقيم المقالات
if __name__ == "__main__":
    evaluator = AdvancedEssayEvaluator()
    
    # مقال اختباري
    sample_essay = """
    التعليم هو أساس تقدم المجتمعات. في عصرنا الحالي، أصبح التعليم ضرورياً لكل فرد. 
    التعليم يساعد في تنمية المهارات وتحسين مستوى المعيشة. 
    
    من خلال التعليم، يمكن للفرد أن يحصل على فرص عمل أفضل. كما أن التعليم ينمي التفكير النقدي والإبداع. 
    التعليم أيضاً يساهم في بناء مجتمع متحضر ومتطور.
    
    في الختام، يجب على الجميع الاهتمام بالتعليم لأنه مفتاح النجاح والتقدم.
    """
    
    # تقييم المقال
    evaluation = evaluator.evaluate_essay(
        essay_text=sample_essay,
        language='arabic',
        topic='أهمية التعليم',
        student_level='intermediate'
    )
    
    print("📝 تقييم المقال:")
    print(f"• الدرجة الشاملة: {evaluation['overall_evaluation']['overall_score']:.1f}/10")
    print(f"• التقييم: {evaluation['overall_evaluation']['grade']}")
    print(f"• نقاط القوة: {', '.join(evaluation['overall_evaluation']['strengths'])}")
    print(f"• مجالات التحسين: {', '.join(evaluation['overall_evaluation']['areas_for_improvement'])}")
    
    # توليد مواضيع كتابة
    prompts = evaluator.generate_writing_prompts('intermediate', 'arabic', 'اجتماعي')
    print(f"\n🎯 مواضيع مقترحة: {prompts[0]['topic']}")
