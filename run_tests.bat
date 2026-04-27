@echo off
chcp 65001 > nul
cd /d d:\AI\somn
echo 运行系统监控和告警机制测试...
"C:\Users\18000\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m pytest tests\test_system_monitor_alert.py -v
echo.
echo 测试完成，按任意键退出...
pause > nul
