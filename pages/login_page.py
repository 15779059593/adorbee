# 登录页面 - 处理 adorbee APP 的登录相关操作

from appium.webdriver.common.appiumby import AppiumBy
from common.base_page import BasePage
import time
import allure


class LoginPage(BasePage):
    """
    登录页面 - adorbee APP
    
    包名: com.amv.adorbee
    Activity: com.amv.adorbee.login.LoginActivity
    """
    
    # ==================== 页面元素 ====================
    
    # 账号输入框
    USERNAME_INPUT = (AppiumBy.ID, "com.amv.adorbee:id/login_name_et")
    
    # 密码输入框
    PASSWORD_INPUT = (AppiumBy.ID, "com.amv.adorbee:id/login_password_et")
    
    # 登录按钮
    LOGIN_BUTTON = (AppiumBy.ID, "com.amv.adorbee:id/login_user_bt")
    
    # 清除账号按钮
    CLEAR_EMAIL_BTN = (AppiumBy.ID, "com.amv.adorbee:id/login_delete_email_iv")
    
    # 显示/隐藏密码按钮
    SHOW_PASSWORD_BTN = (AppiumBy.ID, "com.amv.adorbee:id/login_password_show_iv")
    
    # 忘记密码链接
    FORGOT_PASSWORD_LINK = (AppiumBy.ID, "com.amv.adorbee:id/tv_forget_password")
    
    # 注册链接
    REGISTER_LINK = (AppiumBy.ID, "com.amv.adorbee:id/tv_to_register")
    
    # 国家/地区选择
    COUNTRY_SELECTOR = (AppiumBy.ID, "com.amv.adorbee:id/ll_country")
    COUNTRY_TEXT = (AppiumBy.ID, "com.amv.adorbee:id/tv_region")
    
    # 联系我们
    CONTACT_US = (AppiumBy.ID, "com.amv.adorbee:id/tv_contact_us")
    
    # 登录成功指示元素（首页）
    ADD_DEVICE_BTN = (AppiumBy.ID, "com.amv.adorbee:id/iv_add_device")
    DEVICE_LIST = (AppiumBy.ID, "com.amv.adorbee:id/recycler_view")
    
    # 错误提示（Toast 或页面内提示）
    ERROR_TOAST = (AppiumBy.XPATH, "//android.widget.Toast")
    
    # ==================== 页面操作 ====================
    
    def input_username(self, username: str):
        """
        输入账号（邮箱）
        """
        # 先清除已有内容
        if self.is_element_present(self.CLEAR_EMAIL_BTN, timeout=2):
            self.click(self.CLEAR_EMAIL_BTN)
        
        self.send_keys(self.USERNAME_INPUT, username)
        self.logger.info(f"输入账号: {username}")
    
    def input_password(self, password: str):
        """
        输入密码
        """
        self.send_keys(self.PASSWORD_INPUT, password)
        self.logger.info("输入密码: ********")
    
    def click_login_button(self):
        """
        点击登录按钮
        """
        self.click(self.LOGIN_BUTTON)
        self.logger.info("点击登录按钮")
        time.sleep(2)  # 等待登录响应
    
    def click_clear_email(self):
        """
        点击清除账号按钮
        """
        if self.is_element_present(self.CLEAR_EMAIL_BTN, timeout=2):
            self.click(self.CLEAR_EMAIL_BTN)
            self.logger.info("清除账号输入")
    
    def toggle_password_visibility(self):
        """
        切换密码显示/隐藏
        """
        self.click(self.SHOW_PASSWORD_BTN)
        self.logger.info("切换密码显示状态")
    
    def click_forgot_password(self):
        """
        点击忘记密码
        """
        self.click(self.FORGOT_PASSWORD_LINK)
        self.logger.info("点击忘记密码")
    
    def click_register(self):
        """
        点击注册
        """
        self.click(self.REGISTER_LINK)
        self.logger.info("点击注册")
    
    def select_country(self):
        """
        点击国家/地区选择
        """
        self.click(self.COUNTRY_SELECTOR)
        self.logger.info("点击国家/地区选择")
    
    def get_selected_country(self) -> str:
        """
        获取当前选择的国家/地区
        """
        return self.get_text(self.COUNTRY_TEXT)
    
    def login(self, username: str, password: str):
        """
        执行完整登录流程
        
        Args:
            username: 邮箱账号
            password: 密码
        """
        self.logger.info(f"开始登录流程")
        
        with allure.step(f"输入账号: {username}"):
            self.input_username(username)
        
        with allure.step("输入密码"):
            self.input_password(password)
        
        with allure.step("点击登录"):
            self.click_login_button()
        
        self.logger.info("登录操作完成")
    
    def is_login_success(self, timeout=10) -> bool:
        """
        判断是否登录成功
        
        通过检查首页元素是否存在来判断
        """
        # 检查是否出现首页元素
        indicators = [
            self.ADD_DEVICE_BTN,
            self.DEVICE_LIST,
            (AppiumBy.XPATH, "//*[@text='设备' or @text='Devices']"),
        ]
        
        for indicator in indicators:
            if self.is_element_present(indicator, timeout=timeout):
                self.logger.info("检测到登录成功（首页元素存在）")
                return True
        
        return False
    
    def is_on_login_page(self) -> bool:
        """
        判断是否在当前登录页面
        """
        return self.is_element_present(self.LOGIN_BUTTON, timeout=3) or \
               self.is_element_present(self.USERNAME_INPUT, timeout=2)
    
    def clear_inputs(self):
        """
        清空输入框
        """
        try:
            self.click_clear_email()
        except:
            pass
        
        try:
            password_field = self.find_element(self.PASSWORD_INPUT)
            password_field.clear()
        except:
            pass
        
        self.logger.info("清空输入框")
    
    def get_error_message(self) -> str:
        """
        获取错误提示信息（如果有）
        """
        # 尝试获取 Toast 消息
        try:
            toast = self.find_element(self.ERROR_TOAST)
            return toast.text
        except:
            pass
        
        return ""
