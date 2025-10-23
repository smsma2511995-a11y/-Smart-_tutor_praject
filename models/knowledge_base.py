# models/knowledge_base.py
import json
import re
from typing import Dict, List, Optional

class EducationalKnowledgeBase:
    def __init__(self):
        self.subjects = self._load_comprehensive_knowledge()
        self.language_codes = {"ar": 0, "en": 1, "fr": 2}
        self.subject_codes = {subject: idx for idx, subject in enumerate(self.subjects.keys())}
    
    def _load_comprehensive_knowledge(self):
        """قاعدة معرفة شاملة للمواد الدراسية"""
        return {
            "math": {
                "name": {"ar": "الرياضيات", "en": "Mathematics", "fr": "Mathématiques"},
                "concepts": {
                    "algebra": {
                        "ar": "الجبر هو فرع من الرياضيات يدرس الرموز والقوانين الرياضية لحل المعادلات",
                        "en": "Algebra is a branch of mathematics that studies mathematical symbols and rules for solving equations",
                        "fr": "L'algèbre est une branche des mathématiques qui étudie les symboles et règles mathématiques pour résoudre des équations"
                    },
                    "geometry": {
                        "ar": "الهندسة تدرس الأشكال والفراغ والعلاقات بين النقاط والخطوط والسطوح",
                        "en": "Geometry studies shapes, space, and relationships between points, lines, and surfaces",
                        "fr": "La géométrie étudie les formes, l'espace et les relations entre points, lignes et surfaces"
                    },
                    "calculus": {
                        "ar": "التفاضل والتكامل يدرس التغير والتراكم ومعدلات التغير",
                        "en": "Calculus studies change, accumulation, and rates of change",
                        "fr": "Le calcul étudie le changement, l'accumulation et les taux de changement"
                    }
                },
                "keywords": {
                    "ar": ["معادلة", "مجهول", "زاوية", "مساحة", "تكامل", "تفاضل", "دالة", "متغير"],
                    "en": ["equation", "variable", "angle", "area", "integral", "derivative", "function", "variable"],
                    "fr": ["équation", "variable", "angle", "surface", "intégrale", "dérivée", "fonction", "variable"]
                }
            },
            "english": {
                "name": {"ar": "اللغة الإنجليزية", "en": "English Language", "fr": "Anglais"},
                "concepts": {
                    "grammar": {
                        "ar": "قواعد اللغة الإنجليزية تشمل الأزمنة والأفعال المساعدة والجمل الشرطية",
                        "en": "English grammar includes tenses, auxiliary verbs, and conditional sentences",
                        "fr": "La grammaire anglaise comprend les temps, les verbes auxiliaires et les phrases conditionnelles"
                    },
                    "tenses": {
                        "ar": "أزمنة اللغة الإنجليزية تشمل الماضي والحاضر والمستقبل بأنواعها",
                        "en": "English tenses include past, present, and future in various forms",
                        "fr": "Les temps anglais incluent le passé, le présent et le futur sous diverses formes"
                    },
                    "vocabulary": {
                        "ar": "المفردات الإنجليزية أساسية للتواصل والقراءة والكتابة",
                        "en": "English vocabulary is essential for communication, reading, and writing",
                        "fr": "Le vocabulaire anglais est essentiel pour la communication, la lecture et l'écriture"
                    }
                },
                "keywords": {
                    "ar": ["قواعد", "زمن", "فعل", "جملة", "مفردات", "محادثة", "قراءة", "كتابة"],
                    "en": ["grammar", "tense", "verb", "sentence", "vocabulary", "conversation", "reading", "writing"],
                    "fr": ["grammaire", "temps", "verbe", "phrase", "vocabulaire", "conversation", "lecture", "écriture"]
                }
            },
            "french": {
                "name": {"ar": "اللغة الفرنسية", "en": "French Language", "fr": "Français"},
                "concepts": {
                    "grammar": {
                        "ar": "قواعد الفرنسية تشمل التذكير والتأنيث والأدوات والتركيب",
                        "en": "French grammar includes gender, articles, and sentence structure",
                        "fr": "La grammaire française comprend le genre, les articles et la structure des phrases"
                    },
                    "conjugation": {
                        "ar": "تصريف الأفعال الفرنسية حسب الزمن والضمير والمبني للمعلوم والمبني للمجهول",
                        "en": "French verb conjugation according to tense, pronoun, and voice",
                        "fr": "La conjugaison des verbes français selon le temps, le pronom et la voix"
                    },
                    "pronunciation": {
                        "ar": "نطق الفرنسية يعتمد على الحروف الصامتة والمتحركة والحركات",
                        "en": "French pronunciation depends on consonants, vowels, and accents",
                        "fr": "La prononciation française dépend des consonnes, des voyelles et des accents"
                    }
                },
                "keywords": {
                    "ar": ["قواعد", "تصريف", "نطق", "ضمير", "حرف", "جنس", "أداة", "تركيب"],
                    "en": ["grammar", "conjugation", "pronunciation", "pronoun", "article", "gender", "tool", "structure"],
                    "fr": ["grammaire", "conjugaison", "prononciation", "pronom", "article", "genre", "outil", "structure"]
                }
            },
            "science": {
                "name": {"ar": "العلوم", "en": "Science", "fr": "Science"},
                "concepts": {
                    "physics": {
                        "ar": "الفيزياء تدرس المادة والطاقة والقوى والحركة والقوانين الطبيعية",
                        "en": "Physics studies matter, energy, forces, motion, and natural laws",
                        "fr": "La physique étudie la matière, l'énergie, les forces, le mouvement et les lois naturelles"
                    },
                    "chemistry": {
                        "ar": "الكيمياء تدرس العناصر والمركبات والتفاعلات والروابط الكيميائية",
                        "en": "Chemistry studies elements, compounds, reactions, and chemical bonds",
                        "fr": "La chimie étudie les éléments, les composés, les réactions et les liaisons chimiques"
                    },
                    "biology": {
                        "ar": "الأحياء تدرس الكائنات الحية والخلية والوراثة والتطور",
                        "en": "Biology studies living organisms, cells, genetics, and evolution",
                        "fr": "La biologie étudie les organismes vivants, les cellules, la génétique et l'évolution"
                    }
                },
                "keywords": {
                    "ar": ["طاقة", "قوة", "تفاعل", "عنصر", "مركب", "خلية", "وراثة", "تطور"],
                    "en": ["energy", "force", "reaction", "element", "compound", "cell", "genetics", "evolution"],
                    "fr": ["énergie", "force", "réaction", "élément", "composé", "cellule", "génétique", "évolution"]
                }
            },
            "arabic": {
                "name": {"ar": "اللغة العربية", "en": "Arabic Language", "fr": "Arabe"},
                "concepts": {
                    "grammar": {
                        "ar": "النحو يدرس إعراب الكلمات وموقعها الإعرابي في الجملة",
                        "en": "Grammar studies the parsing of words and their grammatical position in the sentence",
                        "fr": "La grammaire étudie l'analyse des mots et leur position grammaticale dans la phrase"
                    },
                    "morphology": {
                        "ar": "الصرف يدرس بنية الكلمة وتصريفها وأوزانها",
                        "en": "Morphology studies word structure, conjugation, and patterns",
                        "fr": "La morphologie étudie la structure des mots, la conjugaison et les modèles"
                    },
                    "rhetoric": {
                        "ar": "البلاغة تدرس فنون البيان والمعاني والبديع",
                        "en": "Rhetoric studies the arts of expression, meanings, and embellishment",
                        "fr": "La rhétorique étudie les arts de l'expression, les significations et l'embellissement"
                    }
                },
                "keywords": {
                    "ar": ["نحو", "صرف", "بلاغة", "إعراب", "بناء", "فعل", "اسم", "حرف"],
                    "en": ["grammar", "morphology", "rhetoric", "parsing", "structure", "verb", "noun", "letter"],
                    "fr": ["grammaire", "morphologie", "rhétorique", "analyse", "structure", "verbe", "nom", "lettre"]
                }
            }
        }
    
    def detect_language(self, text):
        """كشف اللغة التلقائي المحسن"""
        arabic_chars = set('ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي')
        french_chars = set('éèêëàâçîïôùûüÿœæ')
        english_chars = set('abcdefghijklmnopqrstuvwxyz')
        
        text_chars = set(text.lower())
        
        arabic_count = len(text_chars & arabic_chars)
        french_count = len(text_chars & french_chars)
        english_count = len(text_chars & english_chars)
        
        if arabic_count > max(french_count, english_count, 3):
            return "ar"
        elif french_count > max(arabic_count, english_count, 3):
            return "fr"
        elif english_count > max(arabic_count, french_count, 3):
            return "en"
        else:
            # إذا كانت النسب متقاربة، نستخدم خوارزمية أكثر تطوراً
            return self._advanced_language_detection(text)
    
    def _advanced_language_detection(self, text):
        """كشف اللغة المتقدم باستخدام الكلمات الشائعة"""
        arabic_common = ['ال', 'في', 'من', 'على', 'إلى', 'أن', 'هو', 'هي']
        french_common = ['le', 'la', 'et', 'est', 'un', 'une', 'dans', 'pour']
        english_common = ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'for']
        
        text_lower = text.lower()
        arabic_score = sum(1 for word in arabic_common if word in text_lower)
        french_score = sum(1 for word in french_common if word in text_lower)
        english_score = sum(1 for word in english_common if word in text_lower)
        
        scores = {
            "ar": arabic_score,
            "fr": french_score, 
            "en": english_score
        }
        
        return max(scores.items(), key=lambda x: x[1])[0] if max(scores.values()) > 0 else "en"
    
    def detect_subject(self, text, language):
        """كشف المادة الدراسية المحسن"""
        text_lower = text.lower()
        scores = {}
        
        for subject, data in self.subjects.items():
            score = 0
            
            # البحث في الكلمات المفتاحية للمادة
            keywords = data["keywords"].get(language, [])
            for keyword in keywords:
                if keyword in text_lower:
                    score += 2
            
            # البحث في أسماء المفاهيم
            for concept_name in data["concepts"].keys():
                if concept_name in text_lower:
                    score += 3
            
            # البحث في أسماء المواد باللغات المختلفة
            for lang in ["ar", "en", "fr"]:
                subject_name = data["name"][lang].lower()
                if subject_name in text_lower:
                    score += 5
            
            scores[subject] = score
        
        # إرجاع المادة ذات أعلى درجة، أو الرياضيات كافتراضي
        best_subject = max(scores.items(), key=lambda x: x[1])[0] if scores else "math"
        return best_subject if scores[best_subject] > 0 else "math"
