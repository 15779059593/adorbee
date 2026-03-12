# Appium Desired Capabilities 配置

from config.config import DeviceConfig

def get_android_capabilities(app_path=None, no_reset=True):
    """
    获取 Android 设备配置
    
    Args:
        app_path: APK 文件路径，None 表示使用已安装的 App
        no_reset: True 表示不重置应用数据，False 表示每次重置
    """
    caps = {
        'platformName': DeviceConfig.ANDROID_PLATFORM,
        'platformVersion': DeviceConfig.ANDROID_PLATFORM_VERSION,
        'deviceName': DeviceConfig.ANDROID_DEVICE_NAME,
        'automationName': 'UiAutomator2',
        'newCommandTimeout': 300,
        'noReset': no_reset,
        'fullReset': False,
        'autoGrantPermissions': True,
        'unicodeKeyboard': True,
        'resetKeyboard': True,
    }
    
    if app_path:
        caps['app'] = app_path
    else:
        caps['appPackage'] = DeviceConfig.ANDROID_APP_PACKAGE
        caps['appActivity'] = DeviceConfig.ANDROID_APP_ACTIVITY
    
    return caps


def get_ios_capabilities(app_path=None, no_reset=True):
    """
    获取 iOS 设备配置
    
    Args:
        app_path: IPA 文件路径或 App 路径
        no_reset: True 表示不重置应用数据
    """
    caps = {
        'platformName': DeviceConfig.IOS_PLATFORM,
        'deviceName': DeviceConfig.IOS_DEVICE_NAME,
        'automationName': 'XCUITest',
        'newCommandTimeout': 300,
        'noReset': no_reset,
        'fullReset': False,
        'autoAcceptAlerts': True,
    }
    
    if app_path:
        caps['app'] = app_path
    else:
        caps['bundleId'] = DeviceConfig.IOS_BUNDLE_ID
    
    return caps


def get_capabilities(platform='android', app_path=None, **kwargs):
    """
    获取设备配置
    
    Args:
        platform: 'android' 或 'ios'
        app_path: App 文件路径
        **kwargs: 其他自定义配置
    """
    if platform.lower() == 'android':
        caps = get_android_capabilities(app_path)
    elif platform.lower() == 'ios':
        caps = get_ios_capabilities(app_path)
    else:
        raise ValueError(f"不支持的平台: {platform}")
    
    # 更新自定义配置
    caps.update(kwargs)
    return caps
