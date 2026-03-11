#!/usr/bin/env python3
"""
Adorbee APP 自动化测试 - 简单连接测试
"""

import sys
import os

sys.path.insert(0, 'D:\\Test\\adorbee')

def simple_test():
    """简单连接测试"""
    print("=" * 60)
    print("Simple Connection Test")
    print("=" * 60)
    
    # 1. 检查设备
    print("\n[1] Device check...")
    import subprocess
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    print(result.stdout)
    
    if 'R3CN4042QJP' not in result.stdout:
        print("[FAIL] Device not found")
        return False
    print("[PASS] Device found")
    
    # 2. 检查Appium
    print("\n[2] Appium check...")
    try:
        import urllib.request
        response = urllib.request.urlopen('http://127.0.0.1:4723/status', timeout=5)
        data = response.read().decode()
        print(f"[PASS] Appium response: {data[:100]}...")
    except Exception as e:
        print(f"[FAIL] {e}")
        return False
    
    # 3. 尝试连接（不指定app，只连接设备）
    print("\n[3] Trying to connect without app...")
    try:
        from appium import webdriver
        from appium.options.android import UiAutomator2Options
        
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.device_name = 'SM-G981N'
        options.udid = 'R3CN4042QJP'
        # 不指定app，只获取当前页面
        
        print("Connecting (timeout 30s)...")
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        
        print("[PASS] Connected!")
        print(f"Current package: {driver.current_package}")
        print(f"Current activity: {driver.current_activity}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] {e}")
        return False


if __name__ == '__main__':
    simple_test()
