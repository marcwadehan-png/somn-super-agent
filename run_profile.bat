@echo off
cd /d d:\AI\somn
"C:\Users\18000\.workbuddy\binaries\python\versions\3.13.12\python.exe" profile_load.py > profile_output.txt 2>&1
echo Exit code: %ERRORLEVEL%
