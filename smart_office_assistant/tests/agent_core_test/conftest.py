# -*- coding: utf-8 -*-
"""
agent_core 测试配置
"""
import sys
import os
from pathlib import Path

# 项目路径引导
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant"))

sys.stdout.reconfigure(encoding='utf-8')

# 测试配置
TEST_CONFIG = {
    'auto_learn': True,
    'learning_data_path': 'data/learning',
}
