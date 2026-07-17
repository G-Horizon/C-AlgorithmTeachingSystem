@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\student_start.ps1"
if errorlevel 1 (
  echo.
  echo Student demo failed to start. Press any key to close.
  pause >nul
)
