# -*- coding: utf-8 -*-
"""
本地LLM引擎 - A+B双模型核心 v4.1
=================================
完全独立，不依赖任何第三方库
内置智能模板引擎 + 可选GGUF加载 + safetensors加载

A大模型: Llama 3.2 1B (Ollama/GGUF)
B大模型: Gemma4 多模态 (safetensors/Transformers)

系统启动时由 _somn_ensure.py Group D 自动预热
"""

import os
import time
import logging
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import re

logger = logging.getLogger("LocalLLM")

# ============================================================
# 常量
# ============================================================

# A大模型 (Llama 3.2 1B - GGUF/Ollama)
DEFAULT_MODEL_DIR = Path(__file__).resolve().parents[3] / "models" / "llama-3.2-1b-instruct"
DEFAULT_MODEL_FILE = "llama-3.2-1b-instruct-q4_k_m.gguf"
DEFAULT_MODEL_NAME = "llama-3.2-1b-a"

# B大模型 (Gemma4 多模态 - safetensors)
MODEL_B_DIR = Path(__file__).resolve().parents[3] / "models" / "gemma4-local-b"
MODEL_B_NAME = "gemma4-local-b"


# ============================================================
# 枚举
# ============================================================

class LoadMode(Enum):
    GGUF_DIRECT = "gguf_direct"
    CTRANSFORMERS = "ctransformers"
    SMART_TEMPLATE = "smart_template"
    OLLAMA = "ollama"
    SAFETENSORS = "safetensors"


class ServiceState(Enum):
    STOPPED = "stopped"
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"


# ============================================================
# 数据类
# ============================================================

@dataclass
class GenerationResult:
    text: str
    model: str
    tokens: int
    latency_ms: float
    finish_reason: str = "stop"
    error: Optional[str] = None


# ============================================================
# 智能模板引擎 v2.0
# ============================================================

