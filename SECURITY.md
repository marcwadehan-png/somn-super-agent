# Security Policy

## Supported Versions

| 版本 | 支持状态 |
|------|----------|
| v6.x (当前) | ✅ 活跃维护（安全更新） |
| v5.x | ⚠️ 仅关键安全修复 |

## Reporting a Vulnerability

如果你发现安全漏洞，**请勿公开 Issue**。请通过以下方式私密报告：

1. **GitHub Private Advisory**: 使用 GitHub 的 [Security Advisory](https://github.com/marcwadehan-png/somn-agent/security/advisories/new) 功能提交
2. **Email**: 发送邮件至项目维护者

报告内容请包含：
- 漏洞类型和描述
- 影响范围（受影响版本）
- 复现步骤
- 潜在的影响评估
- 如有修复建议也欢迎提供

## 响应承诺

| 阶段 | 时间线 |
|------|--------|
| 确认收到 | 48 小时内 |
| 初步评估 | 7 天内 |
| 修复方案 | 严重漏洞 14 天内，中低风险 30 天内 |
| 公开披露 | 修复发布后 |

## 安全架构概述

Somn 采用了多层安全策略：

### 1. 数据隔离
- 用户数据存储在独立的 SQLite 实例中
- 多用户场景下使用 session 隔离
- API Key 和凭证不存储在代码库中

### 2. API 认证
```
server:
  api_key: ""    # 为空时不启用认证
                  # 生产环境建议设置强密码
```

### 3. 输入验证 & 防护
- **SQL 注入**: 使用参数化查询，ORM 层防护
- **XSS**: FastAPI 自动转义 + 自定义中间件
- **eval/exec 安全**: 禁用直接 eval，使用 AST 解析器沙箱
- **路径遍历**: `pathlib` 规范化 + 白名单校验
- **命令注入**: subprocess 使用 list 参数（非字符串拼接）

### 4. 依赖安全
- CI 流水线集成 `bandit` (SAST) + `safety` (依赖检查)
- 定期审计第三方依赖版本

## 安全 Checklist（开源前）

在部署到生产环境前，请确认：

- [ ] 设置了 `server.api_key`（非空值）
- [ ] 更换了默认端口（如需要）
- [ ] 配置了 CORS 白名单（当前为 `*`）
- [ ] 启用了 `storage.security.encryption`
- [ ] 配置了 HTTPS 反向代理
- [ ] 定期备份数据（藏书阁备份已内置）

## 已知安全限制

| 项目 | 说明 | 缓解措施 |
|------|------|----------|
| 本地模型加载 | safetensors 文件需信任来源 | 仅从 HuggingFace 官方下载 |
| Web Search 功能 | 默认关闭 | `features.enable_web_search: false` |
| Ollama 绑定 | 仅监听 127.0.0.1 | 不对外暴露 |
