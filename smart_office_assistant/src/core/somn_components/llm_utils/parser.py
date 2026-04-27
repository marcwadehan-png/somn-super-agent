"""
__all__ = [
    'call_for_json',
    'clear_session_cache',
    'get_cache_size',
    'safe_industry_type',
]

LLM解析器 - 提供LLM调用和JSON解析能力
"""

import logging
import re
from typing import Dict, Any, Optional, Callable

logger = logging.getLogger(__name__)

class LLMParser:
    """LLM解析器封装类"""

    def __init__(self, llm=None):
        """
        Args:
            llm: LLM实例
        """
        self._llm = llm
        self._session_cache: Dict[str, Any] = {}

    def call_for_json(
        self,
        prompt: str,
        system_prompt: str = "",
        json_schema: str = "",
        timeout: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        调用 LLM 并尽量解析 JSON

        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            json_schema: JSON Schema 描述
            timeout: 超时秒数

        Returns:
            解析后的JSON或None
        """
        if not self._llm:
            return None

        # 构建缓存键
        cache_key = self._make_cache_key(prompt, system_prompt)

        # 检查会话缓存
        if cache_key in self._session_cache:
            logger.info(f"[LLM缓存命中] {cache_key[:32]}...")
            return self._session_cache[cache_key]

        try:
            full_prompt = prompt
            if json_schema:
                full_prompt = f"{prompt}\n\n请严格按照以下JSON格式返回:\n{json_schema}"

            result = self._llm.generate(full_prompt, system_prompt=system_prompt)

            if result:
                json_data = self._extract_json_payload(result)
                if json_data:
                    self._session_cache[cache_key] = json_data
                    # 限制缓存大小
                    if len(self._session_cache) > 200:
                        oldest = next(iter(self._session_cache))
                        del self._session_cache[oldest]
                    return json_data

        except Exception as e:
            logger.warning(f"LLM调用失败: {e}")

        return None

    def _make_cache_key(self, prompt: str, system_prompt: str) -> str:
        """生成缓存键"""
        import hashlib
        key_str = f"{prompt[:256]}|{system_prompt[:256]}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def _extract_json_payload(self, text: str) -> Optional[Dict[str, Any]]:
        """
        从模型文本中提取 JSON

        Args:
            text: 模型输出文本

        Returns:
            解析后的JSON或None
        """
        import json

        # 方法1: 尝试直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 方法2: 提取 ```json ... ``` 块
        json_blocks = re.findall(r'```(?:json)?\s*([\s\S]*?)\s*```', text, re.MULTILINE)
        for block in json_blocks:
            try:
                return json.loads(block.strip())
            except json.JSONDecodeError:
                continue

        # 方法3: 提取 {...} 或 [...] 块
        for match in re.finditer(r'\{[\s\S]*\}', text):
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                continue

        for match in re.finditer(r'\[[\s\S]*\]', text):
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                continue

        return None

    def safe_industry_type(self, industry: str) -> Optional[Any]:
        """
        安全转换行业枚举

        Args:
            industry: 行业字符串

        Returns:
            IndustryType枚举或None
        """
        try:
            # 延迟导入避免循环依赖
            from src.industry_engine import IndustryType
            return IndustryType(industry)
        except Exception:
            return None

    def clear_session_cache(self):
        """清除会话缓存"""
        self._session_cache.clear()

    def get_cache_size(self) -> int:
        """获取缓存大小"""
        return len(self._session_cache)
