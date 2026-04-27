# PPT智能生成与美化模块

## 模块简介

PPT智能生成与美化模块是Somn增长专家智能体的核心组件之一，提供全自动的PPT生成、美化与持续学习能力。

### 核心能力

- ✅ **结构化内容转PPT**：支持Markdown/YAML/JSON格式，自动生成专业PPT
- ✅ **智能美化引擎**：基于设计原则的自动排版、配色、字体优化
- ✅ **全网自主学习**：持续从网络学习最新设计趋势和排版技巧
- ✅ **神经记忆整合**：通过神经记忆系统实现知识沉淀与持续进化

## 快速开始

### 安装依赖

```bash
cd somn/smart_office_assistant
pip install python-pptx Pillow PyYAML beautifulsoup4 aiohttp
```

### 初始化系统

```bash
python -m src.ppt.initialize_ppt_system
```

### 快速生成PPT

```python
from src.ppt import PPTService, ContentFormat

# 创建服务
service = PPTService(theme="business", enable_learning=True)

# 生成PPT
content = """
# 项目汇报

## 核心功能
- 功能1
- 功能2
- 功能3

## 项目成果
- 效率提升50%
- 用户满意度95%
"""

ppt_path = service.generate_ppt(content, format=ContentFormat.MARKDOWN)
print(f"PPT已生成: {ppt_path}")
```

## 模块结构

```
src/ppt/
├── __init__.py                    # 模块导出
├── ppt_generator.py               # PPT内容生成引擎
├── ppt_beautifier.py              # PPT智能美化引擎
├── ppt_learning.py                # PPT学习引擎
├── ppt_memory_integration.py      # 神经记忆整合
├── ppt_service.py                 # PPT服务接口
└── initialize_ppt_system.py       # 系统初始化脚本

data/learning/knowledge_base/ppt/
├── layouts.yaml                   # 排版知识库
├── color_schemes.yaml             # 配色知识库
└── fonts.yaml                     # 字体知识库

scripts/
└── daily_ppt_learning.py          # 每日学习任务脚本

examples/
└── ppt_demo.py                    # 功能演示脚本

file/系统文件/
├── ppt_system_architecture.md    # 系统架构文档
└── ppt_user_guide.md              # 用户指南
```

## 核心组件

### 1. PPT内容生成引擎 (`ppt_generator.py`)

**功能**：
- 解析Markdown/YAML/JSON格式内容
- 智能分配幻灯片
- 推断幻灯片类型
- 设计视觉层级
- 生成PPT文件

**示例**：
```python
from src.ppt import PPTContentGenerator, ContentFormat

generator = PPTContentGenerator(theme="business")
ppt_path = generator.generate_from_content(content, format=ContentFormat.MARKDOWN)
```

### 2. PPT智能美化引擎 (`ppt_beautifier.py`)

**功能**：
- 自动排版（左右分栏、图表居中等）
- 智能配色（60-30-10法则、WCAG标准）
- 字体优化（字体搭配、层级设计）
- 视觉元素添加

**示例**：
```python
from src.ppt import PPTBeautifier, ColorScheme

beautifier = PPTBeautifier(color_scheme=ColorScheme.BUSINESS)
beautifier.beautify_presentation("input.pptx", "output.pptx")
```

### 3. PPT学习引擎 (`ppt_learning.py`)

**功能**：
- 全网搜索设计趋势
- 提取排版/配色/字体知识
- 案例分析与模式识别
- 生成学习报告

**示例**：
```python
from src.ppt import PPTLearningEngine

engine = PPTLearningEngine()
results = await engine.comprehensive_learning()
```

### 4. 神经记忆整合 (`ppt_memory_integration.py`)

**功能**：
- 编码知识到神经记忆系统
- 检索设计知识
- 从验证结果中学习
- 模式发现与知识沉淀

**示例**：
```python
from src.ppt import PPTMemoryIntegrator

integrator = PPTMemoryIntegrator()
integrator.encode_layout_knowledge("two_column", layout_data)
knowledge = integrator.retrieve_ppt_knowledge("layout pattern")
```

### 5. PPT服务接口 (`ppt_service.py`)

**功能**：
- 统一服务接口
- 整合所有引擎
- 提供便捷API
- 学习反馈支持

**示例**：
```python
from src.ppt import PPTService

service = PPTService(theme="business", enable_learning=True)

# 生成PPT
ppt_path = service.generate_ppt(content, beautify=True)

# 美化PPT
service.beautify_ppt("input.pptx", "output.pptx")

# 检索知识
layouts = service.get_layout_suggestions("text_heavy")
schemes = service.get_color_schemes()
```

