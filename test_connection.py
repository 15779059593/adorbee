#!/usr/bin/env python3
"""
设备和Appium连接测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.device_utils import get_connected_devices, get_device_info, print_device_info


def check_appium():
    """检查Appium是否运行"""
    import urllib.request
    import json
    
    try:
        response = urllib.request.urlopen(
            'http://127.0.0.1:4723/wd/hub/status',
            timeout=5
        )
        data = json.loads(response.read().decode())
        return True, data.get('value', {}).get('build', {}).get('version', 'unknown')
    except Exception as e:
        return False, str(e)


def test_device_connection():
    """测试设备连接"""
    print("=" * 60)
    print("设备连接测试")
    print("=" * 60)
    
    # 获取设备列表
    devices = get_connected_devices()
    
    if not devices:
        print("[FAIL] 未检测到连接的设备")
        return False
    
    print(f"[PASS] 检测到 {len(devices)} 个设备")
    
    # 显示设备信息
    for serial in devices:
        info = get_device_info(serial)
        print(f"\n设备: {serial}")
        print(f"  型号: {info.get('model', 'N/A')}")
        print(f"  Android: {info.get('android_version', 'N/A')}")
    
    return True


def test_appium_connection():
    """测试Appium连接"""
    print("\n" + "=" * 60)
    print("Appium连接测试")
    print("=" * 60)
    
    is_running, version = check_appium()
    
    if is_running:
        print(f"[PASS] Appium运行正常")
        print(f"  版本: {version}")
        return True
    else:
        print(f"[FAIL] Appium未运行或无法连接")
        print(f"  错误: {version}")
        return False


def test_full_connection():
    """测试完整连接（设备+Appium）"""
    print("\n" + "=" * 60)
    print("完整连接测试")
    print("=" * 60)
    
    # 检查设备
    devices = get_connected_devices()
    if not devices:
        print("[FAIL] 没有连接的设备")
        return False
    
    # 检查Appium
    is_running, _ = check_appium()
    if not is_running:
        print("[FAIL] Appium未运行")
        return False
    
    print("[PASS] 设备和Appium都正常")
    
    # 尝试创建WebDriver连接
    try:
        from appium import webdriver
        from utils.device_utils import get_first_device_capabilities
        
        print("\n尝试连接设备...")
        caps = get_first_device_capabilities()
        
        print(f"配置信息:")
        print(f"  platformName: {caps['platformName']}")
        print(f"  deviceName: {caps['deviceName']}")
        print(f"  udid: {caps['udid']}")
        
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)
        
        print("[PASS] WebDriver连接成功!")
        print(f"  屏幕尺寸: {driver.get_window_size()}")
        
        # 关闭连接
        driver.quit()
        print("[PASS] 连接已关闭")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] WebDriver连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n" + "*" * 60)
    print("* Adorbee 自动化测试 - 连接测试")
    print("*" * 60)
    
    # 显示设备信息
    print_device_info()
    
    # 测试设备连接
    device_ok = test_device_connection()
    
    # 测试Appium
    appium_ok = test_appium_connection()
    
    # 如果都正常，测试完整连接
    if device_ok and appium_ok:
        test_full_connection()
    else:
        print("\n[SKIP] 跳过完整连接测试（设备或Appium未就绪）")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
