"""
__all__ = [
    'anonymize_dict',
    'anonymize_logs',
    'decrypt_data',
    'encrypt_data',
    'get_obfuscation_stats',
    'hash_data',
    'obfuscate_user_data',
]

数据混淆器 - Data Obfuscator
实现说明:
"在宇宙中,暴露即死亡" - 最小化数据暴露,实现隐藏即安全

核心哲学:
1. 隐藏即安全:数据不暴露就不可能被攻击
2. 最小化攻击面:只暴露必要信息
3. 深度防御:多层混淆,即使一层被突破也不暴露全部
4. 可逆性:必要时可恢复,但需要密钥
"""

import hashlib
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logger.warning("cryptography未安装,加密功能将受限")

class ObfuscationLevel(Enum):
    """混淆级别"""
    NONE = "none"           # 不混淆
    LOW = "low"             # 低级混淆 - 部分隐藏
    MEDIUM = "medium"       # 中级混淆 - 大部分隐藏
    HIGH = "high"           # 高级混淆 - 完全隐藏
    EXTREME = "extreme"     # 极端混淆 - 加密+混淆

@dataclass
class ObfuscationResult:
    """混淆结果"""
    original_data: Any
    obfuscated_data: Any
    obfuscation_level: ObfuscationLevel
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

class DataObfuscator:
    """
    数据混淆器 - 实现数据隐蔽性
    
    基于<三体>黑暗森林法则:
    - 宇宙是黑暗的森林,暴露即死亡
    - 对于AI系统,数据暴露即风险
    - 最小化暴露,最大化隐藏
    
    功能:
    1. 用户数据混淆 - 隐藏敏感信息
    2. 日志匿名化 - 移除可recognize信息
    3. 数据脱敏 - 部分隐藏关键信息
    4. 数据加密 - 端到端加密
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.enabled = self.config.get('obfuscation_enabled', True)
        self.obfuscation_level = ObfuscationLevel(
            self.config.get('obfuscation_level', 'medium')
        )
        
        # 敏感字段模式
        self.sensitive_patterns = {
            'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            'phone': re.compile(r'1[3-9]\d{9}'),
            'id_card': re.compile(r'\d{17}[\dXx]'),
            'ip_address': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            'credit_card': re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
        }
        
        # init加密器
        self._init_encryption()
        
        logger.info(f"数据混淆器init完成 - 级别: {self.obfuscation_level}")
    
    def _init_encryption(self):
        """init加密器"""
        if not CRYPTO_AVAILABLE:
            self.fernet = None
            logger.warning("加密功能不可用")
            return
        
        encryption_key = self.config.get('encryption_key')
        if not encryption_key:
            # generate随机密钥
            self.fernet = Fernet.generate_key()
            logger.info("generate新的加密密钥")
        else:
            # 使用提供的密钥
            key = encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
            try:
                self.fernet = Fernet(key)
                logger.info("使用提供的加密密钥")
            except Exception as e:
                logger.error(f"加密密钥init失败: {e}")
                self.fernet = None
    
    def obfuscate_user_data(self, data: Dict) -> ObfuscationResult:
        """
        混淆用户数据
        
        基于<三体>:隐藏是生存的第一原则
        
        strategy:
        1. 根据混淆级别选择混淆strategy
        2. 对敏感字段进行混淆
        3. 对个人信息进行部分隐藏
        4. 对关键字段进行加密
        
        Args:
            data: 原始用户数据
            
        Returns:
            ObfuscationResult: 混淆结果
        """
        if not self.enabled:
            return ObfuscationResult(data, data, ObfuscationLevel.NONE)
        
        obfuscated = data.copy()
        metadata = {}
        
        # 混淆姓名
        if 'name' in obfuscated:
            obfuscated['name'], name_metadata = self._obfuscate_name(obfuscated['name'])
            metadata['name'] = name_metadata
        
        # 混淆邮箱
        if 'email' in obfuscated:
            obfuscated['email'], email_metadata = self._obfuscate_email(obfuscated['email'])
            metadata['email'] = email_metadata
        
        # 混淆手机号
        if 'phone' in obfuscated:
            obfuscated['phone'], phone_metadata = self._obfuscate_phone(obfuscated['phone'])
            metadata['phone'] = phone_metadata
        
        # 混淆身份证
        if 'id_card' in obfuscated:
            obfuscated['id_card'], id_metadata = self._obfuscate_id_card(obfuscated['id_card'])
            metadata['id_card'] = id_metadata
        
        # 混淆地址
        if 'address' in obfuscated:
            obfuscated['address'], address_metadata = self._obfuscate_address(obfuscated['address'])
            metadata['address'] = address_metadata
        
        return ObfuscationResult(
            original_data=data,
            obfuscated_data=obfuscated,
            obfuscation_level=self.obfuscation_level,
            metadata=metadata
        )
    
    def _obfuscate_name(self, name: str) -> Tuple[str, Dict]:
        """混淆姓名"""
        if len(name) <= 1:
            return name, {'obfuscated': False}
        
        # 中文字符:保留姓,隐藏名
        if self._is_chinese(name):
            return name[0] + '*', {'obfuscated': True, 'method': 'partial'}
        # 英文字符:保留首字母
        else:
            return name[0] + '*' * (len(name) - 1), {'obfuscated': True, 'method': 'partial'}
    
    def _obfuscate_email(self, email: str) -> Tuple[str, Dict]:
        """混淆邮箱"""
        if '@' not in email:
            return email, {'obfuscated': False}
        
        username, domain = email.split('@')
        
        if len(username) <= 2:
            obfuscated_username = '*' * len(username)
        else:
            obfuscated_username = username[0] + '*' * (len(username) - 2) + username[-1]
        
        return f"{obfuscated_username}@{domain}", {'obfuscated': True, 'method': 'partial'}
    
    def _obfuscate_phone(self, phone: str) -> Tuple[str, Dict]:
        """混淆手机号"""
        # 保留前3位和后2位
        if len(phone) < 7:
            return phone, {'obfuscated': False}
        
        return phone[:3] + '*' * (len(phone) - 5) + phone[-2:], {'obfuscated': True, 'method': 'partial'}
    
    def _obfuscate_id_card(self, id_card: str) -> Tuple[str, Dict]:
        """混淆身份证"""
        if len(id_card) < 10:
            return id_card, {'obfuscated': False}
        
        return id_card[:3] + '*' * (len(id_card) - 6) + id_card[-3:], {'obfuscated': True, 'method': 'partial'}
    
    def _obfuscate_address(self, address: str) -> Tuple[str, Dict]:
        """混淆地址"""
        # 保留省级信息,隐藏详细地址
        parts = address.split('省' if '省' in address else '市')
        if len(parts) > 1:
            return parts[0] + '省**', {'obfuscated': True, 'method': 'partial'}
        return address[:2] + '**', {'obfuscated': True, 'method': 'partial'}
    
    def _is_chinese(self, text: str) -> bool:
        """judge是否为中文字符"""
        return any('\u4e00' <= char <= '\u9fff' for char in text)
    
    def anonymize_logs(self, log_data: str) -> str:
        """
        匿名化日志
        
        基于<三体>:在宇宙中,暴露位置即暴露生存
        对于日志,暴露用户信息即暴露隐私
        
        strategy:
        1. 移除IP地址
        2. 移除用户标识
        3. 移除敏感关键词
        4. 替换为通用标识符
        
        Args:
            log_data: 原始日志
            
        Returns:
            匿名化后的日志
        """
        if not self.enabled:
            return log_data
        
        anonymized = log_data
        
        # 移除IP地址
        anonymized = self.sensitive_patterns['ip_address'].sub('[IP_REDACTED]', anonymized)
        
        # 移除邮箱
        anonymized = self.sensitive_patterns['email'].sub('[EMAIL_REDACTED]', anonymized)
        
        # 移除手机号
        anonymized = self.sensitive_patterns['phone'].sub('[PHONE_REDACTED]', anonymized)
        
        # 移除身份证号
        anonymized = self.sensitive_patterns['id_card'].sub('[ID_REDACTED]', anonymized)
        
        # 移除银行卡号
        anonymized = self.sensitive_patterns['credit_card'].sub('[CARD_REDACTED]', anonymized)
        
        # 移除常见敏感关键词(如密码,token等)
        sensitive_keywords = ['password', 'token', 'secret', 'api_key', 'access_token']
        for keyword in sensitive_keywords:
            pattern = re.compile(rf'{keyword}["\']?\s*[:=]\s*["\']?[^"\'\s]+["\']?', re.IGNORECASE)
            anonymized = pattern.sub(f'{keyword}=[REDACTED]', anonymized)
        
        return anonymized
    
    def encrypt_data(self, data: Any) -> Tuple[Optional[bytes], Optional[str]]:
        """
        加密数据
        
        基于<三体>:只有隐藏,才能生存
        
        Args:
            data: 要加密的数据
            
        Returns:
            (加密后的数据, 错误信息)
        """
        if not self.enabled or self.fernet is None:
            return None, "加密功能不可用"
        
        try:
            # 将数据序列化为JSON
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            
            # 加密
            encrypted = self.fernet.encrypt(json_data)
            
            return encrypted, None
        except Exception as e:
            logger.error(f"数据加密失败: {e}")
            return None, "数据加密失败"
    
    def decrypt_data(self, encrypted_data: bytes) -> Tuple[Optional[Any], Optional[str]]:
        """
        解密数据
        
        Args:
            encrypted_data: 加密的数据
            
        Returns:
            (解密后的数据, 错误信息)
        """
        if not self.enabled or self.fernet is None:
            return None, "解密功能不可用"
        
        try:
            # 解密
            decrypted = self.fernet.decrypt(encrypted_data)
            
            # 反序列化
            data = json.loads(decrypted.decode('utf-8'))
            
            return data, None
        except Exception as e:
            logger.error(f"数据解密失败: {e}")
            return None, "数据解密失败"
    
    def hash_data(self, data: str, salt: Optional[str] = None) -> str:
        """
        哈希数据 - 不可逆
        
        基于<三体>:有些信息应该永远消失
        
        Args:
            data: 要哈希的数据
            salt: 盐值(可选)
            
        Returns:
            哈希值
        """
        if salt:
            data = f"{salt}{data}"
        
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def anonymize_dict(self, data: Dict, sensitive_keys: List[str]) -> Dict:
        """
        匿名字典中的敏感字段
        
        Args:
            data: 原始字典
            sensitive_keys: 敏感字段列表
            
        Returns:
            匿名化后的字典
        """
        if not self.enabled:
            return data
        
        anonymized = data.copy()
        
        for key in sensitive_keys:
            if key in anonymized:
                if isinstance(anonymized[key], str):
                    # 字符串:部分隐藏
                    value = anonymized[key]
                    if len(value) > 4:
                        anonymized[key] = value[:2] + '*' * (len(value) - 4) + value[-2:]
                    else:
                        anonymized[key] = '*' * len(value)
                elif isinstance(anonymized[key], (int, float)):
                    # 数字:转换为哈希
                    anonymized[key] = self.hash_data(str(anonymized[key]))[:8]
        
        return anonymized
    
    def get_obfuscation_stats(self, data: Dict) -> Dict[str, int]:
        """
        get混淆统计信息
        
        Args:
            data: 原始数据
            
        Returns:
            统计信息
        """
        result = self.obfuscate_user_data(data)
        
        total_fields = len(data)
        obfuscated_fields = sum(1 for k, v in result.metadata.items() if v.get('obfuscated'))
        
        return {
            'total_fields': total_fields,
            'obfuscated_fields': obfuscated_fields,
            'obfuscation_rate': obfuscated_fields / total_fields if total_fields > 0 else 0,
            'obfuscation_level': result.obfuscation_level.value
        }

# 测试代码
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
