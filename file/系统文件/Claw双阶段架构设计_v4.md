# Claw双阶段架构设计文档

## 版本: v4.1.0（整合版）
## 日期: 2026-04-23
## 历史版本: v3.0.0（Claw双阶段架构设计.md）

---

## 十三、完整上下文能力 (v4.1.0)

### 13.1 四级上下文

| 级别 | 内容 | 访问 |
|------|------|------|
| **System** | 时间、时段、季节、时区、问候语 | `context.system` |
| **Session** | 会话ID、历史、主题 | `context.session` |
| **User** | 用户信息、偏好、兴趣 | `context.user` |
| **Claw** | Claw状态、记忆快照、协作历史 | `context.claw` |

### 13.2 环境变量适配

```bash
# 环境变量前缀
CLAW_* / OPENCLAW_*

# 基础配置
CLAW_NAME=孔子
CLAW_MODE=independent
CLAW_LEVEL=normal

# 记忆配置
CLAW_MEMORY_ENABLED=true
CLAW_MEMORY_PATH=data/claws/{name}/memory
CLAW_MEMORY_AUTO_SAVE=true

# 协作配置
CLAW_COLLABORATORS=孟子,荀子
CLAW_COLLABORATION_MAX=2
CLAW_COLLABORATION_TIMEOUT=60

# 性能配置
CLAW_TIMEOUT=300
CLAW_MAX_RETRIES=3
CLAW_CACHE_ENABLED=true

# 日志配置
CLAW_LOG_LEVEL=INFO
CLAW_LOG_FILE=
```

### 13.3 用法示例

```python
from src.intelligence.claws.context import ClawContextContainer, ClawEnvironment

# 1. 上下文容器
context = ClawContextContainer("孔子")
context.set_session("session-001", current_topic="讨论知行合一")
context.add_user_message("什么是知行合一?")
full_context = context.get_full_context()
prompt = context.build_system_prompt(query, style="循循善诱")

# 2. 环境变量适配
env = ClawEnvironment("孔子")
timeout = env.get_timeout()  # 300
memory_enabled = env.is_memory_enabled()  # True
collaborators = env.get_collaborators()  # ["孟子", "荀子"]

# 3. 验证配置
validation = env.validate()
if not validation["valid"]:
    print(validation["errors"])

# 4. 导出配置到.env
env.to_env_file(Path("claw.env"))
```

---

## 十四、完整ClawEngine架构

### 14.1 模块结构

```
claws/
├── soul/
│   ├── __init__.py
│   └── _soul_driver.py      # v3.1.0
├── identity/
│   ├── __init__.py
│   └── _identity_router.py  # v3.2.0
├── memory/
│   ├── __init__.py
│   ├── _dynamic_cells.py    # v3.3.0
│   └── _learning_engine.py  # v3.3.0
├── context/
│   ├── __init__.py
│   ├── _claw_context.py     # v4.1.0
│   └── _claw_environment.py   # v4.1.0
├── _claw_engine.py          # v4.1.0
├── configs/
│   └── 孔子_v3.yaml
└── file/系统文件/
    └── Claw双阶段架构设计.md
```

### 14.2 ClawIndependentWorker完整组件

```python
class ClawIndependentWorker:
    # 核心配置
    name: str
    metadata: ClawMetadata
    architect: Optional[ClawArchitect]
    
    # v4.1.0 完整上下文
    context: ClawContextContainer
    environment: ClawEnvironment
    
    # v3.x 引擎
    soul_engine: SoulBehaviorEngine
    identity_engine: IdentityRouterEngine
    learning_engine: LearningEngine
    
    # 存储
    memory_dir: Path
```

### 14.3 完整处理流程

```
用户提问
    ↓
ClawEngine.ask()
    ↓
ClawIndependentWorker.process()
    ├── 1. 设置会话上下文
    ├── 2. 添加用户消息
    ├── 3. 更新用户信息
    ├── 4. 获取完整上下文
    ├── 5. SOUL驱动行为
    ├── 6. ReAct闭环处理
    ├── 7. 学习记录
    ├── 8. 添加助手消息
    └── 9. 更新Claw状态
    
返回完整结果
{
    "success": True,
    "response": "...",
    "soul_result": {...},
    "context": {
        "system": {...},
        "session": {...},
        "user": {...},
        "claw": {...}
    },
    "environment": {...},
    "learning_result": {...}
}
```

---

## 十五、环境变量优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 命令行 | 最高优先级 |
| 2 | 环境变量 | CLAW_*/OPENCLAW_* |
| 3 | .env文件 | 项目配置 |
| 4 | YAML配置 | Claw配置 |
| 5 | 默认值 | 最低优先级 |

---

## 十六、完整用法

```python
from pathlib import Path
from src.intelligence.claws import ClawEngine

# 1. 初始化引擎
engine = ClawEngine(Path("{项目根}"))

# 2. 独立工作模式
result = await engine.ask(
    query="什么是知行合一?",
    claw_name="孔子",
    session_id="session-001",
    user_info={"id": "user-1", "name": "张三", "level": "normal"}
)
print(result["response"])
print(result["context"]["system"]["greeting"])  # "上午好"

# 3. 协作工作模式
result = await engine.ask(
    query="如何制定营销策略?",
    claw_name="孔子",
    collaborators=["孟子", "荀子"]
)
print(result["collaborators"])

# 4. 获取统计
stats = engine.get_stats()
```