# Somn AI Farming Philosophy - "磨坊+厨师"哲学

> 大模型 + 搜索能力 = **小麦**（原材料）
> Somn = **磨坊 + 厨师**（加工能力）
> 云端大模型 = **老师们**（知识来源）
> 本地大模型 = **学生**（学习者）

---

## 1. 核心理念

### 1.1 烹饪隐喻

| 元素 | 角色 | 说明 |
|------|------|------|
| 小麦 | 大模型 + 搜索 | 原材料，来自外部 |
| 磨坊 | Somn 编排器 | 研磨加工，控制流程 |
| 厨师 | Somn 智慧体系 | 决定做成什么、怎么调味 |
| 面包/面条/饺子 | 最终输出 | 任务结果 |
| 采购员 | 搜索/API 工具 | 获取小麦（原材料）|

### 1.2 师生隐喻

| 角色 | 对应 | 特点 |
|------|------|------|
| 老师 | 云端大模型（DeepSeek/Gemini/Groq...） | 知识渊博、视野广、但不懂 Somn |
| 学生 | 本地大模型（Ollama/qwen2.5...） | 正在学习、效率高、成本低 |
| 教务主任 | Somn 智能编排层 | 调配资源、评估质量、决定何时求助 |

---

## 2. 系统架构

```
用户请求
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│              Somn Orchestrator（磨坊+厨师）              │
│  ┌─────────┐  ┌──────────┐  ┌────────────┐             │
│  │FAST模式 │  │HOME模式   │  │FEAST模式   │             │
│  │快手菜   │  │家常菜     │  │大餐        │             │
│  │本地直答 │  │本地+云端  │  │多老师投票  │             │
│  └─────────┘  └──────────┘  └────────────┘             │
└───────────────────────┬─────────────────────────────────┘
                        │
    ┌───────────────────┼───────────────────┐
    ▼                   ▼                   ▼
┌─────────┐       ┌───────────┐       ┌─────────────┐
│  Cloud  │◄────►│ Teacher-  │◄────►│  LLM        │
│  Model  │      │ Student   │      │  Service    │
│  Hub    │      │ Engine    │      │  (Local)    │
│ (老师们) │      │ (学习引擎) │      │  (学生)     │
└─────────┘       └───────────┘       └─────────────┘
```

---

## 3. 云端模型枢纽（CloudModelHub）

### 3.1 已集成的免费云端大模型

| 老师 | 模型 | 专长 | 特色 |
|------|------|------|------|
| DeepSeek老师 | deepseek-chat | 推理/代码 | 深度思考能力强 |
| DeepSeek推理老师 | deepseek-reasoner | 推理 | 复杂推理专精 |
| Groq极速老师 | llama-3.3-70b | 快速/综合 | 速度极快，免费 |
| GroqMixtral老师 | mixtral-8x7b | 快速/代码 | 高吞吐量 |
| Gemini老师 | gemini-2.0-flash | 多模态/快速 | 免费多模态 |
| Mistral老师 | mistral-small | 综合/创意 | 欧洲均衡派 |
| Mistral大老师 | mistral-large | 推理/学术 | 高质量 |
| Cohere老师 | command-r-plus | RAG/推理 | 检索增强优化 |
| Together老师 | meta-llama | 综合/代码 | 开源聚合 |
| HF老师 | huggingface-llama | 综合 | 开源生态 |
| OpenRouter老师 | aggregate | 综合 | 50+模型聚合 |
| 智谱老师 | glm-4-flash | 综合/代码 | 国产免费 |

### 3.2 老师管理策略

```python
# 选择最合适的老师
1. 优先指定老师 → 2. 根据专长选择 → 3. 智能推荐
                                    │
                    按历史表现排序（好老师优先）
                                    │
                        排除限速中的老师（最多返回N位）
```

### 3.3 环境变量配置

```bash
# 支持的 API Key 环境变量
DEEPSEEK_API_KEY=sk-xxxx          # DeepSeek
GROQ_API_KEY=gsk_xxxx             # Groq
GOOGLE_API_KEY=AIzaSyxxxx          # Gemini
MISTRAL_API_KEY=xxxx              # Mistral
COHERE_API_KEY=xxxx               # Cohere
TOGETHER_API_KEY=xxxx             # Together AI
HF_API_KEY=hf_xxxx                # HuggingFace
OPENROUTER_API_KEY=sk-or-xxxx     # OpenRouter
ZHIPU_API_KEY=xxxx                # 智谱
```

---

## 4. 师生学习引擎（TeacherStudentEngine）

### 4.1 四种学习模式

