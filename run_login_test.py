#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录功能自动化测试执行脚本
"""
import os
import sys
import subprocess
import yaml

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


def check_environment():
    """检查测试环境"""
    print("=" * 50)
    print("检查测试环境")
    print("=" * 50)
    
    # 检查 Python
    print("\n[1] 检查 Python 环境...")
    try:
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True
        )
        print(f"   ✓ Python: {result.stdout.strip() or result.stderr.strip()}")
    except Exception as e:
        print(f"   ✗ Python 检查失败: {e}")
        return False
    
    # 检查 pytest
    print("\n[2] 检查 pytest...")
    try:
        result = subprocess.run(
            ["python", "-c", "import pytest; print(pytest.__version__)"],
            capture_output=True,
            text=True
        )
        print(f"   ✓ pytest: {result.stdout.strip()}")
    except Exception as e:
        print(f"   ✗ pytest 检查失败: {e}")
        return False
    
    # 检查 Appium
    print("\n[3] 检查 Appium Server...")
    try:
        import urllib.request
        req = urllib.request.Request(
            "http://127.0.0.1:4723/wd/hub/status",
            method="GET"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            print("   ✓ Appium Server 运行中")
    except Exception as e:
        print(f"   ✗ Appium Server 未启动: {e}")
        print("   请先运行: appium")
        return False
    
    # 检查测试账号配置
    print("\n[4] 检查测试账号配置...")
    accounts_file = os.path.join(BASE_DIR, "data", "accounts.yaml")
    if os.path.exists(accounts_file):
        with open(accounts_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            accounts = data.get("test_accounts", [])
            if accounts:
                print(f"   ✓ 已配置 {len(accounts)} 个测试账号")
                for acc in accounts:
                    print(f"     - {acc.get('name', 'Unknown')}: {acc.get('username', 'N/A')}")
            else:
                print("   ⚠ 未配置测试账号，请在 data/accounts.yaml 中添加")
    else:
        print(f"   ✗ 未找到账号配置文件: {accounts_file}")
        return False
    
    print("\n" + "=" * 50)
    print("环境检查完成")
    print("=" * 50)
    return True


def run_tests(test_type="all"):
    """运行测试"""
    print(f"\n运行测试: {test_type}")
    print("-" * 50)
    
    # 构建 pytest 命令
    cmd = ["python", "-m", "pytest", "testcases/test_login.py", "-v"]
    
    if test_type == "smoke":
        cmd.extend(["-m", "smoke"])
    elif test_type == "abnormal":
        cmd.extend(["-k", "TestAbnormalLogin"])
    elif test_type == "security":
        cmd.extend(["-k", "TestLoginSecurity"])
    elif test_type == "ui":
        cmd.extend(["-k", "TestLoginUI"])
    
    # 添加 Allure 报告输出
    cmd.extend(["--alluredir=reports/allure-results"])
    
    # 执行测试
    result = subprocess.run(cmd)
    return result.returncode


def show_menu():
    """显示菜单"""
    print("\n" + "=" * 50)
    print("Adorbee APP 登录功能自动化测试")
    print("=" * 50)
    print("\n请选择要运行的测试：")
    print("\n  [1] 运行所有登录测试")
    print("  [2] 运行冒烟测试 (仅正常登录)")
    print("  [3] 运行异常登录测试")
    print("  [4] 运行安全测试 (SQL注入/XSS)")
    print("  [5] 运行UI交互测试")
    print("  [6] 生成 Allure 测试报告")
    print("  [7] 清理测试报告和日志")
    print("  [0] 退出")
    print()


def generate_report():
    """生成 Allure 报告"""
    print("\n生成 Allure 报告...")
    
    results_dir = os.path.join(BASE_DIR, "reports", "allure-results")
    report_dir = os.path.join(BASE_DIR, "reports", "allure-report")
    
    if not os.path.exists(results_dir):
        print("✗ 未找到测试结果，请先运行测试")
        return
    
    result = subprocess.run([
        "allure", "generate", results_dir,
        "-o", report_dir, "--clean"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ 报告已生成: {report_dir}")
        print("\n查看报告方式:")
        print(f"  1. 命令行: allure open {report_dir}")
        print(f"  2. 直接打开: {report_dir}/index.html")
    else:
        print(f"✗ 生成报告失败: {result.stderr}")
        print("请确保已安装 Allure: npm install -g allure-commandline")


def clean_reports():
    """清理报告"""
    print("\n清理测试报告和日志...")
    
    dirs_to_clean = [
        os.path.join(BASE_DIR, "reports", "allure-results"),
        os.path.join(BASE_DIR, "reports", "allure-report"),
        os.path.join(BASE_DIR, "reports", "screenshots"),
    ]
    
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            import shutil
            shutil.rmtree(dir_path)
            print(f"  ✓ 已清理: {dir_path}")
    
    # 清理日志文件
    logs_dir = os.path.join(BASE_DIR, "logs")
    if os.path.exists(logs_dir):
        for file in os.listdir(logs_dir):
            if file.endswith(".log"):
                os.remove(os.path.join(logs_dir, file))
                print(f"  ✓ 已清理日志: {file}")
    
    print("\n✓ 清理完成")


def main():
    """主函数"""
    # 检查环境
    if not check_environment():
        print("\n✗ 环境检查未通过，请修复后重试")
        sys.exit(1)
    
    while True:
        show_menu()
        choice = input("请输入选项 (0-7): ").strip()
        
        if choice == "1":
            run_tests("all")
        elif choice == "2":
            run_tests("smoke")
        elif choice == "3":
            run_tests("abnormal")
        elif choice == "4":
            run_tests("security")
        elif choice == "5":
            run_tests("ui")
        elif choice == "6":
            generate_report()
        elif choice == "7":
            clean_reports()
        elif choice == "0":
            print("\n再见！")
            break
        else:
            print("\n无效选项，请重新选择")
        
        input("\n按 Enter 键继续...")


if __name__ == "__main__":
    main()