# في models/knowledge_base.py - محسن لكشف أي مادة
def detect_subject(self, text, language):
    """كشف المادة الدراسية - يعمل مع أي مادة جديدة"""
    text_lower = text.lower()
    scores = {}
    
    # 1. البحث في المواد المعرفة مسبقاً
    for subject, data in self.subjects.items():
        score = 0
        
        # البحث في الكلمات المفتاحية
        keywords = data["keywords"].get(language, [])
        for keyword in keywords:
            if keyword in text_lower:
                score += 2
        
        # البحث في أسماء المفاهيم
        for concept_name in data["concepts"].keys():
            if concept_name in text_lower:
                score += 3
        
        # البحث في أسماء المواد
        for lang in ["ar", "en", "fr"]:
            subject_name = data["name"][lang].lower()
            if subject_name in text_lower:
                score += 5
        
        scores[subject] = score
    
    # 2. إذا لم توجد نتائج قوية، نستخدم الكشف الذكي للمواد الجديدة
    if not scores or max(scores.values()) < 2:
        return self._detect_new_subject(text, language)
    
    best_subject = max(scores.items(), key=lambda x: x[1])[0]
    return best_subject

def _detect_new_subject(self, text, language):
    """كشف المواد الجديدة بناءً على المحتوى"""
    text_lower = text.lower()
    
    # كلمات مفتاحية للمواد الشائعة
    subject_keywords = {
        "physics": {
            "ar": ["طاقة", "قوة", "حركة", "سرعة", "تسارع", "كتلة", "شحنة", "مغناطيس"],
            "en": ["energy", "force", "motion", "velocity", "acceleration", "mass", "charge", "magnet"],
            "fr": ["énergie", "force", "mouvement", "vitesse", "accélération", "masse", "charge", "aimant"]
        },
        "chemistry": {
            "ar": ["عنصر", "مركب", "تفاعل", "ذرة", "جزيء", "ph", "حمض", "قلوي"],
            "en": ["element", "compound", "reaction", "atom", "molecule", "ph", "acid", "base"],
            "fr": ["élément", "composé", "réaction", "atome", "molécule", "ph", "acide", "base"]
        },
        "history": {
            "ar": ["تاريخ", "حضارة", "امبراطورية", "ملك", "معركة", "ثورة", "قديم", "وسيط"],
            "en": ["history", "civilization", "empire", "king", "battle", "revolution", "ancient", "medieval"],
            "fr": ["histoire", "civilisation", "empire", "roi", "bataille", "révolution", "ancien", "médiéval"]
        },
        "geography": {
            "ar": ["خريطة", "قارة", "محيط", "جبل", "نهر", "مناخ", "تضاريس", "دولة"],
            "en": ["map", "continent", "ocean", "mountain", "river", "climate", "terrain", "country"],
            "fr": ["carte", "continent", "océan", "montagne", "rivière", "climat", "relief", "pays"]
        }
    }
    
    scores = {}
    for subject, keywords in subject_keywords.items():
        score = 0
        for keyword in keywords.get(language, []):
            if keyword in text_lower:
                score += 2
        scores[subject] = score
    
    if scores and max(scores.values()) > 0:
        return max(scores.items(), key=lambda x: x[1])[0]
    
    return "general"  # إذا لم يتم التعرف، نستخدم الوضع العام
