# Somn 安全策略

## 概述

本文档定义了Somn项目的安全策略和最佳实践。

## 安全原则

### 1. 数据隔离

- **本地存储**: 所有项目数据仅存储在本地
- **无云上传**: 禁止将用户数据上传到外部云服务
- **加密存储**: 敏感数据使用加密存储

### 2. 凭证管理

- **环境变量**: 所有凭证存储在环境变量中
- **无硬编码**: 禁止在代码中硬编码任何凭证
- **定期轮换**: API密钥等定期更换

### 3. 访问控制

```python
class AccessLevel(Enum):
    PUBLIC = 0      # 可公开分享
    INTERNAL = 1    # 项目成员
    RESTRICTED = 2  # 特定角色
    CONFIDENTIAL = 3 # 敏感数据
```

### 4. 审计日志

所有敏感操作必须记录：
- 用户认证
- 数据访问
- 配置变更
- 系统错误

## 保护数据目录

以下目录包含敏感数据，禁止上传到任何公共存储：

```yaml
protected_directories:
  - data/memory_v2/         # 个人记忆
  - data/q_values/          # 学习数据
  - data/learning/          # 学习记录
  - data/solution_learning/ # 解决方案
  - data/memory/            # 记忆系统
  - data/feedback_production/ # 用户反馈
  - data/feedback_loop/     # 反馈循环
  - data/reasoning/         # 推理记录
  - data/ml/roi*            # ROI数据
```

## 安全扫描

### 运行扫描

```bash
# 基础扫描
python security_scan.py --path .

# 完整扫描
python security_scan.py --path . --full

# 输出报告
python security_scan.py --path . --output security_report.json
```

### 扫描类型

| 扫描 | 说明 | 优先级 |
|------|------|--------|
| 硬编码凭证 | 检测密码、API密钥、Token | HIGH |
| SQL注入 | 检查SQL拼接模式 | HIGH |
| 代码执行 | 检测eval/exec使用 | HIGH |
| 文件操作 | 不安全文件操作 | MEDIUM |
| 依赖漏洞 | 检查已知漏洞包 | HIGH |

## 敏感信息处理

### 日志脱敏

```python
import re

def sanitize_log(message: str) -> str:
    """Remove sensitive information from logs."""
    patterns = [
        (r'password[=:]\s*["\']?[^"\'\s]+["\']?', 'password=***'),
        (r'token[=:]\s*["\']?[^"\'\s]+["\']?', 'token=***'),
        (r'api[_-]?key[=:]\s*["\']?[^"\'\s]+["\']?', 'api_key=***'),
    ]

    for pattern, replacement in patterns:
        message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)

    return message
```

### 错误处理

```python
def handle_error(error: Exception, context: dict) -> dict:
    """Safe error handling - don't expose sensitive details."""
    return {
        "error": type(error).__name__,
        "message": "An error occurred",  # Generic message
        "reference_id": generate_error_id(),  # For support
    }
```

## 权限最小化

### 模块间依赖

- 只导入必需的模块
- 使用接口而非具体实现
- 避免循环依赖

### 公共API

- 最小化公共接口
- 输入验证所有参数
- 文档说明安全边界

### 异常信息

```python
# 错误示例
raise ValueError(f"Invalid API key: {api_key}")  # 泄露信息

# 正确示例
raise ValueError("Invalid credentials")  # 不泄露细节
```

## 合规检查

### 提交前检查

```bash
# 运行安全扫描
python security_scan.py --path .

# 检查凭证
git diff --staged | grep -E "(password|api_key|secret|token)"

# 运行bandit
bandit -r smart_office_assistant/
```

### CI/CD集成

安全扫描在CI/CD中自动运行：
- 每次PR必须通过安全扫描
- HIGH级别问题阻止合并
- MEDIUM/LOW级别警告

## 漏洞报告

发现安全漏洞？请：

1. 不要在公开Issue中报告
2. 发送邮件到 security@example.com
3. 包含：
   - 漏洞描述
   - 复现步骤
   - 影响评估
   - 建议修复方案

## 安全更新

安全更新优先级：
- **CRITICAL**: 24小时内修复
- **HIGH**: 7天内修复
- **MEDIUM**: 30天内修复
- **LOW**: 下个版本修复

## 培训

开发者必须了解：
- OWASP Top 10
- 安全编码规范
- 凭证管理最佳实践
- 隐私保护法规

---

*最后更新: 2026-04-24*