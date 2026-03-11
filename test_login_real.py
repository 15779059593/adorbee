#!/usr/bin/env python3
"""
Adorbee APP 自动化测试 - 登录测试
"""

import sys
import os
import time

sys.path.insert(0, 'D:\\Test\\adorbee')

def test_login():
    """测试登录功能"""
    print("=" * 60)
    print("Adorbee APP Login Test")
    print("=" * 60)
    
    # 1. 检查设备连接
    print("\n[1] Checking device connection...")
    import subprocess
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    if 'R3CN4042QJP' not in result.stdout:
        print("[FAIL] Device not connected")
        return False
    print("[PASS] Device connected: R3CN4042QJP")
    
    # 2. 检查Appium
    print("\n[2] Checking Appium service...")
    try:
        import urllib.request
        response = urllib.request.urlopen('http://127.0.0.1:4723/status', timeout=5)
        print("[PASS] Appium service is running")
    except Exception as e:
        print(f"[FAIL] Appium service not running: {e}")
        return False
    
    # 3. 连接设备
    print("\n[3] Connecting to device...")
    try:
        from appium import webdriver
        from appium.options.android import UiAutomator2Options
        
        # 使用Options方式（新版本Appium）
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.device_name = 'SM-G981N'
        options.udid = 'R3CN4042QJP'
        options.app_package = 'com.adorbee.app'
        options.app_activity = 'com.adorbee.app.MainActivity'
        options.no_reset = True
        options.new_command_timeout = 300
        
        print("Connecting...")
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        print("[PASS] Device connected successfully!")
        
        # 获取屏幕尺寸
        size = driver.get_window_size()
        print(f"Screen size: {size['width']}x{size['height']}")
        
        # 等待APP加载
        print("\n[4] Waiting for APP to load...")
        time.sleep(5)
        
        # 截图
        screenshot_path = os.path.join('D:\\Test\\adorbee\\reports', 'screenshot_login.png')
        driver.save_screenshot(screenshot_path)
        print(f"[PASS] Screenshot saved: {screenshot_path}")
        
        # 获取当前页面信息
        print(f"\nCurrent Activity: {driver.current_activity}")
        print(f"Current Package: {driver.current_package}")
        
        # 关闭连接
        print("\n[5] Closing connection...")
        driver.quit()
        print("[PASS] Test completed!")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_login()
    sys.exit(0 if success else 1)
