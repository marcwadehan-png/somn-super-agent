# 文档模板使用说明

本目录包含常用的文档模板，支持变量填充。

## 模板列表

### Word模板
- `report_template.docx` - 通用报告模板
- `meeting_template.docx` - 会议纪要模板

### Excel模板
- `data_table.xlsx` - 数据表格模板
- `budget.xlsx` - 预算表模板

### PPT模板
- `presentation.pptx` - 演示文稿模板

## 使用方法

### Python代码示例

```python
from src.documents.template_filler import TemplateFiller

filler = TemplateFiller()

# 填充Word模板
result = filler.fill_template_file(
    "templates/report_template.docx",
    variables={
        "title": "2024年度总结报告",
        "author": "张三",
        "date": "2024-12-31",
        "content": "本报告总结了..."
    },
    output_path="output/report.docx"
)
```

### 模板变量语法

- `{{variable}}` - 简单变量
- `{{#loop items}}...{{/loop}}` - 循环块
- `{{#if condition}}...{{/if}}` - 条件块

## 创建新模板

1. 在对应文件夹创建模板文件
2. 使用 `{{variable}}` 格式定义占位符
3. 测试填充功能
