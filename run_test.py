#!/usr/bin/env python3
"""
Adorbee APP 自动化测试 - 快速连接测试
使用已运行的Appium连接设备
"""

import sys
import os
import time

sys.path.insert(0, 'D:\\Test\\adorbee')

def run_test():
    """运行测试"""
    print("=" * 60)
    print("Adorbee APP Automation Test")
    print("=" * 60)
    
    # 1. 设备检查
    print("\n[1] Device Check")
    import subprocess
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    if 'R3CN4042QJP' in result.stdout and 'device' in result.stdout:
        print("  [PASS] Device R3CN4042QJP connected")
    else:
        print("  [FAIL] Device not connected")
        return False
    
    # 2. Appium检查
    print("\n[2] Appium Check")
    try:
        import urllib.request
        response = urllib.request.urlopen('http://127.0.0.1:4723/status', timeout=5)
        print("  [PASS] Appium is running")
    except Exception as e:
        print(f"  [FAIL] Appium error: {e}")
        return False
    
    # 3. 启动APP
    print("\n[3] Launch APP")
    subprocess.run(['adb', '-s', 'R3CN4042QJP', 'shell', 'am', 'start', '-n', 'com.adorbee.app/com.adorbee.app.MainActivity'], 
                   capture_output=True)
    print("  [PASS] APP launch command sent")
    time.sleep(3)
    
    # 4. 连接测试
    print("\n[4] Connect to Device")
    try:
        from appium import webdriver
        from appium.options.android import UiAutomator2Options
        
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.device_name = 'SM-G981N'
        options.udid = 'R3CN4042QJP'
        options.no_reset = True
        options.new_command_timeout = 300
        
        print("  Connecting...")
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        print("  [PASS] Connected successfully!")
        
        # 获取信息
        print(f"\n[5] Device Info")
        print(f"  Package: {driver.current_package}")
        print(f"  Activity: {driver.current_activity}")
        size = driver.get_window_size()
        print(f"  Screen: {size['width']}x{size['height']}")
        
        # 截图
        print(f"\n[6] Screenshot")
        screenshot_path = 'D:\\Test\\adorbee\\reports\\test_result.png'
        driver.save_screenshot(screenshot_path)
        print(f"  [PASS] Saved: {screenshot_path}")
        
        # 关闭
        driver.quit()
        print(f"\n[7] Test Complete")
        print("  [PASS] All tests passed!")
        return True
        
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
        return False

if __name__ == '__main__':
    success = run_test()
    print("\n" + "=" * 60)
    if success:
        print("RESULT: SUCCESS")
    else:
        print("RESULT: FAILED")
    print("=" * 60)
    sys.exit(0 if success else 1)
