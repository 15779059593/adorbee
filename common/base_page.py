# 页面基类 - 封装常用操作方法

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
import allure
import os
from datetime import datetime

from config.config import DeviceConfig, TestConfig, BASE_DIR
from common.logger import logger


class BasePage:
    """
    页面基类，封装所有页面共用的操作方法
    
    所有页面对象都应继承此类
    """
    
    def __init__(self, driver: WebDriver):
        """
        初始化
        
        Args:
            driver: WebDriver 实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, DeviceConfig.EXPLICIT_WAIT, DeviceConfig.POLLING_INTERVAL)
        self.logger = logger
        logger.info(f"初始化页面: {self.__class__.__name__}")
    
    # ==================== 元素定位 ====================
    
    def find_element(self, locator) -> WebElement:
        """
        查找单个元素
        
        Args:
            locator: 定位元组，如 (MobileBy.ID, "com.adorbee.app:id/button")
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"找到元素: {locator}")
            return element
        except TimeoutException:
            logger.error(f"查找元素超时: {locator}")
            self.take_screenshot(f"element_not_found_{datetime.now().strftime('%H%M%S')}")
            raise
    
    def find_elements(self, locator) -> list:
        """
        查找多个元素
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"找到 {len(elements)} 个元素: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"查找元素超时: {locator}")
            return []
    
    def is_element_present(self, locator, timeout=5) -> bool:
        """
        判断元素是否存在
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    # ==================== 元素操作 ====================
    
    def click(self, locator):
        """
        点击元素
        """
        element = self.find_element(locator)
        element.click()
        logger.info(f"点击元素: {locator}")
    
    def send_keys(self, locator, text: str):
        """
        输入文本
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"输入文本 '{text}' 到: {locator}")
    
    def get_text(self, locator) -> str:
        """
        获取元素文本
        """
        element = self.find_element(locator)
        text = element.text
        logger.info(f"获取文本 '{text}' 从: {locator}")
        return text
    
    def get_attribute(self, locator, attribute: str) -> str:
        """
        获取元素属性
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.info(f"获取属性 '{attribute}={value}' 从: {locator}")
        return value
    
    # ==================== 手势操作 ====================
    
    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        滑动操作
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        logger.info(f"滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
    
    def swipe_up(self, duration=1000):
        """
        向上滑动
        """
        size = self.driver.get_window_size()
        self.swipe(size['width'] * 0.5, size['height'] * 0.8, 
                   size['width'] * 0.5, size['height'] * 0.2, duration)
    
    def swipe_down(self, duration=1000):
        """
        向下滑动
        """
        size = self.driver.get_window_size()
        self.swipe(size['width'] * 0.5, size['height'] * 0.2, 
                   size['width'] * 0.5, size['height'] * 0.8, duration)
    
    def swipe_left(self, duration=1000):
        """
        向左滑动
        """
        size = self.driver.get_window_size()
        self.swipe(size['width'] * 0.8, size['height'] * 0.5, 
                   size['width'] * 0.2, size['height'] * 0.5, duration)
    
    def swipe_right(self, duration=1000):
        """
        向右滑动
        """
        size = self.driver.get_window_size()
        self.swipe(size['width'] * 0.2, size['height'] * 0.5, 
                   size['width'] * 0.8, size['height'] * 0.5, duration)
    
    def tap(self, x, y):
        """
        点击坐标
        """
        self.driver.tap([(x, y)])
        logger.info(f"点击坐标: ({x}, {y})")
    
    # ==================== 等待方法 ====================
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        等待元素可见
        """
        timeout = timeout or DeviceConfig.EXPLICIT_WAIT
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_invisible(self, locator, timeout=None):
        """
        等待元素不可见
        """
        timeout = timeout or DeviceConfig.EXPLICIT_WAIT
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    def sleep(self, seconds: float):
        """
        强制等待（不推荐，尽量使用显式等待）
        """
        import time
        time.sleep(seconds)
    
    # ==================== 截图 ====================
    
    def take_screenshot(self, filename=None):
        """
        截图
        """
        if filename is None:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        screenshot_dir = TestConfig.SCREENSHOT_DIR
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        logger.info(f"截图保存: {filepath}")
        
        # 添加到 Allure 报告
        with open(filepath, 'rb') as f:
            allure.attach(f.read(), filename, allure.attachment_type.PNG)
        
        return filepath
    
    # ==================== 系统操作 ====================
    
    def get_window_size(self):
        """
        获取屏幕尺寸
        """
        return self.driver.get_window_size()
    
    def press_keycode(self, keycode):
        """
        按物理按键（Android）
        """
        self.driver.press_keycode(keycode)
    
    def hide_keyboard(self):
        """
        隐藏键盘
        """
        try:
            self.driver.hide_keyboard()
        except:
            pass
    
    def launch_app(self):
        """
        启动应用
        """
        self.driver.launch_app()
        logger.info("启动应用")
    
    def close_app(self):
        """
        关闭应用
        """
        self.driver.close_app()
        logger.info("关闭应用")
    
    def reset_app(self):
        """
        重置应用
        """
        self.driver.reset()
        logger.info("重置应用")
