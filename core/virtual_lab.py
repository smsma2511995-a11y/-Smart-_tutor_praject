# core/virtual_lab.py
class VirtualLab:
    """مختبر افتراضي للتجارب العلمية"""
    
    def __init__(self):
        self.experiments = self.load_experiments()
    
    def load_experiments(self):
        return {
            "chemistry": {
                "titration": {
                    "name": "معايرة الحمض والقاعدة",
                    "description": "تجربة تحديد تركيز محلول حمضي",
                    "steps": [
                        "إضافة الحمض إلى دورق مخروطي",
                        "إضافة دليل الفينولفثالين",
                        "إضافة القاعدة من السحاحة قطرة قطرة",
                        "التوقف عند تغير اللون"
                    ],
                    "simulation": self.simulate_titration
                }
            },
            "physics": {
                "pendulum": {
                    "name": "بندول بسيط",
                    "description": "دراسة حركة البندول وعلاقتها بطول الخيط",
                    "simulation": self.simulate_pendulum
                }
            }
        }
    
    def run_experiment(self, subject, experiment_name, parameters):
        """تشغيل تجربة افتراضية"""
        if subject in self.experiments and experiment_name in self.experiments[subject]:
            experiment = self.experiments[subject][experiment_name]
            return experiment["simulation"](parameters)
        return None
    
    def simulate_titration(self, parameters):
        """محاكاة معايرة كيميائية"""
        # محاكاة بسيطة للتجربة
        acid_concentration = parameters.get("acid_conc", 0.1)
        base_concentration = parameters.get("base_conc", 0.1)
        volume_acid = parameters.get("volume_acid", 25)
        
        # حساب حجم القاعدة المطلوب
        volume_base = (acid_concentration * volume_acid) / base_concentration
        
        return {
            "result": f"حجم القاعدة المطلوب: {volume_base:.2f} ml",
            "observation": "يتغير لون المحلول من عديم اللون إلى الزهري الفاتح",
            "conclusion": "تم تحديد تركيز المحلول بنجاح"
        }