class SmartTemplateEngine:
    """
    智能模板引擎 - 无依赖的主引擎
    
    基于语义理解的规则引擎，能处理多种类型的请求
    """

    def __init__(self):
        self._init_templates()
        self._init_topic_knowledge()

    def _init_templates(self):
        """初始化模板库"""
        
        # 概念解释模板
        self.concept_templates = [
            "【{topic}】是{field}领域的重要概念。\n\n📌 定义：\n{definition}\n\n🔍 特点：\n{features}\n\n💡 应用：\n{applications}",
            
            "关于【{topic}】，这是{field}中的核心内容：\n\n◆ 基本概念：{definition}\n\n◆ 关键要素：\n{features}\n\n◆ 实际应用：\n{applications}\n\n📚 推荐深入学习该主题的经典理论。",
        ]

        # 操作指南模板
        self.action_templates = [
            "【{action}】的方法与步骤：\n\n📝 前期准备：\n{prep}\n\n⚙️ 核心步骤：\n{steps}\n\n✅ 注意事项：\n{notes}",
            
            "关于【{action}】，以下是系统性指南：\n\n1️⃣ 准备阶段：{prep}\n\n2️⃣ 执行阶段：\n{steps}\n\n3️⃣ 收尾工作：{notes}",
        ]

        # 代码生成模板
        self.code_templates = {
            "python": """# {task}
{comments}

def {function_name}({params}):
    \"\"\"{docstring}\"\"\"
    {body}
    return {return_value}
""",
            "javascript": """// {task}
/**
 * {docstring}
 */
function {function_name}({params}) {{
    {body}
    return {return_value};
}}
""",
            "generic": """// {task}
/**
 * {docstring}
 */
function {function_name}({params}) {{
    // 实现逻辑
    {body}
    return {return_value};
}}
""",
        }

        # 翻译模板
        self.translate_templates = [
            "【翻译】\n\n📝 原文：{text}\n\n🌐 翻译：{translation}\n\n💭 说明：{notes}",
        ]

        # 分析模板
        self.analyze_templates = [
            "【分析报告】主题：{topic}\n\n📊 现状：\n{current_state}\n\n⚖️ 优劣势：\n{pros_cons}\n\n🎯 建议：\n{recommendations}",
        ]

    def _init_topic_knowledge(self):
        """初始化领域知识"""
        self.topic_definitions = {
            "python": {
                "field": "编程",
                "definition": "一种高级、解释型、面向对象的编程语言，以简洁易读的语法著称",
                "features": "• 语法简洁优雅\n• 丰富的标准库\n• 跨平台支持\n• 广泛的应用领域",
                "applications": "• Web开发 (Django, Flask)\n• 数据科学 (Pandas, NumPy)\n• 人工智能 (TensorFlow, PyTorch)\n• 自动化脚本",
            },
            "人工智能": {
                "field": "计算机科学",
                "definition": "使机器具有人类智能的技术，包括学习、推理、感知等能力",
                "features": "• 机器学习\n• 深度学习\n• 自然语言处理\n• 计算机视觉",
                "applications": "• 智能助手\n• 自动驾驶\n• 医疗诊断\n• 金融风控",
            },
            "javascript": {
                "field": "编程",
                "definition": "一种运行在浏览器中的脚本语言，也可用于服务端(Node.js)",
                "features": "• 事件驱动\n• 原型继承\n• 动态类型\n• 异步编程",
                "applications": "• 前端开发\n• 后端服务\n• 移动应用\n• 桌面应用",
            },
            "machine_learning": {
                "field": "人工智能",
                "definition": "让计算机从数据中自动学习并改进的算法技术",
                "features": "• 监督学习\n• 无监督学习\n• 强化学习\n• 深度学习",
                "applications": "• 图像识别\n• 语音识别\n• 推荐系统\n• 预测分析",
            },
        }

    def _extract_topic(self, prompt: str) -> str:
        """从提示中提取主题"""
        # 移除常见前缀
        patterns = [
            r'什么是(.+)',
            r'(.+)是什么',
            r'介绍一下(.+)',
            r'解释一下(.+)',
            r'说一说(.+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, prompt)
            if match:
                return match.group(1).strip()
        
        # 返回第一个关键词
        words = prompt.replace('?', '').replace('！', '').split()
        return words[2] if len(words) > 2 else prompt[:20]

    def _detect_intent(self, prompt: str) -> str:
        """检测意图"""
        prompt_lower = prompt.lower()
        
        # 代码相关
        if any(k in prompt_lower for k in ['代码', 'function', 'def ', 'class ', '函数', '写代码']):
            return 'code'
        
        # 翻译相关
        if any(k in prompt_lower for k in ['翻译', 'translate', '翻译成']):
            return 'translate'
        
        # 操作相关
        if any(k in prompt_lower for k in ['如何', '怎么', '怎样', '步骤', '方法']):
            return 'action'
        
        # 分析相关
        if any(k in prompt_lower for k in ['分析', '比较', '对比', '评估']):
            return 'analyze'
        
        # 默认概念解释
        return 'concept'

    def _detect_code_language(self, prompt: str) -> str:
        """检测编程语言"""
        prompt_lower = prompt.lower()
        if 'python' in prompt_lower:
            return 'python'
        if 'javascript' in prompt_lower or 'js' in prompt_lower:
            return 'javascript'
        return 'generic'

    def _generate_code_example(self, prompt: str, language: str) -> str:
        """生成代码示例"""
        
        # 解析代码任务
        code_tasks = {
            '阶乘': ("factorial", "计算阶乘", "n", "计算n的阶乘，返回n!", "if n <= 1:\\n        return 1\\n    return n * factorial(n-1)", "factorial(n)"),
            '排序': ("sort_list", "列表排序", "lst", "对列表进行快速排序", "return sorted(lst)", "sort_list([3,1,4,1,5])"),
            '斐波那契': ("fibonacci", "斐波那契数列", "n", "返回斐波那契数列前n项", "if n <= 1:\\n        return [1]\\n    result = [1, 1]\\n    for i in range(2, n):\\n        result.append(result[i-1] + result[i-2])\\n    return result", "fibonacci(10)"),
            '反转': ("reverse_string", "字符串反转", "s", "反转输入字符串", "return s[::-1]", 'reverse_string("hello")'),
            '素数': ("is_prime", "判断素数", "n", "判断n是否为素数", "if n < 2:\\n        return False\\n    for i in range(2, int(n**0.5)+1):\\n        if n % i == 0:\\n            return False\\n    return True", "is_prime(17)"),
            '爬虫': ("fetch_webpage", "网页爬取", "url", "获取网页内容", "import urllib.request\\n    with urllib.request.urlopen(url) as response:\\n        return response.read().decode('utf-8')", 'fetch_webpage("https://example.com")'),
            'API': ("call_api", "API调用", "endpoint", "调用REST API", "import requests\\n    response = requests.get(endpoint)\\n    return response.json()", 'call_api("https://api.example.com/data")'),
        }
        
        # 尝试匹配具体任务
        for key, (func_name, desc, param, doc, body, example) in code_tasks.items():
            if key in prompt:
                if language == 'python':
                    return f"""```python
# {desc}

def {func_name}({param}):
    \"\"\"{doc}\"\"\"
    {body}

# 使用示例
result = {example}
print(result)
```"""
                else:
                    return f"""```{language}
// {desc}

function {func_name}({param}) {{
    // {doc}
    // 实现逻辑
    return null; // 返回结果
}}

// 使用示例
const result = {func_name}(/* 参数 */);
console.log(result);
```"""
        
        # 默认代码模板
        if language == 'python':
            return """```python
# Python 代码模板

def your_function(param):
    \"\"\"函数说明\"\"\"
    # 在这里实现您的逻辑
    result = None
    return result

# 使用示例
result = your_function(your_data)
print(result)
```"""
        else:
            return f"""```{language}
// JavaScript 代码模板

function yourFunction(param) {{
    // 在这里实现您的逻辑
    const result = null;
    return result;
}}

// 使用示例
const result = yourFunction(yourData);
console.log(result);
```"""

    def _generate_concept_response(self, topic: str) -> str:
        """生成概念解释"""
        # 尝试精确匹配
        topic_key = topic.lower().replace(' ', '_').replace('-', '_')
        if topic_key in self.topic_definitions:
            info = self.topic_definitions[topic_key]
            template = self.concept_templates[0]
            return template.format(
                topic=topic,
                field=info['field'],
                definition=info['definition'],
                features=info['features'],
                applications=info['applications']
            )
        
        # 通用的解释模板
        return f"""【{topic}】

📌 基本概念：
{topic}是相关领域的重要概念，涉及多个层面的理解和应用。

🔍 核心要点：
• 理解基本定义和原理
• 掌握关键技术要素
• 了解典型应用场景
• 注重实践和经验积累

💡 建议：
深入学习相关理论基础，结合实际案例进行理解。

📚 推荐资源：
建议查阅相关领域的经典著作和最新研究成果。"""

    def _generate_action_response(self, prompt: str) -> str:
        """生成操作指南"""
        topic = self._extract_topic(prompt)
        template = self.action_templates[0]
        return template.format(
            action=topic,
            prep="1. 明确目标和需求\n2. 收集必要资料\n3. 准备工具和环境",
            steps="1. 按步骤执行\n2. 记录关键节点\n3. 及时调整优化",
            notes="1. 注意安全规范\n2. 做好备份\n3. 总结经验教训"
        )

    def _generate_analyze_response(self, prompt: str) -> str:
        """生成分析报告"""
        topic = self._extract_topic(prompt)
        template = self.analyze_templates[0]
        return template.format(
            topic=topic,
            current_state="从多个维度进行现状分析，包括内部因素和外部环境。",
            pros_cons="优势：\n• 核心能力突出\n• 资源积累丰富\n\n劣势：\n• 存在改进空间\n• 需要持续优化",
            recommendations="1. 保持优势领域\n2. 补齐短板\n3. 持续迭代改进"
        )

    def _generate_translate_response(self, prompt: str) -> str:
        """生成翻译响应"""
        # 简单翻译提示
        return f"""【翻译建议】

原文：{prompt}

🌐 翻译要点：
• 保持原意准确
• 符合目标语言习惯
• 注意文化差异

💡 提示：
如需精确翻译，建议使用专业翻译工具或请教专业人士。"""

    def generate(self, prompt: str, **kwargs) -> str:
        """主生成方法"""
        intent = self._detect_intent(prompt)
        
        if intent == 'code':
            lang = self._detect_code_language(prompt)
            return self._generate_code_example(prompt, lang)
        
        elif intent == 'translate':
            return self._generate_translate_response(prompt)
        
        elif intent == 'action':
            return self._generate_action_response(prompt)
        
        elif intent == 'analyze':
            return self._generate_analyze_response(prompt)
        
        else:  # concept
            topic = self._extract_topic(prompt)
            return self._generate_concept_response(topic)


# ============================================================
# 本地LLM引擎 v3.1
# ============================================================

class LocalLLMEngine:
    """
    本地LLM引擎 - A大模型核心
    
    支持模式：
    1. llama-cpp-python (需要安装)
    2. ctransformers (需要安装)
    3. SmartTemplateEngine (内置，无需依赖)
    """

    _instance: Optional['LocalLLMEngine'] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        model_path: Optional[str] = None,
        model_name: str = DEFAULT_MODEL_NAME,
        config: Optional[Dict[str, Any]] = None
    ):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.model_path = model_path or str(DEFAULT_MODEL_DIR / DEFAULT_MODEL_FILE)
        self.model_name = model_name
        self.config = config or {}

        self._state = ServiceState.STOPPED
        self._init_error: Optional[str] = None
        self._load_mode: Optional[LoadMode] = None

        # 加载器
        self._llm = None
        self._ctrans = None
        self._template: Optional[SmartTemplateEngine] = None
        self._model_b = None  # safetensors/Transformers 模型 (B大模型)
        self._tokenizer_b = None  # safetensors/Transformers tokenizer

        # 统计
        self._stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
        }

        self._initialized = True
        logger.info(f"[LocalLLM] Engine v3.1 initialized: {model_name}")

    def start(self, timeout: float = 30.0) -> bool:
        """启动引擎 - 自动尝试各模式 [v4.3 B大模型优先版]
        
        根据model_name自动选择加载策略:
        - gemma4-local-b: 优先safetensors模式 (Transformers直接加载，无Ollama依赖!)
        - llama-3.2-1b-a: 优先本地加载，Ollama作为可选备选
        
        [v4.3] B大模型可独立运行，A大模型可选(需要Ollama或llama-cpp-python)
        """
        with self._lock:
            if self._state == ServiceState.READY:
                return True

            self._state = ServiceState.INITIALIZING
            
            if self.model_name == MODEL_B_NAME:
                logger.info("[LocalLLM] Starting B大模型 (Gemma4, Ollama-free)...")
            else:
                logger.info(f"[LocalLLM] Starting {self.model_name}...")

        last_error = None

        # 根据模型名决定优先加载模式
        if self.model_name == MODEL_B_NAME:
            # B大模型(Gemma4) - [v4.3] 仅使用safetensors，无需Ollama
            llm_modes = [
                (LoadMode.SAFETENSORS, self._start_safetensors),
            ]
        elif self.model_name == DEFAULT_MODEL_NAME:
            # A大模型(Llama) - 优先本地加载，Ollama可选
            llm_modes = [
                (LoadMode.CTRANSFORMERS, self._start_ctransformers),
                (LoadMode.GGUF_DIRECT, self._start_gguf),
                (LoadMode.OLLAMA, self._start_ollama),
            ]
        else:
            # 通用 - 全部尝试（Ollama作为最后备选）
            llm_modes = [
                (LoadMode.CTRANSFORMERS, self._start_ctransformers),
                (LoadMode.GGUF_DIRECT, self._start_gguf),
                (LoadMode.SAFETENSORS, self._start_safetensors),
                (LoadMode.OLLAMA, self._start_ollama),
            ]

        for mode, start_fn in llm_modes:
            try:
                self._load_mode = mode
                start_fn()
                self._state = ServiceState.READY
                self._init_error = None
                logger.info(f"[LocalLLM] Ready! Mode: {mode.value}")
                return True
            except Exception as e:
                last_error = e
                logger.warning(f"[LocalLLM] {mode.value} failed: {e}")
                continue

        # 降级到智能模板引擎
        try:
            self._load_mode = LoadMode.SMART_TEMPLATE
            self._template = SmartTemplateEngine()
            self._state = ServiceState.READY
            self._init_error = None
            logger.info("[LocalLLM] Ready! Mode: smart_template (no dependencies)")
            return True
        except Exception as e:
            self._state = ServiceState.ERROR
            self._init_error = str(e)
            logger.error(f"[LocalLLM] All modes failed: {e}")
            return False

    def _start_ollama(self):
        """连接Ollama服务"""
        import requests
        # 检查Ollama服务是否可用
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            if r.status_code != 200:
                raise ConnectionError("Ollama service not ready")
        except ConnectionError:
            raise
        except requests.Timeout:
            raise ConnectionError("Ollama connection timeout")
        except requests.RequestException as e:
            raise ConnectionError(f"Ollama not available: {e}")

    def _start_gguf(self):
        """加载GGUF (llama-cpp-python)"""
        from llama_cpp import Llama
        model_file = Path(self.model_path)
        if not model_file.exists():
            raise FileNotFoundError(f"Model not found: {model_file}")
        
        self._llm = Llama(
            model_path=str(model_file),
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )

    def _start_ctransformers(self):
        """[v4.2] 加载GGUF (ctransformers) - 无需Ollama!
        
        ctransformers可以直接加载GGUF格式模型，无需Ollama服务。
        适用于A大模型(Llama 3.2 1B)等GGUF格式模型。
        """
        from ctransformers import AutoModelForCausalLM
        
        # 如果model_path是目录，查找GGUF文件
        model_path = Path(self.model_path)
        if model_path.is_dir():
            # 在目录中查找.gguf文件
            gguf_files = list(model_path.glob("*.gguf"))
            if gguf_files:
                model_file = gguf_files[0]  # 使用第一个找到的GGUF文件
            else:
                raise FileNotFoundError(f"No .gguf files found in {model_path}")
        else:
            # 直接是文件路径
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found: {model_path}")
            model_file = model_path
        
        logger.info(f"[LocalLLM] Loading GGUF via ctransformers: {model_file}")
        
        self._ctrans = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id=str(model_file),
            model_type="llama",
            local_files_only=True,
        )
        
        logger.info("[LocalLLM] ctransformers GGUF loaded successfully")

    def _start_safetensors(self):
        """加载safetensors模型 (HuggingFace Transformers)
        
        适用于B大模型(Gemma4等safetensors格式)
        需要依赖: transformers, torch, safetensors
        """
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch
        
        model_dir = Path(self.model_path)
        if not model_dir.exists():
            raise FileNotFoundError(f"Model directory not found: {model_dir}")
        
        # 检查safetensors文件是否存在
        safetensors_files = list(model_dir.glob("*.safetensors"))
        if not safetensors_files:
            raise FileNotFoundError(f"No .safetensors files found in {model_dir}")
        
        # 检查config.json
        if not (model_dir / "config.json").exists():
            raise FileNotFoundError(f"config.json not found in {model_dir}")
        
        logger.info(f"[LocalLLM] Loading safetensors model from {model_dir}...")
        
        # 自动检测设备
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if device == "cuda" else torch.float32
        
        logger.info(f"[LocalLLM] Device: {device}, dtype: {dtype}")
        
        # 加载tokenizer
        self._tokenizer_b = AutoTokenizer.from_pretrained(
            str(model_dir),
            local_files_only=True,
            trust_remote_code=True,
        )
        
        # [v4.3] Gemma4 tokenizer 缺少配置，手动设置 special tokens
        # 根据 config.json: bos_token_id=2, eos_token_id=1, pad_token_id=0
        if self._tokenizer_b.pad_token is None:
            self._tokenizer_b.pad_token = self._tokenizer_b.eos_token
        if self._tokenizer_b.bos_token is None:
            # Gemma4 使用 token_id=2 作为 bos
            self._tokenizer_b.bos_token = self._tokenizer_b.convert_ids_to_tokens(2)
        if self._tokenizer_b.eos_token is None:
            self._tokenizer_b.eos_token = self._tokenizer_b.convert_ids_to_tokens(1)
        
        logger.info(f"[LocalLLM] Tokenizer tokens: bos={self._tokenizer_b.bos_token}, eos={self._tokenizer_b.eos_token}, pad={self._tokenizer_b.pad_token}")
        
        # 加载模型
        self._model_b = AutoModelForCausalLM.from_pretrained(
            str(model_dir),
            local_files_only=True,
            trust_remote_code=True,
            dtype=dtype,
            device_map=device if device == "cuda" else None,
            low_cpu_mem_usage=True,
        )
        
        if device == "cpu":
            self._model_b = self._model_b.to(device)
        
        self._model_b.eval()
        logger.info(f"[LocalLLM] Safetensors model loaded successfully on {device}")

    def stop(self):
        with self._lock:
            if self._state == ServiceState.STOPPED:
                return
            self._llm = None
            self._ctrans = None
            self._template = None
            self._model_b = None
            self._tokenizer_b = None
            self._state = ServiceState.STOPPED

    def restart(self, timeout: float = 30.0) -> bool:
        """
        重启引擎 [v4.1 修复：添加超时保护，避免阻塞]
        
        Args:
            timeout: 启动超时时间（秒），默认30秒
            
        Returns:
            是否成功启动
        """
        self.stop()
        
        # 使用超时保护等待 stop() 完成
        # stop() 有锁保护，通常很快，但以防万一
        start_wait = time.time()
        while self._state != ServiceState.STOPPED:
            if time.time() - start_wait > 5.0:  # 最多等待5秒
                logger.warning("[LocalLLM] stop() 等待超时，强制继续")
                break
            time.sleep(0.1)  # 短暂等待， release GIL
        
        # 使用超时保护启动
        try:
            if timeout > 0:
                # 使用 timeout_utils 的 run_with_timeout
                try:
                    from src.timeout_utils import run_with_timeout
                    logger.info(f"[LocalLLM] 正在重启（启动超时: {timeout}s）...")
                    result = run_with_timeout(self.start, timeout=timeout, description="LocalLLM重启")
                    return result
                except ImportError:
                    # timeout_utils 不可用，直接调用
                    logger.warning("[LocalLLM] timeout_utils 不可用，直接重启")
                    return self.start()
            else:
                return self.start()
        except Exception as e:
            logger.error(f"[LocalLLM] 重启失败: {e}")
            return False

    # ==================== 生成 ====================

    def generate(self, prompt: str, **kwargs) -> GenerationResult:
        """生成回复 [v22.0 + 全路径超时保护]"""
        if self._state != ServiceState.READY:
            if not self.start():
                return GenerationResult(
                    text="[Error] Failed to start engine",
                    model=self.model_name,
                    tokens=0,
                    latency_ms=0,
                    finish_reason="error"
                )

        # [v22.0] 请求级超时，默认120s
        request_timeout = kwargs.pop("request_timeout", 120.0)

        start_time = time.time()
        self._stats["total_requests"] += 1

        def _do_generate() -> str:
            """实际生成逻辑（在线程池中执行，可被超时中断）"""
            if self._load_mode == LoadMode.OLLAMA:
                return self._generate_ollama(prompt, **kwargs)
            elif self._load_mode == LoadMode.GGUF_DIRECT:
                return self._generate_llm(prompt, **kwargs)
            elif self._load_mode == LoadMode.CTRANSFORMERS:
                return self._generate_ctrans(prompt, **kwargs)
            elif self._load_mode == LoadMode.SAFETENSORS:
                return self._generate_safetensors(prompt, **kwargs)
            else:
                return self._template.generate(prompt, **kwargs)

        try:
            from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

            # [v22.0] 用线程池+future实现统一超时，覆盖所有4条路径
            with ThreadPoolExecutor(max_workers=1, thread_name_prefix="llm_gen") as executor:
                future = executor.submit(_do_generate)
                text = future.result(timeout=request_timeout)

            self._stats["successful_requests"] += 1

            return GenerationResult(
                text=text,
                model=self.model_name,
                tokens=len(text.split()),
                latency_ms=(time.time() - start_time) * 1000,
                finish_reason="stop"
            )

        except FuturesTimeout:
            self._stats["failed_requests"] += 1
            latency = (time.time() - start_time) * 1000
            return GenerationResult(
                text=f"[Timeout] LLM generation exceeded {request_timeout:.0f}s",
                model=self.model_name,
                tokens=0,
                latency_ms=latency,
                finish_reason="timeout",
                error=f"timeout after {request_timeout:.0f}s"
            )

        except Exception as e:
            self._stats["failed_requests"] += 1
            error_msg = str(e)
            logger.error(f"[LocalLLM] Generation error: {error_msg}")
            return GenerationResult(
                text=f"[Error] {error_msg}",
                model=self.model_name,
                tokens=0,
                latency_ms=(time.time() - start_time) * 1000,
                finish_reason="error",
                error=error_msg,
            )

    def _generate_ollama(self, prompt: str, **kwargs) -> str:
        import requests
        max_tokens = kwargs.get("max_new_tokens", 256)
        temp = kwargs.get("temperature", 0.7)
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama-3.2-1b-a",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temp,
                }
            },
            timeout=120
        )
        if response.status_code != 200:
            raise RuntimeError(f"Ollama error: {response.text}")
        return response.json().get("response", "").strip()

    def _generate_llm(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_new_tokens", 256)
        temp = kwargs.get("temperature", 0.7)
        
        response = self._llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temp,
            stop=["</s>", "User:", "Human:"],
            echo=False
        )
        return response["choices"][0]["text"].strip()

    def _generate_ctrans(self, prompt: str, **kwargs) -> str:
        """[v4.2] 使用ctransformers生成 - 无需Ollama"""
        max_tokens = kwargs.get("max_new_tokens", 256)
        temp = kwargs.get("temperature", 0.7)
        
        # [v4.2] 改进Llama提示词格式
        full_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        text = self._ctrans.generate(
            full_prompt,
            max_new_tokens=max_tokens,
            temperature=temp if temp > 0 else 0.7,
        )
        
        # 清理输出
        if full_prompt in text:
            text = text[len(full_prompt):].strip()
        
        # 移除可能的结束标记
        text = text.split("<|im_end|>")[0].strip()
        
        return text.strip() if text else "[Empty response]"

    def _generate_safetensors(self, prompt: str, **kwargs) -> str:
        """[v4.3] 使用safetensors/Transformers模型生成 (B大模型)"""
        import torch
        
        max_tokens = kwargs.get("max_new_tokens", 256)
        temp = kwargs.get("temperature", 0.7)
        
        # 构建输入 - Gemma4 没有 chat_template，直接使用简单方式
        # [v4.3] 修复: Gemma4 tokenizer 没有 chat_template
        tokenizer = self._tokenizer_b
        
        # 尝试使用chat_template，如果不存在则使用简单prompt格式
        if hasattr(tokenizer, 'chat_template') and tokenizer.chat_template:
            messages = [{"role": "user", "content": prompt}]
            inputs = tokenizer.apply_chat_template(
                messages, 
                return_tensors="pt",
                add_generation_prompt=True,
            )
        else:
            # Gemma4 格式: 直接使用简单prompt
            # Gemma4 使用特殊的对话格式
            full_prompt = f"User: {prompt}\nModel:"
            inputs = tokenizer(full_prompt, return_tensors="pt", add_special_tokens=True)
        
        # 移到模型所在设备
        device = next(self._model_b.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # [v4.3] Gemma4 生成参数优化
        eos_id = self._tokenizer_b.eos_token_id
        if isinstance(eos_id, list):
            eos_id = eos_id[0]
        
        generation_kwargs = {
            "max_new_tokens": max_tokens,
            "do_sample": temp > 0,
            "pad_token_id": eos_id,
            "eos_token_id": eos_id,
            # [v4.3] 高重复惩罚防止循环
            "repetition_penalty": 1.5,
        }
        
        if temp > 0:
            generation_kwargs["temperature"] = temp
            generation_kwargs["top_p"] = 0.9
        
        with torch.no_grad():
            outputs = self._model_b.generate(
                **inputs,
                **generation_kwargs,
            )
        
        # 解码，只取新生成的部分
        input_len = inputs["input_ids"].shape[1] if "input_ids" in inputs else 0
        generated_ids = outputs[0][input_len:]
        text = self._tokenizer_b.decode(generated_ids, skip_special_tokens=True)
        
        return text.strip()

    def chat(self, message: str, **kwargs) -> str:
        result = self.generate(message, **kwargs)
        return result.text

    # ==================== 属性 ====================

    @property
    def state(self) -> ServiceState:
        return self._state

    @property
    def is_ready(self) -> bool:
        return self._state == ServiceState.READY

    @property
    def load_mode(self) -> Optional[str]:
        return self._load_mode.value if self._load_mode else None

    @property
    def model_info(self) -> Dict[str, Any]:
        return {
            "name": self.model_name,
            "path": self.model_path,
            "state": self._state.value,
            "mode": self.load_mode,
        }

    def get_stats(self) -> Dict[str, Any]:
        stats = self._stats.copy()
        if stats["total_requests"] > 0:
            stats["success_rate"] = stats["successful_requests"] / stats["total_requests"]
        return stats

    def __repr__(self):
        return f"LocalLLMEngine({self.model_name}, {self._state.value}, {self.load_mode})"


# ============================================================
# 全局
# ============================================================

_global_engine: Optional[LocalLLMEngine] = None
_global_engine_b: Optional[LocalLLMEngine] = None


def get_engine(**kwargs) -> LocalLLMEngine:
    global _global_engine
    if _global_engine is None:
        _global_engine = LocalLLMEngine(**kwargs)
    return _global_engine


def get_engine_b(**kwargs) -> LocalLLMEngine:
    """获取B大模型引擎 (Gemma4 safetensors)"""
    global _global_engine_b
    if _global_engine_b is None:
        kwargs.setdefault("model_path", str(MODEL_B_DIR))
        kwargs.setdefault("model_name", MODEL_B_NAME)
        _global_engine_b = LocalLLMEngine(**kwargs)
    return _global_engine_b


def shutdown_engine():
    global _global_engine
    if _global_engine:
        _global_engine.stop()
        _global_engine = None


def shutdown_engine_b():
    """关闭B大模型引擎"""
    global _global_engine_b
    if _global_engine_b:
        _global_engine_b.stop()
        _global_engine_b = None


def chat(message: str, **kwargs) -> str:
    return get_engine().chat(message, **kwargs)


def chat_b(message: str, **kwargs) -> str:
    """使用B大模型聊天"""
    return get_engine_b().chat(message, **kwargs)


def generate(prompt: str, **kwargs) -> GenerationResult:
    return get_engine().generate(prompt, **kwargs)


def generate_b(prompt: str, **kwargs) -> GenerationResult:
    """使用B大模型生成"""
    return get_engine_b().generate(prompt, **kwargs)


__all__ = [
    "LocalLLMEngine",
    "GenerationResult",
    "ServiceState",
    "LoadMode",
    "SmartTemplateEngine",
    "get_engine",
    "get_engine_b",
    "shutdown_engine",
    "shutdown_engine_b",
    "chat",
    "chat_b",
    "generate",
    "generate_b",
    "DEFAULT_MODEL_NAME",
    "MODEL_B_NAME",
    "MODEL_B_DIR",
]
