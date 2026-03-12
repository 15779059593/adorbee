"""
登录功能测试用例
测试 adorbee APP 的账号登录功能
"""
import pytest
import allure
import yaml
import os
from appium.webdriver.common.mobileby import MobileBy

from pages.login_page import LoginPage


# 加载测试账号数据
def load_test_accounts():
    """加载测试账号配置"""
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'accounts.yaml')
    with open(data_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('test_accounts', [])


@allure.feature("登录模块")
@allure.story("正常登录流程")
class TestNormalLogin:
    """正常登录测试"""
    
    @allure.title("使用有效账号密码登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, driver):
        """
        测试场景：使用正确的账号密码登录
        预期结果：登录成功，跳转到设备列表页
        """
        login_page = LoginPage(driver)
        
        # 获取测试账号
        accounts = load_test_accounts()
        if not accounts:
            pytest.skip("未配置测试账号，请在 data/accounts.yaml 中添加")
        
        account = accounts[0]
        username = account['username']
        password = account['password']
        
        with allure.step(f"步骤1: 输入账号 {username}"):
            login_page.input_username(username)
        
        with allure.step("步骤2: 输入密码"):
            login_page.input_password(password)
        
        with allure.step("步骤3: 点击登录按钮"):
            login_page.click_login_button()
        
        with allure.step("步骤4: 验证登录成功"):
            assert login_page.is_login_success(timeout=10), "登录失败，未进入首页"
            login_page.take_screenshot("login_success")
    
    @allure.title("登录后显示添加设备按钮")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_shows_add_device(self, driver):
        """
        测试场景：登录成功后显示添加设备按钮
        预期结果：能看到添加设备按钮
        """
        login_page = LoginPage(driver)
        
        accounts = load_test_accounts()
        if not accounts:
            pytest.skip("未配置测试账号")
        
        # 执行登录
        account = accounts[0]
        login_page.login(account['username'], account['password'])
        
        with allure.step("验证首页元素"):
            # 检查是否有添加设备按钮
            has_add_btn = login_page.is_element_present(
                login_page.ADD_DEVICE_BTN, timeout=10
            )
            
            assert has_add_btn, "登录后未显示添加设备按钮"


@allure.feature("登录模块")
@allure.story("异常登录场景")
class TestAbnormalLogin:
    """异常登录测试"""
    
    @allure.title("使用错误密码登录")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_wrong_password(self, driver):
        """
        测试场景：使用正确的账号但错误的密码
        预期结果：登录失败，显示错误提示
        """
        login_page = LoginPage(driver)
        
        accounts = load_test_accounts()
        if not accounts:
            pytest.skip("未配置测试账号")
        
        username = accounts[0]['username']
        wrong_password = "wrong_password_123"
        
        with allure.step(f"输入正确账号: {username}"):
            login_page.input_username(username)
        
        with allure.step(f"输入错误密码: {wrong_password}"):
            login_page.input_password(wrong_password)
        
        with allure.step("点击登录"):
            login_page.click_login_button()
        
        with allure.step("验证登录失败"):
            # 验证仍在登录页或显示错误
            is_still_login = login_page.is_on_login_page()
            
            assert is_still_login, "错误密码不应登录成功"
            login_page.take_screenshot("login_wrong_password")
    
    @allure.title("使用不存在的账号登录")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_nonexistent_user(self, driver):
        """
        测试场景：使用不存在的账号
        预期结果：登录失败
        """
        login_page = LoginPage(driver)
        
        with allure.step("输入不存在的账号"):
            login_page.input_username("nonexistent@test.com")
        
        with allure.step("输入任意密码"):
            login_page.input_password("some_password")
        
        with allure.step("点击登录"):
            login_page.click_login_button()
        
        with allure.step("验证登录失败"):
            assert not login_page.is_login_success(timeout=5), "不存在的账号不应登录成功"
    
    @allure.title("空账号登录")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_with_empty_username(self, driver):
        """
        测试场景：账号为空
        预期结果：登录失败，保持在登录页
        """
        login_page = LoginPage(driver)
        
        with allure.step("输入空账号"):
            login_page.input_username("")
        
        with allure.step("输入密码"):
            login_page.input_password("some_password")
        
        with allure.step("点击登录"):
            login_page.click_login_button()
        
        with allure.step("验证仍在登录页面"):
            assert login_page.is_on_login_page() or not login_page.is_login_success(), \
                "空账号不应登录成功"
    
    @allure.title("空密码登录")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_with_empty_password(self, driver):
        """
        测试场景：密码为空
        预期结果：登录失败
        """
        login_page = LoginPage(driver)
        
        accounts = load_test_accounts()
        if not accounts:
            pytest.skip("未配置测试账号")
        
        with allure.step("输入账号"):
            login_page.input_username(accounts[0]['username'])
        
        with allure.step("输入空密码"):
            login_page.input_password("")
        
        with allure.step("点击登录"):
            login_page.click_login_button()
        
        with allure.step("验证登录失败"):
            assert not login_page.is_login_success(timeout=5), "空密码不应登录成功"


@allure.feature("登录模块")
@allure.story("安全测试")
class TestLoginSecurity:
    """登录安全测试"""
    
    @allure.title("SQL注入攻击测试")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sql_injection_attempt(self, driver):
        """
        测试场景：尝试SQL注入攻击
        预期结果：登录失败，系统安全
        """
        login_page = LoginPage(driver)
        
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "admin'--",
            "' OR 1=1#",
        ]
        
        for payload in sql_payloads:
            with allure.step(f"测试SQL注入: {payload}"):
                login_page.clear_inputs()
                login_page.input_username(payload)
                login_page.input_password(payload)
                login_page.click_login_button()
                
                # 验证未登录成功
                assert not login_page.is_login_success(timeout=3), \
                    f"SQL注入不应成功: {payload}"
    
    @allure.title("XSS攻击测试")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_xss_attempt(self, driver):
        """
        测试场景：尝试XSS攻击
        预期结果：系统正常处理，不执行脚本
        """
        login_page = LoginPage(driver)
        
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
        ]
        
        for payload in xss_payloads:
            with allure.step(f"测试XSS: {payload[:30]}..."):
                login_page.clear_inputs()
                login_page.input_username(payload)
                login_page.input_password("password")
                login_page.click_login_button()
                
                # 验证未登录成功，且系统未崩溃
                assert not login_page.is_login_success(timeout=3), \
                    f"XSS攻击不应成功"
                
                # 验证仍在登录页（系统未崩溃）
                assert login_page.is_on_login_page(), "系统可能已崩溃"


