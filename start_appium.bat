@echo off
chcp 65001 >nul
echo ==========================================
echo     Appium Server 启动脚本
echo ==========================================
echo.

REM 设置 Appium 路径
set APPIUM_PATH=C:\Users\Lai\AppData\Local\Programs\OneClaw\appium.cmd

REM 检查 Appium 是否存在
if not exist "%APPIUM_PATH%" (
    echo [错误] 未找到 Appium，请先安装
    echo        npm install -g appium
    pause
    exit /b 1
)

echo [信息] Appium 路径: %APPIUM_PATH%
echo.

REM 检查端口是否被占用
echo [检查] 检查端口 4723...
netstat -ano | findstr :4723 >nul
if %errorlevel% equ 0 (
    echo [警告] 端口 4723 已被占用，Appium 可能已在运行
    echo.
    choice /C YN /M "是否强制关闭并重启"
    if errorlevel 2 goto end
    if errorlevel 1 (
        echo [操作] 关闭占用端口的进程...
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :4723') do (
            taskkill /F /PID %%a >nul 2>&1
        )
    )
)

echo.
echo [启动] 正在启动 Appium Server...
echo        地址: http://127.0.0.1:4723
echo.
echo 按 Ctrl+C 停止服务
echo.

REM 启动 Appium
"%APPIUM_PATH%" --address 127.0.0.1 --port 4723

:end
echo.
echo [结束] Appium Server 已停止
pause
