# 驱动工厂 - 创建和管理 WebDriver

from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.config import AppiumConfig, DeviceConfig
from config.capabilities import get_capabilities
from common.logger import logger


class DriverFactory:
    """
    WebDriver 工厂类
    
    用于创建和管理 WebDriver 实例
    """
    
    _instance = None
    _driver = None
    
    @classmethod
    def get_driver(cls, platform='android', app_path=None, **kwargs):
        """
        获取 WebDriver 实例（单例模式）
        
        Args:
            platform: 'android' 或 'ios'
            app_path: App 文件路径
            **kwargs: 其他配置
        """
        if cls._driver is None:
            cls._driver = cls.create_driver(platform, app_path, **kwargs)
        return cls._driver
    
    @classmethod
    def create_driver(cls, platform='android', app_path=None, **kwargs):
        """
        创建新的 WebDriver 实例
        
        Args:
            platform: 'android' 或 'ios'
            app_path: App 文件路径
            **kwargs: 其他配置
        """
        logger.info(f"创建 WebDriver (平台: {platform})")
        
        # 获取设备配置
        caps = get_capabilities(platform, app_path, **kwargs)
        
        # 创建 Options 对象
        if platform.lower() == 'android':
            options = UiAutomator2Options()
            options.load_capabilities(caps)
        else:
            options = None
        
        # 创建 WebDriver
        driver = webdriver.Remote(
            AppiumConfig.URL,
            options=options
        )
        
        # 设置隐式等待
        driver.implicitly_wait(DeviceConfig.IMPLICIT_WAIT)
        
        logger.info("WebDriver 创建成功")
        return driver
    
    @classmethod
    def quit_driver(cls):
        """
        关闭 WebDriver
        """
        if cls._driver:
            logger.info("关闭 WebDriver")
            cls._driver.quit()
            cls._driver = None
    
    @classmethod
    def restart_driver(cls, platform='android', app_path=None, **kwargs):
        """
        重启 WebDriver
        """
        cls.quit_driver()
        return cls.get_driver(platform, app_path, **kwargs)