| 模式 | 名称 | 流程 | 适用场景 |
|------|------|------|----------|
| DIRECT | 快手模式 | 学生直答 → Somn评估 → 差则补救 | 简单任务、快速响应 |
| PREVIEW | 预习模式 | 先问老师 → 学生学习 → 学生作答 → Somn裁定 | 复杂任务、学术写作 |
| REVIEW | 复习模式 | 学生先答 → 请教老师 → 对比修正 | 学生有基础、需要验证 |
| DEMOCRATIC | 民主模式 | 多老师同时回答 → Somn综合裁定 | 重要决策、多角度分析 |

### 4.2 质量评估维度

| 维度 | 权重 | 评估内容 |
|------|------|----------|
| 准确性 | 30% | 答案是否正确、有无逻辑矛盾 |
| Somn融合度 | 30% | 是否融入 Somn 的智慧风格 |
| 实用性 | 25% | 是否有可执行的建议 |
| 完整性 | 15% | 是否覆盖所有要点 |

### 4.3 混合模式智能决策

```
任务复杂度 < 0.3 + 学生掌握度 > 0.7 → DIRECT（简单已掌握）
任务复杂度 > 0.7 + 重要性 > 0.8     → DEMOCRATIC（复杂重要）
学生掌握度 > 0.4                    → REVIEW（已有基础）
默认                                   → PREVIEW（一般情况）
```

---

## 5. Somn 编排器（SomnOrchestrator）

### 5.1 三种烹饪模式

| 模式 | 烹饪方式 | 成本 | 速度 | 质量 |
|------|----------|------|------|------|
| FAST（快手菜） | 本地模型直接答 | 最低 | 最快 | 中等 |
| HOME（家常菜） | 本地+云端辅助 | 中等 | 中等 | 较高 |
| FEAST（大餐） | 多云端民主投票 | 较高 | 较慢 | 最高 |

### 5.2 自动模式判断

```python
关键词触发：
- "查一下"/"多少钱"/"一句话"/"简单" → FAST
- "研究"/"分析报告"/"深度"/"论证" → FEAST
- 默认 → HOME
```

### 5.3 便捷接口

```python
# 快速回答（快手菜）
somn.quick_answer("今天天气怎么样")

# 深度回答（家常菜）
somn.thoughtful_answer("分析一下当前市场趋势", context=my_data)

# 综合报告（大餐）
somn.comprehensive_report("关于XX行业的深度研究报告")
```

---

## 6. 使用流程

### 6.1 初始化

```python
from src.tool_layer import (
    LLMService, CloudModelHub, TeacherStudentEngine, SomnOrchestrator
)

# 1. 初始化各组件
llm_service = LLMService()
cloud_hub = CloudModelHub()
teacher_student = TeacherStudentEngine(cloud_hub=cloud_hub, llm_service=llm_service)
somn = SomnOrchestrator(cloud_hub=cloud_hub, teacher_student_engine=teacher_student, llm_service=llm_service)

# 2. 查看可用老师
status = somn.get_kitchen_status()
print(status["teachers_available"], "位老师可用")

# 3. 开始工作
response = somn.quick_answer("用一句话解释量子计算")
print(response)
```

### 6.2 查看厨房状态

```python
status = somn.get_kitchen_status()
# {
#   "modes": {"fast": "...", "home": "...", "feast": "..."},
#   "dishes": ["soup", "noodles", "dumplings", ...],
#   "learning": {"total_tasks": 10, "avg_quality": 0.75, "mastered_topics": 3},
#   "teachers_available": 5,
#   "teacher_list": [{"id": "deepseek-chat", "name": "DeepSeek老师"}, ...]
# }
```

---

## 7. 扩展：添加新老师

```python
from src.tool_layer import CloudModelHub, TeacherConfig, TeacherSpecialty

hub = CloudModelHub()
hub.register_teacher(TeacherConfig(
    teacher_id="my-teacher",
    name="我的专属老师",
    provider="custom",
    model_name="my-model",
    api_base="https://my-api.com/v1",
    specialties=[TeacherSpecialty.REASONING, TeacherSpecialty.CODE],
    free_tier=True,
))
```

---

## 8. 设计原则总结

1. **本地优先**：能用本地模型的绝不用云端，保护隐私，降低成本
2. **按需调用**：简单任务快手直答，复杂任务才请教老师
3. **Somn 做主**：无论云端老师多么强大，最终答案由 Somn 裁定
4. **持续学习**：每次任务都记录学习，学生的能力持续提升
5. **质量闭环**：每份输出都经过 Somn 质量评估，不达标则修正
6. **隐私底线**：所有项目代码和知识不外传，只检索公开信息

---

*最后更新：2026-04-04*
