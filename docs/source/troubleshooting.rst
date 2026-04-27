# Somn 故障排查手册 v6.1

## 快速诊断

当遇到问题时，按以下顺序检查：

```
1. 服务是否运行？
2. 配置是否正确？
3. 依赖是否安装？
4. 日志有无错误？
5. 测试是否通过？
```

## 常见问题

### 1. 导入错误 (ImportError)

**症状**:
```
ModuleNotFoundError: No module named 'smart_office_assistant'
```

**解决方案**:
```bash
# 方法1: 设置PYTHONPATH
export PYTHONPATH=.

# 方法2: 安装为开发包
pip install -e .

# 方法3: 使用项目引导
python path_bootstrap.py
```

### 2. 模型未找到

**症状**:
```
FileNotFoundError: Model not found at path/to/model
```

**解决方案**:
1. 检查 `config/config.yaml` 中的 `model_path`
2. 确认模型文件存在
3. 检查文件权限

```bash
ls -la path/to/model
```

### 3. 内存不足

**症状**:
```
MemoryError: Unable to allocate array
```

**解决方案**:
```yaml
# config.yaml
memory:
  max_size_gb: 8  # 减少内存使用

# 或清理旧数据
python scripts/cleanup_memory.py --keep-days 7
```

### 4. 测试失败

**症状**:
```
FAILED tests/test_xxx.py::test_yyy
```

**解决方案**:
```bash
# 查看详细错误
pytest tests/test_xxx.py::test_yyy -v

# 检查依赖
pip install -r requirements-dev.txt

# 清理缓存
rm -rf .pytest_cache tests/.pytest_cache
pytest tests/ -v --cache-clear
```

### 5. 性能问题

**症状**:
- 响应时间过长
- CPU/内存占用过高

**诊断**:
```bash
# 运行性能测试
pytest tests/test_performance.py -v --benchmark-only

# 查看热点
python -m cProfile -o output.prof your_script.py
python -m pstats output.prof
```

## 错误代码

| 代码 | 含义 | 解决方案 |
|------|------|----------|
| E001 | 导入失败 | 检查PYTHONPATH |
| E002 | 模型未找到 | 检查model_path |
| E003 | 配置错误 | 验证YAML语法 |
| E004 | 权限不足 | 检查文件权限 |
| E005 | 内存不足 | 减少max_size_gb |
| E010 | 超时 | 增加timeout值 |
| E011 | 网络错误 | 检查网络连接 |
| E020 | 推理引擎错误 | 查看日志详情 |

## 日志分析

### 日志位置

```bash
# 默认日志位置
logs/somn.log

# pytest日志
tests/.pytest_cache/
```

### 常用日志命令

```bash
# 查看最近的错误
grep -i error logs/somn.log | tail -50

# 查看特定模块日志
grep -i "wisdom_dispatch" logs/somn.log

# 查看某个时间段的日志
grep "2026-04-24 10:" logs/somn.log

# 统计错误类型
grep -i error logs/somn.log | awk '{print $5}' | sort | uniq -c
```

### 日志级别

```python
# 设置日志级别
import logging
logging.basicConfig(level=logging.DEBUG)

# 各模块独立设置
logging.getLogger('smart_office_assistant.core').setLevel(logging.DEBUG)
logging.getLogger('smart_office_assistant.wisdom').setLevel(logging.INFO)
```

## 调试模式

### 启用调试

```python
# 在代码中
import smart_office_assistant as somn

somn.configure(
    debug=True,
    log_level='DEBUG',
    verbose=True
)
```

### 调试端点

```bash
# 健康检查
curl http://localhost:8000/health

# 配置状态
curl http://localhost:8000/status/config

# 内存状态
curl http://localhost:8000/status/memory

# 性能统计
curl http://localhost:8000/status/metrics
```

## 性能分析

### 内存分析

```bash
# 使用memory_profiler
pip install memory_profiler
python -m memory_profiler your_script.py

# 使用tracemalloc
python -X tracemalloc your_script.py
```

### CPU分析

```bash
# 使用cProfile
python -m cProfile -s cumtime your_script.py

# 使用line_profiler
pip install line_profiler
kernprof -l your_script.py
python -l -v your_script.py.lprof
```

## 网络问题

### 检查连接

```bash
# Ping检查
ping model-server.local

# 端口检查
telnet localhost 8000

# 防火墙规则
iptables -L -n
```

### 超时配置

```yaml
# config.yaml
network:
  timeout_seconds: 30
  retry_attempts: 3
  retry_delay: 1
```

## 数据恢复

### 从备份恢复

```bash
# 1. 停止服务
systemctl stop somn

# 2. 恢复数据
tar -xzf backups/somn_data_20260424.tar.gz -C /

# 3. 验证
python -c "from smart_office_assistant import check_data; check_data()"

# 4. 重启
systemctl start somn
```

### 重建索引

```bash
# 重建搜索索引
python scripts/rebuild_index.py --all

# 重建记忆索引
python scripts/rebuild_memory_index.py
```

## 联系支持

如果以上方法无法解决问题：

1. 收集诊断信息
2. 查看 [GitHub Issues](https://github.com/marcwadehan-png/somn-agent/issues)
3. 提交Issue包含:
   - 环境信息 (`python -c "import sys; print(sys.version)"`)
   - 完整错误日志
   - 最小复现代码
   - 配置（脱敏后）

---

*最后更新: 2026-04-24*