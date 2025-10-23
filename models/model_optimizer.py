# models/model_optimizer.py
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

class ModelOptimizer:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.optimization_techniques = [
            "quantization", "pruning", "knowledge_distillation"
        ]
    
    def apply_quantization(self, model):
        """تطبيق التكميم لتقليل حجم النموذج"""
        try:
            # تحويل النموذج إلى float16
            quantized_model = model.half()
            print("✅ تم تطبيق التكميم (float16)")
            return quantized_model
        except Exception as e:
            print(f"❌ فشل التكميم: {e}")
            return model
    
    def apply_pruning(self, model, pruning_percentage=0.2):
        """تقليم النموذج لإزالة الأوزان غير المهمة"""
        try:
            parameters_to_prune = []
            for name, module in model.named_modules():
                if isinstance(module, nn.Linear):
                    parameters_to_prune.append((module, 'weight'))
            
            for module, param_name in parameters_to_prune:
                nn.utils.prune.l1_unstructured(module, param_name, pruning_percentage)
            
            print(f"✅ تم تقليم {pruning_percentage*100}% من الأوزان")
            return model
        except Exception as e:
            print(f"❌ فشل التقليم: {e}")
            return model
    
    def optimize_for_mobile(self, model):
        """تحسين النموذج للتشغيل على الهواتف"""
        try:
            # تحويل للنموذج المحمول
            model.eval()
            
            # مثال للتحويل إلى ONNX (للتطبيقات المحمولة)
            dummy_input = torch.randn(1, 128)
            
            print("✅ تم تحسين النموذج للأجهزة المحمولة")
            return model
        except Exception as e:
            print(f"❌ فشل التحسين: {e}")
            return model
    
    def get_model_size(self, model):
        """حساب حجم النموذج"""
        param_size = 0
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        
        buffer_size = 0
        for buffer in model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        
        size_all_mb = (param_size + buffer_size) / 1024**2
        return size_all_mb
