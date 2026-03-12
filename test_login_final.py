"""
Adorbee APP Login Test - Final Version
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from appium.webdriver.common.appiumby import AppiumBy


def close_system_dialog(driver):
    """关闭系统弹窗"""
    try:
        # 尝试点击确定/关闭按钮
        for btn_text in ['确定', '确认', 'OK', 'Close', '关闭']:
            try:
                btn = driver.find_element(AppiumBy.XPATH, f"//*[@text='{btn_text}']")
                btn.click()
                print(f"   Closed system dialog ({btn_text})")
                time.sleep(1)
                return True
            except:
                continue
    except:
        pass
    return False


def close_ad_popup(driver):
    """关闭广告弹窗"""
    try:
        close_btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='×']")
        close_btn.click()
        print("   [OK] Closed ad popup")
        time.sleep(1)
        return True
    except:
        pass
    return False


def is_ad_popup_present(driver):
    """检查广告弹窗"""
    try:
        driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='×']")
        return True
    except:
        pass
    return False


def test_login():
    """登录测试"""
    print("=" * 70)
    print("Adorbee APP Login Test")
    print("=" * 70)
    
    driver = None
    
    try:
        # Step 1: 清除数据并创建 WebDriver
        print("\n[Step 1] Setup...")
        print("   Clearing app data...")
        os.system("adb shell pm clear com.amv.adorbee >nul 2>&1")
        time.sleep(2)
        
        print("   Creating WebDriver...")
        driver = DriverFactory.get_driver()
        print(f"   [OK] Device: {driver.capabilities.get('deviceModel', 'Unknown')}")
        
        # 手动启动APP
        print("   Starting app...")
        driver.activate_app("com.amv.adorbee")
        time.sleep(3)
        
        login_page = LoginPage(driver)
        
        # Step 2: 等待进入登录页
        print("\n[Step 2] Waiting for login page...")
        max_wait = 20
        waited = 0
        while waited < max_wait:
            current = driver.current_activity
            print(f"   Current: {current}")
            
            # 处理系统弹窗
            if "AppErrorDialog" in current or "sm.iafd" in current:
                print("   System dialog detected, trying to close...")
                close_system_dialog(driver)
                time.sleep(2)
                waited += 2
                continue
            
            # 检查是否在登录页
            if ".login.LoginActivity" in current:
                print("   [OK] On login page")
                break
            
            time.sleep(2)
            waited += 2
        
        if ".login.LoginActivity" not in driver.current_activity:
            print("   [FAIL] Timeout waiting for login page")
            return False
        
        # Step 2b: 切换到中国区
        print("\n[Step 2b] Switch to China region...")
        try:
            country_btn = driver.find_element(AppiumBy.ID, "com.amv.adorbee:id/ll_country")
            country_btn.click()
            time.sleep(2)
            
            china_option = driver.find_element(AppiumBy.XPATH, "//*[@text='China' or @text='中国']")
            china_option.click()
            time.sleep(1)
            print("   [OK] Switched to China")
        except Exception as e:
            print(f"   [WARNING] Could not switch region: {e}")
        
        # Step 3: 执行登录
        print("\n[Step 3] Login...")
        username = "2y5qa@airsworld.net"
        password = "12345678"
        
        login_page.input_username(username)
        login_page.input_password(password)
        login_page.click_login_button()
        
        print("   Waiting for result...")
        time.sleep(8)  # 增加等待时间
        
        # Step 4: 验证登录结果
        print("\n[Step 4] Verify login...")
        
        # 等待页面跳转
        max_wait = 15
        waited = 0
        current = driver.current_activity
        while ".login.LoginActivity" in current and waited < max_wait:
            time.sleep(2)
            current = driver.current_activity
            waited += 2
            print(f"   Waiting... Current: {current}")
        
        print(f"   Activity: {current}")
        
        if ".main.MainActivity" in current or ".promotion." in current:
            print("   [OK] Login success")
        else:
            print("   [FAIL] Login failed")
            # 截图查看错误
            screenshot = login_page.take_screenshot("login_failed")
            print(f"   Screenshot saved: {screenshot}")
            return False
        
        # Step 5: 关闭广告弹窗
        print("\n[Step 5] Handle popup...")
        if is_ad_popup_present(driver):
            close_ad_popup(driver)
            print("   [OK] Popup closed")
        else:
            print("   No popup")
        
        # Step 6: 截图保存
        print("\n[Step 6] Save screenshot...")
        screenshot = login_page.take_screenshot("login_success")
        print(f"   [OK] Saved: {screenshot}")
        
        print("\n" + "=" * 70)
        print("TEST PASSED!")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("\n[Cleanup] Closing...")
            DriverFactory.quit_driver()
            print("   [OK] Done")


if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)
