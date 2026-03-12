# 全局配置

import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 设备配置
class DeviceConfig:
    """设备配置"""
    ANDROID_PLATFORM = 'Android'
    IOS_PLATFORM = 'iOS'
    
    # Android 默认配置 - 使用已连接的设备
    ANDROID_DEVICE_NAME = 'SM-G981N'  # Samsung Galaxy S20
    ANDROID_APP_PACKAGE = 'com.amv.adorbee'  # adorbee APP 包名
    ANDROID_APP_ACTIVITY = 'com.amv.adorbee.main.MainActivity'  # 主页面Activity
    ANDROID_PLATFORM_VERSION = '13'  # Android 版本
    
    # iOS 默认配置
    IOS_DEVICE_NAME = 'iPhone'
    IOS_BUNDLE_ID = 'com.adorbee.app'
    
    # 超时配置（秒）
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    
    # 轮询间隔
    POLLING_INTERVAL = 0.5

# 测试配置
class TestConfig:
    """测试配置"""
    # 测试环境
    ENV = 'test'  # test / staging / prod
    
    # 重试次数
    MAX_RETRY = 3
    
    # 截图配置
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = os.path.join(BASE_DIR, 'reports', 'screenshots')
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Appium Server 配置
class AppiumConfig:
    """Appium 配置"""
    HOST = '127.0.0.1'
    PORT = 4723
    # Appium 3.x 使用新的 URL 路径
    URL = f'http://{HOST}:{PORT}'
