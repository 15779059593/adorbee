#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本 - 检查 Appium 自动化测试环境
"""
import subprocess
import sys
import os
import urllib.request
import json


def check_command(cmd, args=None, name=None):
    """检查命令是否存在"""
    name = name or cmd
    try:
        result = subprocess.run(
            [cmd] + (args or ["--version"]),
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"  ✓ {name}: {version.split()[0] if version else 'OK'}")
            return True
    except Exception as e:
        pass
    
    print(f"  ✗ {name}: 未找到")
    return False


def check_appium_drivers():
    """检查 Appium 驱动"""
    print("\n[3] 检查 Appium 驱动...")
    
    appium_cmd = r"C:\Users\Lai\AppData\Local\Programs\OneClaw\appium.cmd"
    if not os.path.exists(appium_cmd):
        print("  ✗ Appium 未安装")
        return False
    
    try:
        result = subprocess.run(
            [appium_cmd, "driver", "list", "--installed"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        
        if "uiautomator2" in output:
            print("  ✓ uiautomator2 驱动已安装")
            return True
        else:
            print("  ⚠ uiautomator2 驱动未安装")
            print("    安装命令: appium driver install uiautomator2")
            return False
    except Exception as e:
        print(f"  ✗ 检查失败: {e}")
        return False


def check_appium_server():
    """检查 Appium Server 是否运行"""
    print("\n[4] 检查 Appium Server...")
    
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:4723/wd/hub/status",
            method="GET"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == 0 or "value" in data:
                print("  ✓ Appium Server 运行中 (http://127.0.0.1:4723)")
                return True
    except Exception as e:
        pass
    
    print("  ✗ Appium Server 未运行")
    print("    启动命令: appium")
    print("    或使用: D:\\Test\\adorbee\\start_appium.bat")
    return False


def check_android_devices():
    """检查 Android 设备连接"""
    print("\n[5] 检查 Android 设备...")
    
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        lines = result.stdout.strip().split("\n")
        devices = [line for line in lines[1:] if line.strip() and "device" in line]
        
        if devices:
            print(f"  ✓ 发现 {len(devices)} 个设备:")
            for device in devices:
                parts = device.split()
                if len(parts) >= 2:
                    print(f"    - {parts[0]} ({parts[1]})")
            return True
        else:
            print("  ✗ 未连接设备")
            print("    请检查:")
            print("      1. USB 调试是否已开启")
            print("      2. 数据线是否正常")
            print("      3. 驱动是否正确安装")
            return False
    except Exception as e:
        print(f"  ✗ 检查失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("Appium 自动化测试环境检查")
    print("=" * 50)
    
    checks = []
    
    # 1. 检查 Node.js
    print("\n[1] 检查 Node.js...")
    checks.append(check_command("node", name="Node.js"))
    
    # 2. 检查 npm
    print("\n[2] 检查 npm...")
    checks.append(check_command("npm", name="npm"))
    
    # 3. 检查 Appium 驱动
    checks.append(check_appium_drivers())
    
    # 4. 检查 Appium Server
    checks.append(check_appium_server())
    
    # 5. 检查 ADB
    print("\n[6] 检查 ADB...")
    checks.append(check_command("adb", name="ADB"))
    
    # 6. 检查 Android 设备
    checks.append(check_android_devices())
    
    # 7. 检查 Python 依赖
    print("\n[7] 检查 Python 依赖...")
    dependencies = [
        ("appium", "Appium-Python-Client"),
        ("pytest", "pytest"),
        ("allure", "allure-pytest"),
        ("yaml", "PyYAML"),
        ("selenium", "selenium"),
    ]
    
    for module, package in dependencies:
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (未安装)")
            print(f"    安装命令: pip install {package}")
            checks.append(False)
    
    # 总结
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    print(f"检查结果: {passed}/{total} 项通过")
    
    if passed == total:
        print("✓ 环境检查全部通过，可以开始测试！")
    else:
        print("⚠ 部分检查未通过，请根据提示修复")
    
    print("=" * 50)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
