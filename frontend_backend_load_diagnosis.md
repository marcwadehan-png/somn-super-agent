# Somn 前端后端加载全局诊断报告

**诊断时间**: 2026-04-30 16:40
**诊断人**: C0dy AI

---

## 一、诊断执行情况

### 1.1 测试命令
```bash
# 前端加载验证
python d:\AI\Somn-GUI\test_load_verify.py --url http://127.0.0.1:8964

# 后端API检查
curl http://127.0.0.1:8964/api/v1/admin/system/components
curl http://127.0.0.1:8964/api/v1/health/detail
```

### 1.2 前端加载验证结果
```
[CONNECT] 连接探测: ✅ 通过 (343ms)
[LLM] 基础服务: ✅ 通过 (30ms)
[REASONING] 核心推理: ❌ 失败 (22ms)
[KNOWLEDGE] 知识系统: ✅ 通过 (21ms)
[MEMORY] 记忆系统: ✅ 通过 (20ms)
[TRACK] 双轨系统: ✅ 通过 (18ms)
[VERIFY] 功能验证: ✅ 通过 (245ms)

总计: 6 通过, 1 失败
```

---

## 二、发现的问题

### 问题 1: 核心推理加载失败 ⚠️ 严重

**现象**:
- SageDispatch: `loaded = False`
- DivineReason: `loaded = False`

**原因分析**:
后端 `/api/v1/admin/system/components` 返回的结构与前端期望的不一致。

| 前端期望字段 | 后端实际返回 |
|------------|-------------|
| `sage_dispatch.loaded` | 不存在 |
| `divine_reason.loaded` | 不存在 |
| `tianshu` | 不存在 |

**后端实际返回**:
```json
{
  "data": {
    "components": {
      "neural_memory": {...},
      "knowledge_graph": {...}
    }
  }
}
```

### 问题 2: 6 个关键 API 端点返回 404 ❌ 严重

| 端点 | 状态 | 描述 |
|------|------|------|
| `/api/v1/knowledge/domain/status` | 404 | DomainNexus状态 |
| `/api/v1/wisdom/pan/tree/info` | 404 | Pan-Wisdom Tree信息 |
| `/api/v1/track-b/status` | 404 | 神行轨状态 |
| `/api/v1/memory/stats` | 404 | 记忆统计 |
| `/api/v1/refute/status` | 404 | RefuteCore状态 |
| `/api/v1/wisdom/dispatch/prewarm` | 404 | SageDispatch预热 |

**原因**:
- `load_status.py` 在 **16:29** 修改
- 后端服务在 **16:09** 启动
- **后端运行的是旧代码**，没有加载 `load_status.py` 中的新端点

### 问题 3: 版本号不一致 ⚠️ 中等

| 位置 | 版本号 |
|------|--------|
| 后端 /health | `v6.2.0` |
| 前端文档 | `S1.0` |
| 测试报告 | `S1.0` |
| LOAD_ARCHITECTURE.md | `S1.0` |

**说明**: 这不是 bug，但需要注意版本命名规范。

### 问题 4: 端点定义冲突 ⚠️ 中等

`admin.py` 和 `load_status.py` 都定义了 `/api/v1/admin/system/components`:

| 文件 | 行号 | 定义方式 |
|------|------|---------|
| `admin.py` | 763 | 使用 SystemMonitor |
| `load_status.py` | 83 | 自定义组件状态 |

**当前行为**: 后注册的 `load_status.py` 覆盖了 `admin.py`，但由于后端未重启，实际上 `admin.py` 的版本仍在运行。

---

## 三、后端组件状态详情

### 健康检查
```json
{
  "status": "healthy",
  "version": "v6.2.0",
  "uptime_seconds": 1790.1,
  "components": {
    "api_server": "healthy",
    "somn_core": "healthy"
  },
  "warmup_status": {
    "llm": true,
    "dual_model": true
  }
}
```

### 组件加载状态
- `neural_memory`: operational
- `knowledge_graph`: 13 nodes, 1 edges

---

## 四、修复建议

### 4.1 立即修复: 重启后端服务

```powershell
# 停止后端
python d:\AI\somn\process_manager.py stop

# 重新启动
python d:\AI\somn\process_manager.py start
```

或者使用:
```powershell
# 杀掉旧进程
Stop-Process -Id 40452 -Force

# 重新启动
python d:\AI\somn\start_server.py
```

### 4.2 代码修复: 统一组件状态返回结构

**问题**: 前端期望 `sage_dispatch.loaded` 等字段，但后端返回的是 `SystemMonitor` 的结构。

**修复方案**:

方案 A: 修改 `load_status.py` 的 `get_system_components()` 使其正确返回

方案 B: 修改前端 `test_load_verify.py` 使用实际返回的字段

### 4.3 长期改进: 添加版本检查机制

在前后端通信时增加版本校验:
```python
# 前端
expected_version = "S1.0"
backend_version = response.headers.get("X-Somn-Version")

if backend_version != expected_version:
    show_warning(f"版本不匹配: 前端 {expected_version}, 后端 {backend_version}")
```

---

## 五、诊断结论

| 问题级别 | 数量 | 说明 |
|---------|------|------|
| 🔴 严重 | 2 | 核心推理失败 + 6个端点404 |
| 🟡 中等 | 2 | 版本不一致 + 端点冲突 |
| 🟢 轻微 | 0 | - |

**建议操作**:
1. **已修复**: `load_status.py` 中 DomainNexus 导入路径已修复
2. **立即**: 重启后端服务使新代码生效
3. **短期**: 统一前后端 API 响应结构
4. **长期**: 建立版本同步机制

---

## 七、修复记录

### 7.1 修复 1: DomainNexus 导入路径错误 ✅

**问题**: `load_status.py` 第 314 行导入路径错误
```python
# 错误
from src.neural_memory.unified_memory_interface import DomainNexus

# 正确
from knowledge_cells.domain_nexus import DomainNexus
```

**修复时间**: 2026-04-30 16:45
**状态**: ✅ 已修复

### 7.2 验证结果

```bash
=== 端点注册检查 ===
OK /api/v1/knowledge/domain/status
OK /api/v1/wisdom/pan/tree/info
OK /api/v1/track-b/status
OK /api/v1/memory/stats
OK /api/v1/refute/status
OK /api/v1/wisdom/dispatch/prewarm
OK /api/v1/reasoning/initialize
```

**结论**: 代码修复已验证通过，需要重启后端服务使修复生效。

---

## 六、附件: 后端 API 清单

### 6.1 已注册端点 (88个)

**关键端点**:
- `/api/v1/health` ✅
- `/api/v1/health/detail` ✅
- `/api/v1/admin/system/components` ⚠️ (结构不匹配)
- `/api/v1/admin/llm/configs` ✅
- `/api/v1/admin/llm/status` ✅
- `/api/v1/admin/neural/status` ✅

**缺失端点** (需要重启后端):
- `/api/v1/knowledge/domain/status` ❌
- `/api/v1/wisdom/pan/tree/info` ❌
- `/api/v1/track-b/status` ❌
- `/api/v1/memory/stats` ❌
- `/api/v1/refute/status` ❌
- `/api/v1/wisdom/dispatch/prewarm` ❌

---

**诊断完成时间**: 2026-04-30 16:40:30
