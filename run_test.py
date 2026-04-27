#!/usr/bin/env python3
"""运行系统监控和告警测试"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smart_office_assistant'))

import pytest

if __name__ == "__main__":
    # 切换到项目目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 运行测试
    args = [
        "-v",
        "-s",
        "tests/test_system_monitor_alert.py::TestSystemMonitorIntegration::test_check_resources_no_alert",
    ]
    print(f"Running: pytest {' '.join(args)}")
    exit_code = pytest.main(args)
    sys.exit(exit_code)
