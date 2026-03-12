@echo off
chcp 65001 >nul
echo ==========================================
echo     Adorbee APP 登录功能自动化测试
echo ==========================================
echo.

REM 切换到项目目录
cd /d "D:\Test\adorbee"

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请安装 Python 3.x
    pause
    exit /b 1
)

echo [检查] Python 环境: OK

REM 检查 Appium Server
echo [检查] 检查 Appium Server...
curl -s http://127.0.0.1:4723/wd/hub/status >nul 2>&1
if errorlevel 1 (
    echo [警告] Appium Server 未启动！
    echo.
    echo 请先启动 Appium Server:
    echo   命令: appium
    echo.
    echo 或者使用 appium-doctor 检查环境:
    echo   命令: appium-doctor
    echo.
    pause
    exit /b 1
) else (
    echo [检查] Appium Server: OK
)

echo.
echo ==========================================
echo 请选择要运行的测试：
echo ==========================================
echo.
echo  [1] 运行所有登录测试
echo  [2] 运行冒烟测试 (仅正常登录)
echo  [3] 运行异常登录测试
echo  [4] 运行安全测试 (SQL注入/XSS)
echo  [5] 运行UI交互测试
echo  [6] 生成 Allure 测试报告
echo  [7] 清理测试报告和日志
echo  [0] 退出
echo.

set /p choice="请输入选项 (0-7): "

if "%choice%"=="1" goto run_all
if "%choice%"=="2" goto run_smoke
if "%choice%"=="3" goto run_abnormal
if "%choice%"=="4" goto run_security
if "%choice%"=="5" goto run_ui
if "%choice%"=="6" goto generate_report
if "%choice%"=="7" goto clean_reports
if "%choice%"=="0" goto exit

echo [错误] 无效选项
goto end

:run_all
echo.
echo [运行] 执行所有登录测试...
pytest testcases/test_login.py -v --alluredir=reports/allure-results
goto end

:run_smoke
echo.
echo [运行] 执行冒烟测试 (正常登录)...
pytest testcases/test_login.py -v -m smoke --alluredir=reports/allure-results
goto end

:run_abnormal
echo.
echo [运行] 执行异常登录测试...
pytest testcases/test_login.py::TestAbnormalLogin -v --alluredir=reports/allure-results
goto end

:run_security
echo.
echo [运行] 执行安全测试...
pytest testcases/test_login.py::TestLoginSecurity -v --alluredir=reports/allure-results
goto end

:run_ui
echo.
echo [运行] 执行UI交互测试...
pytest testcases/test_login.py::TestLoginUI -v --alluredir=reports/allure-results
goto end

:generate_report
echo.
echo [生成] 生成 Allure 测试报告...
if exist reports\allure-results (
    allure generate reports/allure-results -o reports/allure-report --clean
    if errorlevel 1 (
        echo [错误] 生成报告失败，请确保已安装 Allure
        echo        安装命令: npm install -g allure-commandline
    ) else (
        echo [完成] 报告已生成到 reports/allure-report
        echo.
        echo 查看报告方式:
        echo   1. 命令行: allure open reports/allure-report
        echo   2. 直接打开: reports/allure-report/index.html
    )
) else (
    echo [错误] 未找到测试结果，请先运行测试
)
goto end

:clean_reports
echo.
echo [清理] 清理测试报告和日志...
if exist reports\allure-results rmdir /s /q reports\allure-results 2>nul
if exist reports\allure-report rmdir /s /q reports\allure-report 2>nul
if exist reports\screenshots rmdir /s /q reports\screenshots 2>nul
if exist logs\*.log del /q logs\*.log 2>nul
echo [完成] 已清理
goto end

:exit
echo.
echo 再见！
exit /b 0

:end
echo.
echo [完成] 测试执行完毕
echo.
echo 提示:
echo   - 测试报告: reports/allure-results
echo   - 运行 allure serve reports/allure-results 查看实时报告
pause
