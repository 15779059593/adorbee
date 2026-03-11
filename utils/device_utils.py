# 设备配置工具 - 自动获取连接的设备信息

import subprocess
import re


def get_connected_devices():
    """
    获取已连接的Android设备列表
    
    Returns:
        list: 设备序列号列表
    """
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
        lines = result.stdout.strip().split('\n')
        devices = []
        for line in lines[1:]:
            if '\tdevice' in line:
                serial = line.split('\t')[0]
                devices.append(serial)
        return devices
    except Exception as e:
        print(f"获取设备列表失败: {e}")
        return []


def get_device_info(serial):
    """
    获取设备详细信息
    
    Args:
        serial: 设备序列号
    
    Returns:
        dict: 设备信息
    """
    info = {'serial': serial}
    
    try:
        # 获取设备型号
        result = subprocess.run(
            ['adb', '-s', serial, 'shell', 'getprop', 'ro.product.model'],
            capture_output=True, text=True, timeout=5
        )
        info['model'] = result.stdout.strip()
        
        # 获取Android版本
        result = subprocess.run(
            ['adb', '-s', serial, 'shell', 'getprop', 'ro.build.version.release'],
            capture_output=True, text=True, timeout=5
        )
        info['android_version'] = result.stdout.strip()
        
        # 获取屏幕尺寸
        result = subprocess.run(
            ['adb', '-s', serial, 'shell', 'wm', 'size'],
            capture_output=True, text=True, timeout=5
        )
        size_match = re.search(r'(\d+)x(\d+)', result.stdout)
        if size_match:
            info['screen_width'] = int(size_match.group(1))
            info['screen_height'] = int(size_match.group(2))
        
    except Exception as e:
        print(f"获取设备信息失败: {e}")
    
    return info


def print_device_info():
    """
    打印所有连接设备的信息
    """
    devices = get_connected_devices()
    
    if not devices:
        print("未检测到连接的设备")
        return
    
    print("=" * 60)
    print("已连接的设备:")
    print("=" * 60)
    
    for i, serial in enumerate(devices, 1):
        info = get_device_info(serial)
        print(f"\n设备 {i}:")
        print(f"  序列号: {info.get('serial', 'N/A')}")
        print(f"  型号: {info.get('model', 'N/A')}")
        print(f"  Android版本: {info.get('android_version', 'N/A')}")
        if 'screen_width' in info:
            print(f"  屏幕尺寸: {info['screen_width']}x{info['screen_height']}")
    
    print("\n" + "=" * 60)


def get_first_device_capabilities():
    """
    获取第一个连接设备的Appium配置
    
    Returns:
        dict: Appium capabilities
    """
    devices = get_connected_devices()
    if not devices:
        raise Exception("没有连接的设备")
    
    serial = devices[0]
    info = get_device_info(serial)
    
    from config.config import DeviceConfig
    
    caps = {
        'platformName': 'Android',
        'deviceName': info.get('model', 'Android Device'),
        'udid': serial,
        'automationName': 'UiAutomator2',
        'newCommandTimeout': 300,
        'noReset': True,
        'fullReset': False,
        'autoGrantPermissions': True,
        'unicodeKeyboard': True,
        'resetKeyboard': True,
        'appPackage': DeviceConfig.ANDROID_APP_PACKAGE,
        'appActivity': DeviceConfig.ANDROID_APP_ACTIVITY,
    }
    
    return caps


if __name__ == '__main__':
    print_device_info()
