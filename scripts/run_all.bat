@echo off
setlocal

set ROOT_DIR=%~dp0..

REM Start backend
set PYTHONPATH=%ROOT_DIR%
start "DataSciProject Backend" /B /D %ROOT_DIR% /MIN cmd /C "%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe -m backend.app"

echo Backend started.

REM Start frontend
cd /d %ROOT_DIR%\frontend
if not exist node_modules (
  npm install
)

npm run dev