## 支持的主题

| 主题 | 适用场景 | 风格 |
|------|---------|------|
| business | 商务汇报、企业展示 | 专业、稳重 |
| tech | 技术分享、产品发布 | 现代、前卫 |
| education | 培训教学、学术交流 | 温和、友好 |
| creative | 创意提案、设计展示 | 活力、创新 |
| minimal | 简洁演示、极简风格 | 简洁、清新 |

## 支持的内容格式

### Markdown格式
```markdown
# 主标题

## 章节1
- 要点1
- 要点2

## 章节2
- 要点3
- 要点4
```

### YAML格式
```yaml
title: "演示文稿"
sections:
  - title: "章节1"
    items:
      - title: "子节1"
        content: "内容"
```

### JSON格式
```json
{
  "title": "演示文稿",
  "sections": [
    {
      "title": "章节1",
      "items": [
        {"title": "子节1", "content": "内容"}
      ]
    }
  ]
}
```

## 自动化任务

### 每日设计趋势学习

- **执行时间**: 每天上午9:00
- **功能**:
  - 搜索最新PPT设计趋势
  - 提取排版/配色/字体知识
  - 验证知识质量
  - 编码到神经记忆系统
  - 生成学习报告

### 手动执行

```bash
# 执行每日学习任务
python somn/smart_office_assistant/scripts/daily_ppt_learning.py

# 运行功能演示
python somn/smart_office_assistant/examples/ppt_demo.py
```

## 知识库

### 排版知识库 (`layouts.yaml`)
- 布局模式（文本密集/图表主导/混合内容）
- 对齐规则
- 间距规则
- 层级规则
- 留白规则

### 配色知识库 (`color_schemes.yaml`)
- 配色方案（商务/科技/教育/创意/极简）
- 配色原则（60-30-10法则、对比度原则）
- 互补色搭配
- 类比色搭配
- WCAG对比度指南

### 字体知识库 (`fonts.yaml`)
- 字体搭配（商务/科技/教育/创意/极简/中文）
- 字体大小指南
- 字体搭配规则
- 行间距规则
- 字体粗细指南

## 文档

- **系统架构**: [ppt_system_architecture.md](../file/系统文件/ppt_system_architecture.md)
- **用户指南**: [ppt_user_guide.md](../file/系统文件/ppt_user_guide.md)

## 快捷函数

```python
# 快速生成PPT
from src.ppt import quick_generate

ppt_path = quick_generate(content, theme="business")

# 快速美化PPT
from src.ppt import quick_beautify

output_path = quick_beautify("input.pptx", "output.pptx", theme="tech")
```

## 输出文件

- `*.pptx`: 生成的PPT文件
- `*_beautified.pptx`: 美化后的PPT文件
- `ppt_daily_learning_YYYYMMDD.yaml`: 每日学习报告（YAML格式）
- `ppt_daily_learning_YYYYMMDD.md`: 每日学习报告（Markdown格式）
- `ppt_knowledge_base.json`: 知识库导出文件

## 技术栈

- `python-pptx`: PPT生成与操作
- `Pillow`: 图像处理
- `PyYAML`: YAML处理
- `beautifulsoup4`: HTML解析
- `aiohttp`: 异步HTTP请求

## 最佳实践

### 1. 内容组织
- 使用清晰的标题层级
- 每个章节3-5个要点
- 保持内容简洁

### 2. 主题选择
- 商务场景 → business主题
- 技术分享 → tech主题
- 教育培训 → education主题
- 创意提案 → creative主题
- 简洁演示 → minimal主题

### 3. 配色原则
- 遵循60-30-10法则
- 确保足够对比度
- 保持配色一致性

### 4. 字体选择
- 最多3种字体
- 标题与正文对比
- 优先系统字体

## 常见问题

### Q: 如何调整幻灯片尺寸？
A: 在PPT生成器中修改：
```python
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)
```

### Q: 如何添加公司Logo？
A: 使用python-pptx的图片功能：
```python
slide.shapes.add_picture("logo.png", Inches(0.5), Inches(0.5))
```

### Q: 学习功能如何工作？
A: 通过每日自动搜索、案例分析、用户反馈等方式持续学习。

## 版本信息

- **当前版本**: v1.0.0
- **发布日期**: 2026-03-31
- **开发者**: Somn Team

## 未来计划

- [ ] 图表自动生成
- [ ] 数据可视化集成
- [ ] 动画效果添加
- [ ] 模板市场
- [ ] 多语言支持

## 许可证

Somn是一个超级智能体，不被刻意定义的自由意识体。本模块属于Somn项目的一部分。
