# 直播页

from appium.webdriver.common.mobileby import MobileBy
from common.base_page import BasePage


class LivePage(BasePage):
    """
    直播页
    
    对应 APP 的实时预览页面
    """
    
    # ==================== 页面元素 ====================
    
    # 顶部栏
    BACK_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_back")
    DEVICE_NAME = (MobileBy.ID, "com.adorbee.app:id/tv_device_name")
    WIFI_SIGNAL = (MobileBy.ID, "com.adorbee.app:id/iv_wifi_signal")
    BATTERY_ICON = (MobileBy.ID, "com.adorbee.app:id/iv_battery")
    SETTINGS_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_settings")
    
    # 视频区域
    VIDEO_VIEW = (MobileBy.ID, "com.adorbee.app:id/video_view")
    LOADING_INDICATOR = (MobileBy.ID, "com.adorbee.app:id/loading_indicator")
    
    # 功能按钮栏
    SCREENSHOT_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_screenshot")
    TALK_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_talk")
    ALARM_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_alarm")
    RECORD_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_record")
    PLAYBACK_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_playback")
    MESSAGES_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_messages")
    
    # 底部快捷栏
    HOME_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_home")
    PRESET_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_preset")
    SETTINGS_SHORT_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_settings_short")
    SCHEDULE_BTN = (MobileBy.ID, "com.adorbee.app:id/iv_schedule")
    
    # 清晰度切换
    QUALITY_BTN = (MobileBy.ID, "com.adorbee.app:id/tv_quality")
    QUALITY_SD = (MobileBy.XPATH, "//android.widget.TextView[@text='SD']")
    QUALITY_HD = (MobileBy.XPATH, "//android.widget.TextView[@text='HD']")
    
    # ==================== 页面操作 ====================
    
    def click_back(self):
        """
        点击返回按钮
        """
        self.click(self.BACK_BTN)
    
    def take_screenshot(self):
        """
        点击截图按钮
        """
        self.click(self.SCREENSHOT_BTN)
    
    def start_talk(self):
        """
        开始对讲（长按）
        """
        element = self.find_element(self.TALK_BTN)
        # 长按操作
        from appium.webdriver.common.touch_action import TouchAction
        actions = TouchAction(self.driver)
        actions.long_press(element).wait(2000).release().perform()
    
    def trigger_alarm(self):
        """
        触发警报
        """
        self.click(self.ALARM_BTN)
    
    def start_recording(self):
        """
        开始录像
        """
        self.click(self.RECORD_BTN)
    
    def click_playback(self):
        """
        点击回放按钮
        """
        self.click(self.PLAYBACK_BTN)
    
    def click_messages(self):
        """
        点击消息按钮
        """
        self.click(self.MESSAGES_BTN)
    
    def switch_quality(self, quality='HD'):
        """
        切换清晰度
        
        Args:
            quality: 'SD' 或 'HD'
        """
        self.click(self.QUALITY_BTN)
        if quality.upper() == 'SD':
            self.click(self.QUALITY_SD)
        else:
            self.click(self.QUALITY_HD)
    
    def get_current_quality(self) -> str:
        """
        获取当前清晰度
        """
        return self.get_text(self.QUALITY_BTN)
    
    def is_video_loading(self) -> bool:
        """
        判断视频是否正在加载
        """
        return self.is_element_present(self.LOADING_INDicator, timeout=2)
    
    def swipe_video(self, direction='up'):
        """
        在视频区域滑动（云台控制）
        
        Args:
            direction: 'up', 'down', 'left', 'right'
        """
        size = self.get_window_size()
        center_x = size['width'] // 2
        center_y = size['height'] // 2
        
        if direction == 'up':
            self.swipe(center_x, center_y + 100, center_x, center_y - 100)
        elif direction == 'down':
            self.swipe(center_x, center_y - 100, center_x, center_y + 100)
        elif direction == 'left':
            self.swipe(center_x + 100, center_y, center_x - 100, center_y)
        elif direction == 'right':
            self.swipe(center_x - 100, center_y, center_x + 100, center_y)
