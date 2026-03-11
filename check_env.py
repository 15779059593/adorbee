#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查和测试脚本
用于验证自动化测试框架是否正常工作
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_environment():
    """检查测试环境"""
    print("=" * 60)
    print("Adorbee Automation Test Framework - Environment Check")
    print("=" * 60)
    
    # 1. 检查Python版本
    print("\n[1] Python Version Check")
    version = sys.version_info
    print(f"   Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   [FAIL] Python version too low, need 3.8+")
        return False
    print("   [PASS] Python version OK")
    
    # 2. 检查依赖包
    print("\n[2] Dependencies Check")
    required_packages = [
        ('appium', 'appium-python-client'),
        ('selenium', 'selenium'),
        ('pytest', 'pytest'),
        ('yaml', 'PyYAML'),
    ]
    
    missing_packages = []
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"   [PASS] {package_name}")
        except ImportError:
            print(f"   [FAIL] {package_name} (not installed)")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n   Please install: pip install {' '.join(missing_packages)}")
        return False
    
    # 3. 检查设备连接
    print("\n[3] Device Connection Check")
    import subprocess
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        devices = [line for line in lines[1:] if line.strip() and 'device' in line]
        
        if not devices:
            print("   [FAIL] No device connected")
            return False
        
        for device in devices:
            if 'unauthorized' in device:
                print(f"   [WARN] {device} (unauthorized, please allow USB debugging on device)")
            else:
                print(f"   [PASS] {device}")
    except Exception as e:
        print(f"   [FAIL] Check device failed: {e}")
        return False
    
    # 4. 检查Appium
    print("\n[4] Appium Service Check")
    try:
        import urllib.request
        import json
        response = urllib.request.urlopen('http://127.0.0.1:4723/wd/hub/status', timeout=5)
        data = json.loads(response.read().decode())
        print(f"   [PASS] Appium is running")
        version = data.get('value', {}).get('build', {}).get('version', 'unknown')
        print(f"   Version: {version}")
    except Exception as e:
        print(f"   [FAIL] Appium not running or cannot connect")
        print(f"   Please start Appium: appium")
        return False
    
    print("\n" + "=" * 60)
    print("[PASS] Environment check passed! Ready to run tests")
    print("=" * 60)
    return True


def run_simple_test():
    """运行简单测试"""
    print("\n" + "=" * 60)
    print("Running Simple Connection Test")
    print("=" * 60)
    
    try:
        from appium import webdriver
        from config.capabilities import get_android_capabilities
        
        print("\n[1] Creating device capabilities...")
        caps = get_android_capabilities()
        print(f"   Platform: {caps['platformName']}")
        print(f"   Device: {caps.get('deviceName', 'unknown')}")
        print(f"   App Package: {caps.get('appPackage', 'N/A')}")
        
        print("\n[2] Connecting to device...")
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)
        print("   [PASS] Device connected successfully!")
        
        print("\n[3] Getting device info...")
        size = driver.get_window_size()
        print(f"   Screen size: {size}")
        
        print("\n[4] Closing connection...")
        driver.quit()
        print("   [PASS] Connection closed")
        
        print("\n" + "=" * 60)
        print("[PASS] Simple test passed!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    # 检查环境
    if not check_environment():
        print("\n[FAIL] Environment check failed, please fix the issues above")
        sys.exit(1)
    
    # 运行简单测试
    print("\nRunning simple connection test...")
    run_simple_test()