@allure.feature("登录模块")
@allure.story("UI交互测试")
class TestLoginUI:
    """登录UI交互测试"""
    
    @allure.title("密码显示/隐藏切换")
    @allure.severity(allure.severity_level.MINOR)
    def test_password_visibility_toggle(self, driver):
        """
        测试场景：点击密码显示/隐藏按钮
        预期结果：密码明文/密文切换
        """
        login_page = LoginPage(driver)
        
        with allure.step("输入密码"):
            login_page.input_password("test_password")
        
        with allure.step("点击显示密码按钮"):
            login_page.toggle_password_visibility()
            allure.attach("密码显示切换成功", "结果", allure.attachment_type.TEXT)
    
    @allure.title("点击忘记密码链接")
    @allure.severity(allure.severity_level.MINOR)
    def test_forgot_password_link(self, driver):
        """
        测试场景：点击忘记密码
        预期结果：跳转到找回密码页面
        """
        login_page = LoginPage(driver)
        
        with allure.step("点击忘记密码链接"):
            login_page.click_forgot_password()
        
        with allure.step("验证跳转到找回密码页"):
            # 检查页面是否变化（通过检查是否不在登录页）
            time.sleep(2)
            is_login_page = login_page.is_on_login_page()
            assert not is_login_page, "未跳转到找回密码页面"
    
    @allure.title("点击注册链接")
    @allure.severity(allure.severity_level.MINOR)
    def test_register_link(self, driver):
        """
        测试场景：点击注册账号
        预期结果：跳转到注册页面
        """
        login_page = LoginPage(driver)
        
        with allure.step("点击注册链接"):
            login_page.click_register()
        
        with allure.step("验证跳转到注册页"):
            time.sleep(2)
            is_login_page = login_page.is_on_login_page()
            assert not is_login_page, "未跳转到注册页面"
    
    @allure.title("获取当前选择的国家/地区")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_selected_country(self, driver):
        """
        测试场景：获取当前选择的国家/地区
        预期结果：返回国家名称
        """
        login_page = LoginPage(driver)
        
        with allure.step("获取当前国家/地区"):
            country = login_page.get_selected_country()
            allure.attach(f"当前选择: {country}", "国家/地区", allure.attachment_type.TEXT)
            assert country, "应显示国家/地区"


import time
