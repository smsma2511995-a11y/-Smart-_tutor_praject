import os
import json
import argparse
import subprocess
import time
import shutil
from pathlib import Path
from typing import Dict, Any, Tuple
from tenacity import retry, stop_after_attempt, wait_fixed
from contextlib import contextmanager
import psutil
import gc
import torch

print("🚀 Starting Optimized AI Code Processor...")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    import bitsandbytes
    AI_AVAILABLE = True
    print("✅ AI libraries imported successfully (8-bit enabled)")
except ImportError as e:
    print(f"❌ AI libraries not available. Ensure torch, transformers, and bitsandbytes are installed: {e}")
    AI_AVAILABLE = False

try:
    import psutil
    import humanize
    MEMORY_MONITOR_AVAILABLE = True
except ImportError:
    print("⚠️ psutil/humanize not available - memory monitoring disabled")
    MEMORY_MONITOR_AVAILABLE = False


class OptimizedAIProcessor:
    def __init__(self, model_size: str = "1.3b", batch_limit: int = 6, resume: bool = True, 
                 optimize_memory: bool = True, safe_mode: bool = True):
        self.model_size = model_size
        self.batch_limit = batch_limit
        self.resume = resume
        self.optimize_memory = optimize_memory
        self.safe_mode = safe_mode
        
        self.progress_file = "progress.json"
        self.processed_files = set()
        self.progress_data: Dict[str, Any] = {}
        self.original_content_cache: Dict[str, str] = {}
        
        self.all_files = [] 
        
        # ⭐ التحسين: فحص مساحة القرص عند التهيئة
        if self.safe_mode:
            self.check_disk_space()
        
        self.setup_model()
        self.load_progress()
    
    def check_disk_space(self):
        """فحص مساحة القرص وتنظيف الذاكرة المؤقتة إذا لزم الأمر."""
        try:
            total, used, free = shutil.disk_usage("/")
            free_gb = free // (2**30)
            print(f"💾 Disk Space - Total: {total//(2**30)}GB, Used: {used//(2**30)}GB, Free: {free_gb}GB")
            
            if free_gb < 2:  # أقل من 2GB متبقي
                print("🚨 WARNING: Low disk space! Cleaning cache...")
                self.clean_disk_cache()
        except Exception as e:
            print(f"⚠️ Could not check disk space: {e}")
    
    def clean_disk_cache(self):
        """تنظيف الذاكرة المؤقتة للقرص."""
        try:
            print("🧹 Starting comprehensive disk cleanup...")
            
            # تنظيف ذاكرة pip المؤقتة
            result = subprocess.run(["pip", "cache", "purge"], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print("✅ pip cache cleaned")
            
            # تنظيف ذاكرة huggingface المؤقتة
            result = subprocess.run(["huggingface-cli", "delete-cache", "-f"], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print("✅ huggingface cache cleaned")
            
            # تنظيف ذاكرة torch المؤقتة
            torch_cache = os.path.expanduser("~/.cache/torch")
            if os.path.exists(torch_cache):
                subprocess.run(["rm", "-rf", torch_cache], capture_output=True)
                print("✅ torch cache cleaned")
            
            # تنظيف الملفات المؤقتة الأخرى
            temp_dirs = ['/tmp', '/var/tmp']
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    subprocess.run(["find", temp_dir, "-type", "f", "-name", "*.tmp", "-delete"], capture_output=True)
                    subprocess.run(["find", temp_dir, "-type", "f", "-name", "*.temp", "-delete"], capture_output=True)
            
            print("✅ Comprehensive disk cleanup completed")
            
            # فحص المساحة بعد التنظيف
            total, used, free = shutil.disk_usage("/")
            free_gb = free // (2**30)
            print(f"💾 After cleanup - Free: {free_gb}GB")
                
        except Exception as e:
            print(f"⚠️ Cache cleaning failed: {e}")
    
    def setup_model(self):
        """إعداد النموذج مع الإعدادات المحسنة وتحميل 8-بت."""
        if not AI_AVAILABLE:
            print("❌ AI not available - running in fallback mode (copy only)")
            self.model = None
            return
            
        try:
            model_name = "deepseek-ai/deepseek-coder-1.3b-base"
            print(f"🔧 Loading optimized model: {model_name}")
            
            # ⭐ التحسين: تنظيف القرص قبل تحميل النموذج
            if self.safe_mode:
                self.check_disk_space()
            
            # ⭐ الإصلاح: تعطيل hf_transfer مؤقتًا لتجنب الأخطاء
            original_env = os.environ.get('HF_HUB_ENABLE_HF_TRANSFER')
            os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                padding_side="left"
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                load_in_8bit=True,
                device_map="auto",
                low_cpu_mem_usage=True,
                trust_remote_code=True,
            )
            
            # ⭐ استعادة إعدادات البيئة الأصلية
            if original_env is not None:
                os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = original_env
            else:
                os.environ.pop('HF_HUB_ENABLE_HF_TRANSFER', None)
            
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            
            print("✅ Optimized AI model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            print("🔄 Falling back to copy mode without AI processing")
            self.model = None

    def clear_memory(self):
        """تنظيف ذاكرة GPU/CUDA بعد كل دفعة."""
        if self.optimize_memory and AI_AVAILABLE and torch.cuda.is_available():
            mem_allocated = torch.cuda.memory_allocated()
            mem_cached = torch.cuda.memory_reserved()
            torch.cuda.empty_cache()
            
            if MEMORY_MONITOR_AVAILABLE:
                print(f"🧹 Clearing CUDA cache: Allocated={humanize.naturalsize(mem_allocated)}, Cached={humanize.naturalsize(mem_cached)}")
        
        if self.optimize_memory:
            import gc
            gc.collect()
        
        if MEMORY_MONITOR_AVAILABLE:
            process = psutil.Process(os.getpid())
            print(f"   Current CPU RAM usage: {humanize.naturalsize(process.memory_info().rss)}")

    @contextmanager
    def timer(self, operation_name: str):
        """مراقب بسيط لوقت التشغيل."""
        start = time.time()
        yield
        print(f"⏱️ {operation_name} completed in {time.time() - start:.2f}s")
    
    def discover_files(self):
        """اكتشاف جميع ملفات الكود المراد معالجتها مع قواعد الاستبعاد."""
        extensions = {'.py', '.js', '.html', '.css', '.md', '.txt', '.json'}
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'cleaned_repo', '.github'}
        
        files = []
        for root, dirs, filenames in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in filenames:
                file_path = Path(root) / file
                if any(exclude in file_path.parts for exclude in exclude_dirs):
                     continue
                
                if (file_path.suffix.lower() in extensions and 
                    file_path.stat().st_size <= 50 * 1024):
                    files.append(str(file_path))
        return files

    def initialize_progress(self):
        """تهيئة سجل التقدم."""
        self.all_files = self.discover_files()
        self.progress_data = {
            'total': len(self.all_files),
            'processed': 0,
            'progress': 0.0,
            'batches_completed': 0,
            'processed_files': []
        }
        print(f"📁 Found {len(self.all_files)} files to process")

    def load_progress(self):
        """تحميل سجل التقدم."""
        self.all_files = self.discover_files()
        
        if self.resume and Path(self.progress_file).exists():
            try:
                with open(self.progress_file, 'r') as f:
                    self.progress_data = json.load(f)
                self.processed_files = set(self.progress_data.get('processed_files', []))
                processed_count = self.progress_data.get('processed', 0)
                total_count = self.progress_data.get('total', 0)
                print(f"🔄 Resumed: {processed_count}/{total_count} files processed")
            except Exception as e:
                print(f"⚠️ Failed to load progress: {e}")
                self.initialize_progress()
        else:
            self.initialize_progress()
    
    def get_next_batch(self):
        """الحصول على الدفعة التالية من الملفات للمعالجة."""
        remaining = [f for f in self.all_files if f not in self.processed_files]
        
        python_files = [f for f in remaining if f.endswith('.py')]
        js_files = [f for f in remaining if f.endswith('.js')]
        other_files = [f for f in remaining if not f.endswith(('.py', '.js'))]
        
        prioritized_files = python_files + js_files + other_files
        
        # ⭐ التحسين: تقليل حجم الدفعة في safe mode
        if self.safe_mode and len(prioritized_files) > 4:
            print("🛡️ Safe mode: Reducing batch size for stability")
            return prioritized_files[:4]
        
        return prioritized_files[:self.batch_limit]

    def build_prompt(self, content: str, file_type: str) -> str:
        """بناء البرومبت المُحسَّن لنموذج DeepSeek."""
        
        instruction = (
            "You are an expert code optimizer and cleaner. "
            "Your task is to analyze the following code, "
            "refactor it to be more efficient, and standard compliant. "
            "Crucially, the output code must be fully compliant with Black, isort, and Flake8 standards. "
            "The line length must not exceed 100 characters. "
            "Return ONLY the cleaned code block and nothing else."
        )
        
        if file_type == '.py':
             return f"{instruction}\n\n```{file_type.strip('.')}\n{content.strip()}\n```"
        
        base_prompt = f"Review and optimize the following {file_type.strip('.') if file_type != '.py' else 'code'}. Output ONLY the clean, final code block and nothing else:\n\n"
        return f"{base_prompt}```{file_type.strip('.')}\n{content.strip()}\n```"

    def process_file_without_ai(self, content: str, file_path: str) -> str:
        """معالجة الملف بدون AI - تطبيق التنسيق الأساسي فقط."""
        file_suffix = Path(file_path).suffix
        
        if file_suffix == '.py':
            try:
                # حفظ الملف مؤقتًا لتطبيق التنسيق
                temp_path = Path('temp_processing.py')
                temp_path.write_text(content, encoding='utf-8')
                
                # ⭐ التحسين: تطبيق autopep8 أولاً لإصلاح الأخطاء النحوية
                subprocess.run(["autopep8", "--in-place", "--aggressive", str(temp_path)], check=False, timeout=30)
                
                # ثم تطبيق black
                result = subprocess.run(["black", str(temp_path), "--quiet"], capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    print(f"⚠️ Black failed for {file_path}, using autopep8 only")
                    # إذا فشل Black، نستخدم autopep8 فقط
                    subprocess.run(["autopep8", "--in-place", str(temp_path)], check=False, timeout=30)
                
                formatted_content = temp_path.read_text(encoding='utf-8')
                temp_path.unlink()  # حذف الملف المؤقت
                
                print(f"📝 Formatted {file_path} (no AI)")
                return formatted_content
            except Exception as e:
                print(f"⚠️ Formatting failed for {file_path}: {e}")
                return content
        else:
            return content

    def quality_check(self, code: str, file_type: str) -> str:
        """فحص جودة أساسي للكود المُنتَج."""
        if file_type == '.py':
            # ⭐ الإصلاح: إصلاح الأخطاء الشائعة في النصوص العربية
            if "fمعالجة" in code:
                code = code.replace("fمعالجة", "f\"معالجة\"")
            if "f'معالجة" in code:
                code = code.replace("f'معالجة", "f\"معالجة\"")
            
            if "random.choice" in code:
                code = code.replace("['','', '', '','','',,'']", "['choice1', 'choice2', 'choice3']")
                code = code.replace("['','']", "['item1', 'item2']")
            
            # إزالة أي برومبت متبقي من AI
            lines = code.split('\n')
            cleaned_lines = []
            for line in lines:
                if any(keyword in line for keyword in ['Review and optimize', 'cleaned code block', 'Return ONLY']):
                    continue
                cleaned_lines.append(line)
            code = '\n'.join(cleaned_lines)
            
        return code

    def extract_clean_code(self, result: str, file_type: str) -> str:
        """استخراج الكود النظيف بطريقة مبسطة وآمنة."""
        
        # ⭐ التحسين: تنظيف أكثر شمولية للبرومبت
        if '```' not in result:
            # إذا لم يكن هناك كتلة كود، نحاول استخراج الكود مباشرة
            lines = result.split('\n')
            code_lines = []
            for line in lines:
                if any(keyword in line.lower() for keyword in ['explanation', 'note:', 'here is', 'cleaned code', 'the cleaned', 'review and optimize']):
                    continue
                if line.strip() and not line.startswith('```'):
                    code_lines.append(line)
            return '\n'.join(code_lines).strip()
            
        try:
            parts = result.split('```')
            cleaned = parts[-2]  # نأخذ الكتلة قبل الأخيرة (عادةً الكود)
            
            lang_prefix = file_type.strip('.')
            if cleaned.lower().startswith(lang_prefix):
                cleaned = cleaned[len(lang_prefix):]
            
            lines = [
                line for line in cleaned.split('\n')
                if not any(keyword in line.lower() for keyword in 
                          ['explanation', 'note:', 'here is', 'cleaned code', 'the cleaned', 'review and optimize'])
            ]
            
            return '\n'.join(lines).strip()
        
        except Exception:
            return result.strip()

    def _generate_ai_code(self, full_prompt: str, file_type: str) -> str:
        """توليد الكود بواسطة DeepSeek."""
        if self.model is None:
            return "Error: AI not available"
            
        with self.timer("AI Generation"):
            try:
                inputs = self.tokenizer(
                    full_prompt, 
                    return_tensors="pt", 
                    truncation=True, 
                    max_length=2048,
                    padding=True
                )
                
                with torch.no_grad():
                    with torch.cuda.amp.autocast(dtype=torch.bfloat16):
                        outputs = self.model.generate(
                            inputs.input_ids,
                            attention_mask=inputs.attention_mask,
                            max_new_tokens=600,  
                            temperature=0.2,
                            do_sample=True,
                            pad_token_id=self.tokenizer.pad_token_id,
                            eos_token_id=self.tokenizer.eos_token_id,
                            repetition_penalty=1.2,
                            no_repeat_ngram_size=3
                        )
                
                result = self.tokenizer.decode(
                    outputs[0], 
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=True
                )
                
                cleaned_code = self.extract_clean_code(result, file_type)
                cleaned_code = self.quality_check(cleaned_code, file_type)
                
                return cleaned_code.strip()
                
            except Exception as e:
                print(f"⚠️ AI processing failed during generation: {e}")
                return "Error: AI failed to generate valid code"

    def run_pylint(self, file_path: Path) -> Tuple[bool, str]:
        """تشغيل Pylint واستخراج رسالة الخطأ النحوي."""
        try:
            result = subprocess.run(
                ["pylint", str(file_path), "--disable=all", "--enable=E0001,F0001", "--output-format=text"],
                capture_output=True, text=True, timeout=30
            )
            
            if "E0001" in result.stdout or "F0001" in result.stdout:
                error_message = "\n".join([line for line in result.stdout.split('\n') if "error" in line.lower() or "fatal" in line.lower()])
                return True, error_message.strip()
            
            return False, ""
        except Exception as e:
            return True, f"Pylint failed to execute: {e}"

    def validate_python_syntax(self, code: str) -> bool:
        """التحقق من صحة بناء الجملة في Python."""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            print(f"⚠️ Syntax error detected: {e}")
            return False

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(5))
    def repair_with_ai_loop(self, original_content: str, file_path: str, is_retry: bool = False) -> str:
        """حلقة التصحيح الذاتي الموجه بالأخطاء."""
        # ⭐ إذا كان AI غير متاح، استخدم المعالجة الأساسية
        if self.model is None:
            return self.process_file_without_ai(original_content, file_path)
            
        file_suffix = Path(file_path).suffix
        temp_output_path = Path('cleaned_repo') / file_path
        
        if is_retry:
            print(f"🔄 Attempting AI self-correction for {file_path} (Retry 1/1)...")
            is_error, error_msg = self.run_pylint(temp_output_path)
            
            if not is_error and file_suffix == '.py':
                try:
                    subprocess.run(["autopep8", "--in-place", "--aggressive", str(temp_output_path)], check=True, timeout=30)
                    subprocess.run(["black", str(temp_output_path), "--check"], check=True, timeout=60)
                    print("✅ autopep8 fix successful. Passing.")
                    return temp_output_path.read_text(encoding='utf-8')
                except Exception:
                    pass
            
            prompt = (
                "The previous code failed a Black/Pylint check with the following error:\n"
                f"--- ERROR: {error_msg} ---\n"
                "You MUST fix this precise error and return ONLY the syntactically correct, Black-compliant code block."
            )
            content_to_process = temp_output_path.read_text(encoding='utf-8', errors='ignore')
            full_prompt = f"{prompt}\n\n```{file_suffix.strip('.')}\n{content_to_process.strip()}\n```"
            
        else:
            content_to_process = original_content
            full_prompt = self.build_prompt(content_to_process[:2500], file_suffix)

        cleaned_content = self._generate_ai_code(full_prompt, file_suffix)
        
        temp_output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_output_path.write_text(cleaned_content, encoding='utf-8')

        try:
            # ⭐ التحسين: التحقق من صحة بناء الجملة أولاً
            if file_suffix == '.py' and not self.validate_python_syntax(cleaned_content):
                raise Exception("Generated code has syntax errors")
                
            subprocess.run(["black", str(temp_output_path), "--check"], check=True, timeout=60)
            print(f"✅ AI output for {file_path} passed Black/Pylint check.")
            return cleaned_content

        except subprocess.CalledProcessError:
            if not is_retry:
                raise Exception("Black failed: initiating AI self-correction loop.")
            else:
                print(f"❌ AI self-correction for {file_path} failed after retry. Reverting to original content.")
                return original_content 
        
        except Exception as e:
            print(f"❌ Unexpected failure in repair loop: {e}. Reverting to original content.")
            return original_content

    def process_batch(self):
        """معالجة دفعة واحدة من الملفات."""
        # ⭐ التحسين: فحص مساحة القرص قبل البدء
        if self.safe_mode:
            self.check_disk_space()
        
        batch_files = self.get_next_batch()
        
        if not batch_files:
            print("🎉 All files processed!")
            return True
        
        print(f"🔄 Processing {len(batch_files)} files...")
        if self.model is None:
            print("⚠️ Running in FALLBACK MODE - AI not available, using basic formatting only")
        
        success_count = 0
        with self.timer(f"Processing Batch of {len(batch_files)} files"):
            for file_path in batch_files:
                try:
                    content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
                    self.original_content_cache[file_path] = content
                    
                    cleaned_content = self.repair_with_ai_loop(content, file_path)
                    
                    output_path = Path('cleaned_repo') / file_path
                    output_path.write_text(cleaned_content, encoding='utf-8')
                    
                    self.processed_files.add(file_path)
                    success_count += 1
                    print(f"✅ Finalized: {file_path}")
                    
                    # ⭐ التحسين: تنظيف الذاكرة بعد كل ملف في safe mode
                    if self.optimize_memory:
                        self.clear_memory()
                    
                except Exception as e:
                    print(f"❌ Failed to process: {file_path} - {e}")
            
            if AI_AVAILABLE and self.optimize_memory:
                self.clear_memory()

        self.progress_data['processed'] = len(self.processed_files)
        self.progress_data['progress'] = (self.progress_data['processed'] / self.progress_data['total']) * 100
        self.progress_data['batches_completed'] += 1
        self.progress_data['processed_files'] = list(self.processed_files)
        
        self.save_progress()
        
        print(f"📊 Batch completed: {success_count}/{len(batch_files)} files successful")
        print(f"📈 Overall progress: {self.progress_data['processed']}/{self.progress_data['total']} ({self.progress_data['progress']:.1f}%)")
        
        return False
    
    def save_progress(self):
        """حفظ سجل التقدم."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='AI Code Processor with optimized settings')
    parser.add_argument('--model', default='1.3b', help='Model size')
    parser.add_argument('--limit', type=int, default=6, help='Batch size limit')
    parser.add_argument('--resume', type=bool, default=True, help='Resume from previous progress')
    # ⭐ الإصلاح: إضافة الوسيطات الجديدة
    parser.add_argument('--optimize-memory', action='store_true', help='Enable memory optimization')
    parser.add_argument('--safe-mode', action='store_true', help='Enable safe mode with disk monitoring')
    
    args = parser.parse_args()
    
    print(f"🚀 Starting Optimized AI Processor (Batch: {args.limit}, Model: {args.model})")
    if args.optimize_memory:
        print("🧠 Memory optimization: ENABLED")
    if args.safe_mode:
        print("🛡️ Safe mode: ENABLED")
    
    processor = OptimizedAIProcessor(
        model_size=args.model,
        batch_limit=args.limit,
        resume=args.resume,
        optimize_memory=args.optimize_memory,
        safe_mode=args.safe_mode
    )
    
    is_complete = processor.process_batch()
    
    if is_complete:
        print("🎉 Processing complete! All files have been processed.")
    else:
        print(f"🔄 Batch completed. Ready for next batch.")


if __name__ == "__main__":
    main()
