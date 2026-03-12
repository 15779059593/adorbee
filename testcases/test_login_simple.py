"""
登录功能测试用例 - 简化版
测试 adorbee APP 的账号登录功能
"""
import pytest
import allure
import yaml
import os
import time

from pages.login_page import LoginPage


def load_test_accounts():
    """加载测试账号配置"""
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'accounts.yaml')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('test_accounts', [])
    return []


@allure.feature("Login Module")
@allure.story("UI Interaction")
class TestLoginUI:
    """登录UI交互测试"""
    
    def test_get_selected_country(self, driver):
        """测试获取当前选择的国家/地区"""
        login_page = LoginPage(driver)
        
        country = login_page.get_selected_country()
        print(f"Selected Country/Region: {country}")
        assert country, "Should display country/region"
    
    def test_take_screenshot(self, driver):
        """测试截图功能"""
        login_page = LoginPage(driver)
        screenshot = login_page.take_screenshot("test_screenshot")
        print(f"Screenshot saved: {screenshot}")
        assert os.path.exists(screenshot), "Screenshot should be saved"
