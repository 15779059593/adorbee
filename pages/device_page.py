# 设备列表页 - 首页

from appium.webdriver.common.mobileby import MobileBy
from common.base_page import BasePage


class DevicePage(BasePage):
    """
    设备列表页（首页）
    
    对应 APP 的设备列表页面
    """
    
    # ==================== 页面元素 ====================
    
    # 顶部导航
    USER_AVATAR = (MobileBy.ID, "com.adorbee.app:id/iv_user_avatar")
    CLOUD_ICON = (MobileBy.ID, "com.adorbee.app:id/iv_cloud")
    MESSAGE_ICON = (MobileBy.ID, "com.adorbee.app:id/iv_message")
    ADD_DEVICE_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_add_device")
    
    # 设备卡片
    DEVICE_CARD = (MobileBy.ID, "com.adorbee.app:id/device_card")
    DEVICE_NAME = (MobileBy.ID, "com.adorbee.app:id/tv_device_name")
    DEVICE_PREVIEW = (MobileBy.ID, "com.adorbee.app:id/iv_preview")
    PLAY_BUTTON = (MobileBy.ID, "com.adorbee.app:id/iv_play")
    WIFI_SIGNAL = (MobileBy.ID, "com.adorbee.app:id/iv_wifi_signal")
    BATTERY_ICON = (MobileBy.ID, "com.adorbee.app:id/iv_battery")
    
    # 快捷功能按钮
    SUBSCRIPTION_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_subscription")
    SNOOZE_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_snooze")
    SHARE_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_share")
    SECURITY_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_security")
    SETTINGS_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_settings")
    
    # 底部导航
    NAV_DEVICE = (MobileBy.XPATH, "//android.widget.TextView[@text='设备']")
    NAV_EVENTS = (MobileBy.XPATH, "//android.widget.TextView[@text='事件']")
    NAV_HELP = (MobileBy.XPATH, "//android.widget.TextView[@text='帮助']")
    NAV_EXPLORE = (MobileBy.XPATH, "//android.widget.TextView[@text='探索']")
    
    # ==================== 页面操作 ====================
    
    def click_add_device(self):
        """
        点击添加设备按钮
        """
        self.click(self.ADD_DEVICE_BTN)
    
    def click_device_preview(self, index=0):
        """
        点击设备预览图进入直播
        
        Args:
            index: 设备索引，默认第一个
        """
        devices = self.find_elements(self.DEVICE_CARD)
        if devices and index < len(devices):
            devices[index].click()
        else:
            raise Exception(f"设备索引 {index} 不存在")
    
    def get_device_name(self, index=0) -> str:
        """
        获取设备名称
        """
        names = self.find_elements(self.DEVICE_NAME)
        if names and index < len(names):
            return names[index].text
        return ""
    
    def click_device_settings(self, index=0):
        """
        点击设备设置按钮
        """
        settings = self.find_elements(self.SETTINGS_BTN)
        if settings and index < len(settings):
            settings[index].click()
    
    def click_subscription(self, index=0):
        """
        点击订阅/套餐按钮
        """
        subs = self.find_elements(self.SUBSCRIPTION_BTN)
        if subs and index < len(subs):
            subs[index].click()
    
    def navigate_to_events(self):
        """
        导航到事件页
        """
        self.click(self.NAV_EVENTS)
    
    def navigate_to_help(self):
        """
        导航到帮助页
        """
        self.click(self.NAV_HELP)
    
    def navigate_to_explore(self):
        """
        导航到探索页
        """
        self.click(self.NAV_EXPLORE)
    
    def is_device_present(self) -> bool:
        """
        判断是否有设备存在
        """
        return len(self.find_elements(self.DEVICE_CARD)) > 0
    
    def get_device_count(self) -> int:
        """
        获取设备数量
        """
        return len(self.find_elements(self.DEVICE_CARD))
