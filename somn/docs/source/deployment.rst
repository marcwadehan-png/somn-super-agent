# Somn 部署手册 v6.1

## 部署环境

### 基础设施要求

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 4核 | 8核 |
| 内存 | 8GB | 16GB |
| 磁盘 | 10GB | 50GB |
| OS | Windows Server 2019 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

### 依赖服务

- Python 3.10+
- 至少1个LLM模型文件

## 本地部署

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. 模型准备

```bash
# 下载模型到 models/ 目录
mkdir -p models
# 根据你的配置放置模型文件
```

### 3. 配置

```bash
# 复制并编辑配置
cp config/config.example.yaml config/config.yaml
# 编辑 config.yaml 设置模型路径
```

### 4. 验证部署

```bash
# 运行测试
pytest tests/ -v

# 启动服务
python start_independent.py
```

## Docker部署

### Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "start_independent.py"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t somn:latest .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -v ./data:/app/data \
  -v ./models:/app/models \
  --name somn \
  somn:latest
```

## 生产环境配置

### 环境变量

```bash
# .env file
SOMN_ENV=production
SOMN_LOG_LEVEL=INFO
SOMN_DATA_DIR=/data/somn
SOMN_MODEL_PATH=/models/llama-3b
SOMN_MAX_MEMORY_GB=16
```

### 日志配置

```yaml
# logging.yaml
version: 1
formatters:
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  file:
    class: logging.handlers.RotatingFileHandler
    filename: logs/somn.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
  console:
    class: logging.StreamHandler
    level: INFO
root:
  level: INFO
  handlers: [console, file]
```

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/health

# 预期响应
{"status": "healthy", "version": "6.1.0"}
```

## 监控配置

### Prometheus 指标

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'somn'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Somn Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [{"expr": "rate(somn_requests_total[5m])"}]
      },
      {
        "title": "Latency P95",
        "type": "graph",
        "targets": [{"expr": "histogram_quantile(0.95, somn_latency_seconds)"}]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [{"expr": "rate(somn_errors_total[5m])"}]
      }
    ]
  }
}
```

## 备份策略

### 数据备份

```bash
# 每日备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR=/backups/somn

# 备份数据目录
tar -czf $BACKUP_DIR/data_$DATE.tar.gz data/

# 备份配置
cp config/config.yaml $BACKUP_DIR/config_$DATE.yaml

# 保留最近30天
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### 恢复流程

```bash
# 停止服务
systemctl stop somn

# 恢复数据
tar -xzf /backups/somn/data_20260424.tar.gz -C /

# 重启服务
systemctl start somn
```

## 故障排查

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 导入错误 | PYTHONPATH未设置 | 设置 `export PYTHONPATH=.` |
| 模型未找到 | 路径错误 | 检查 config.yaml 模型路径 |
| 内存不足 | 数据太大 | 减少 max_size_gb |
| 测试失败 | 依赖未安装 | `pip install -r requirements-dev.txt` |

### 日志查看

```bash
# 查看最近日志
tail -f logs/somn.log

# 搜索错误
grep -i error logs/somn.log | tail -20

# 查看特定模块日志
grep -i wisdom logs/somn.log
```

## 安全配置

### 防火墙规则

```bash
# 只允许必要端口
ufw allow 22/tcp   # SSH
ufw allow 8000/tcp # API
ufw enable
```

### SSL/TLS配置

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name somn.example.com;

    ssl_certificate /etc/ssl/certs/somn.crt;
    ssl_certificate_key /etc/ssl/private/somn.key;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

## 升级流程

### 小版本升级 (v6.1 → v6.2)

```bash
# 拉取最新代码
git pull

# 更新依赖
pip install -r requirements.txt

# 运行迁移脚本（如有）
python scripts/migrate_v6_1_to_v1_0.py

# 重启服务
systemctl restart somn
```

### 大版本升级 (v6.x → v7.0)

1. 备份所有数据
2. 阅读升级指南
3. 运行兼容性测试
4. 逐模块升级
5. 验证功能

---

*最后更新: 2026-04-24*