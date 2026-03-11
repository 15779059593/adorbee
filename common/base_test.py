# 测试用例基类

import pytest
from appium import webdriver

from config.config import AppiumConfig
from config.capabilities import get_capabilities
from common.logger import logger


class BaseTest:
    """
    测试用例基类
    
    所有测试类都应继承此类
    """
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, request):
        """
        测试前后的设置和清理
        """
        logger.info(f"========== 开始测试: {request.node.name} ==========")
        
        # 测试前设置
        self._setup()
        
        yield
        
        # 测试后清理
        self._teardown()
        logger.info(f"========== 结束测试: {request.node.name} ==========")
    
    def _setup(self):
        """
        测试前设置，子类可重写
        """
        pass
    
    def _teardown(self):
        """
        测试后清理，子类可重写
        """
        pass


class BaseMobileTest(BaseTest):
    """
    移动端测试基类
    
    提供 WebDriver 的自动管理
    """
    
    driver = None
    
    @pytest.fixture(autouse=True)
    def setup_driver(self, request):
        """
        设置和清理 WebDriver
        """
        # 获取测试类中定义的平台
        platform = getattr(self, 'platform', 'android')
        
        logger.info(f"初始化 WebDriver (平台: {platform})")
        
        # 创建设备配置
        caps = get_capabilities(platform)
        
        # 创建 WebDriver
        self.driver = webdriver.Remote(
            AppiumConfig.URL,
            desired_capabilities=caps
        )
        
        # 设置隐式等待
        from config.config import DeviceConfig
        self.driver.implicitly_wait(DeviceConfig.IMPLICIT_WAIT)
        
        logger.info("WebDriver 初始化完成")
        
        yield
        
        # 清理
        if self.driver:
            logger.info("关闭 WebDriver")
            self.driver.quit()
            self.driver = None
