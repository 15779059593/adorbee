# 测试用例示例 - 设备管理测试

import pytest
import allure

from common.base_test import BaseMobileTest
from pages.device_page import DevicePage
from pages.live_page import LivePage


@allure.feature("设备管理")
class TestDevice(BaseMobileTest):
    """
    设备管理相关测试用例
    """
    
    platform = 'android'
    
    @allure.story("设备列表显示")
    @allure.title("验证设备列表正常显示")
    def test_device_list_display(self):
        """
        测试设备列表是否正常显示
        """
        device_page = DevicePage(self.driver)
        
        # 验证设备列表存在
        assert device_page.is_device_present(), "设备列表为空"
        
        # 获取设备数量
        count = device_page.get_device_count()
        allure.attach(f"设备数量: {count}", "设备统计")
        
        # 验证至少有一个设备
        assert count > 0, "设备数量应该大于0"
    
    @allure.story("进入直播")
    @allure.title("点击设备预览进入直播页")
    def test_enter_live(self):
        """
        测试点击设备预览图进入直播页面
        """
        device_page = DevicePage(self.driver)
        
        # 点击第一个设备的预览图
        device_page.click_device_preview(0)
        
        # 验证进入直播页
        live_page = LivePage(self.driver)
        assert live_page.is_element_present(live_page.VIDEO_VIEW), "未进入直播页"
        
        # 返回设备列表
        live_page.click_back()
    
    @allure.story("设备设置")
    @allure.title("进入设备设置页面")
    def test_device_settings(self):
        """
        测试进入设备设置页面
        """
        device_page = DevicePage(self.driver)
        
        # 点击第一个设备的设置按钮
        device_page.click_device_settings(0)
        
        # 验证设置页面元素（这里需要根据实际情况添加设置页的定位）
        # assert device_page.is_element_present(DevicePage.SETTINGS_TITLE)
        
        # 返回
        device_page.click_back()
    
    @allure.story("底部导航")
    @allure.title("切换底部导航栏")
    def test_bottom_navigation(self):
        """
        测试底部导航栏切换
        """
        device_page = DevicePage(self.driver)
        
        # 切换到事件页
        device_page.navigate_to_events()
        # 这里可以添加事件页的验证
        
        # 切换到帮助页
        device_page.navigate_to_help()
        # 这里可以添加帮助页的验证
        
        # 切换到探索页
        device_page.navigate_to_explore()
        # 这里可以添加探索页的验证
        
        # 切回设备页
        device_page.navigate_to_device()
        assert device_page.is_element_present(DevicePage.DEVICE_CARD), "未返回设备页"


@allure.feature("直播功能")
class TestLive(BaseMobileTest):
    """
    直播功能相关测试用例
    """
    
    platform = 'android'
    
    @pytest.fixture(autouse=True)
    def enter_live(self):
        """
        每个测试前进入直播页
        """
        device_page = DevicePage(self.driver)
        device_page.click_device_preview(0)
        self.live_page = LivePage(self.driver)
        yield
        # 测试后返回
        if self.live_page.is_element_present(self.live_page.BACK_BTN):
            self.live_page.click_back()
    
    @allure.story("截图功能")
    @allure.title("直播页面截图")
    def test_live_screenshot(self):
        """
        测试直播页面截图功能
        """
        # 点击截图按钮
        self.live_page.take_screenshot()
        
        # 验证截图成功（这里可以根据实际情况添加验证）
        # 例如：检查是否有截图成功的提示
    
    @allure.story("清晰度切换")
    @allure.title("切换视频清晰度")
    def test_switch_quality(self):
        """
        测试切换视频清晰度
        """
        # 获取当前清晰度
        current_quality = self.live_page.get_current_quality()
        allure.attach(f"当前清晰度: {current_quality}", "清晰度信息")
        
        # 切换到另一种清晰度
        if current_quality == 'SD':
            self.live_page.switch_quality('HD')
            expected = 'HD'
        else:
            self.live_page.switch_quality('SD')
            expected = 'SD'
        
        # 验证切换成功
        new_quality = self.live_page.get_current_quality()
        assert new_quality == expected, f"清晰度切换失败，期望 {expected}，实际 {new_quality}"
    
    @allure.story("云台控制")
    @allure.title("云台方向控制")
    def test_ptz_control(self):
        """
        测试云台方向控制
        """
        # 向上滑动
        self.live_page.swipe_video('up')
        
        # 向下滑动
        self.live_page.swipe_video('down')
        
        # 向左滑动
        self.live_page.swipe_video('left')
        
        # 向右滑动
        self.live_page.swipe_video('right')
        
        # 云台控制主要是验证滑动操作不报错
        # 实际效果需要通过视频画面变化来验证
