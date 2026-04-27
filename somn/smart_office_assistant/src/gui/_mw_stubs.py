# -*- coding: utf-8 -*-
"""主窗口 - UI样式和消息模板

__all__ = [
    'format_agent_message',
    'format_system_message',
    'format_user_message',
    'is_supported_doc',
    'is_text_file',
]

包含样式定义和消息模板，供主窗口使用。
"""

# 对话消息样式
CHAT_USER_STYLE = '''
<div style="margin: 10px 0; text-align: right;">
    <div style="display: inline-block; background-color: #007bff; color: white; 
                padding: 10px 15px; border-radius: 15px; max-width: 80%;">
        <b>你:</b> {message}
    </div>
</div>
'''

CHAT_AGENT_STYLE = '''
<div style="margin: 10px 0;">
    <div style="display: inline-block; background-color: #e9ecef; 
                padding: 10px 15px; border-radius: 15px; max-width: 80%;">
        <b>🤖 AI:</b> {message}
    </div>
</div>
'''

CHAT_SYSTEM_STYLE = '''
<div style="margin: 10px 0; text-align: center;">
    <div style="display: inline-block; background-color: #f8f9fa; color: #6c757d;
                padding: 10px 15px; border-radius: 10px; font-size: 12px;">
        {message}
    </div>
</div>
'''

# 状态标签样式
STATUS_READY_STYLE = '''
QLabel {
    background-color: #d4edda;
    color: #155724;
    padding: 10px;
    border-radius: 5px;
}
'''

STATUS_THINKING_STYLE = '''
QLabel {
    background-color: #fff3cd;
    color: #856404;
    padding: 10px;
    border-radius: 5px;
}
'''

STATUS_ERROR_STYLE = '''
QLabel {
    background-color: #f8d7da;
    color: #721c24;
    padding: 10px;
    border-radius: 5px;
}
'''

# 欢迎消息
WELCOME_MESSAGE = """👋 欢迎使用 Somn!

汇千古之智，向未知而生。

我能帮你：
• 📄 生成各类文档(Word/PPT/PDF/Excel)
• 🔍 管理和检索知识
• 💡 回答问题,提供建议
• 📊 分析数据和撰写报告
• 🔍 扫描和分析文件系统
• 🎯 制定执行策略
• 📈 ML预测分析

有什么我可以帮你的吗?"""

# 支持的文件类型
SUPPORTED_TEXT_EXTENSIONS = [
    '.txt', '.md', '.py', '.js', '.html', '.css',
    '.json', '.yaml', '.yml', '.xml'
]

SUPPORTED_DOC_EXTENSIONS = ['.docx', '.pdf', '.pptx', '.ppt', '.xlsx', '.xls', '.csv']

# 快速命令
QUICK_COMMANDS = [
    "总结文档", "生成报告", "分析数据", "创建大纲",
    "扫描文件", "制定策略", "预测效果"
]

def format_user_message(message: str) -> str:
    """格式化用户消息"""
    return CHAT_USER_STYLE.format(message=message)

def format_agent_message(message: str) -> str:
    """格式化智能体消息"""
    return CHAT_AGENT_STYLE.format(message=message.replace('\n', '<br>'))

def format_system_message(message: str) -> str:
    """格式化系统消息"""
    return CHAT_SYSTEM_STYLE.format(message=message.replace('\n', '<br>'))

def is_text_file(suffix: str) -> bool:
    """判断是否为文本文件"""
    return suffix.lower() in SUPPORTED_TEXT_EXTENSIONS

def is_supported_doc(suffix: str) -> bool:
    """判断是否为支持的文档"""
    return suffix.lower() in SUPPORTED_DOC_EXTENSIONS
