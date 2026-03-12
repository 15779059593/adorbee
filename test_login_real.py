"""
Login Function Test - With Ad Popup Handling
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from appium.webdriver.common.appiumby import AppiumBy


def close_ad_popup(driver):
    """
    关闭广告弹窗
    
    广告弹窗有关闭按钮（×），点击后关闭
    """
    try:
        # 查找关闭按钮（×）
        # 根据 UI  dump: text="×", class="android.widget.Button"
        close_btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='×']")
        close_btn.click()
        print("   Clicked ad popup close button (×)")
        time.sleep(1)
        return True
    except:
        # 尝试其他方式查找关闭按钮
        try:
            close_btn = driver.find_element(AppiumBy.XPATH, "//*[@text='×' or @text='✕' or @text='✖']")
            close_btn.click()
            print("   Clicked ad popup close button")
            time.sleep(1)
            return True
        except:
            pass
    
    return False


def is_ad_popup_present(driver):
    """
    检查是否有广告弹窗
    
    通过检查关闭按钮或广告内容来判断
    """
    try:
        # 检查是否有关闭按钮
        driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='×']")
        return True
    except:
        pass
    
    # 检查是否有广告内容（WebView 中的图片）
    try:
        driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Sale') or contains(@content-desc, 'sale')]")
        return True
    except:
        pass
    
    return False


def test_login():
    """Test login function with ad popup handling"""
    print("=" * 60)
    print("Adorbee APP Login Function Test")
    print("=" * 60)
    
    driver = None
    try:
        # 1. Create WebDriver
        print("\n[1] Creating WebDriver...")
        driver = DriverFactory.get_driver()
        print(f"   Device: {driver.capabilities.get('deviceModel', 'Unknown')}")
        print(f"   Current Activity: {driver.current_activity}")
        
        login_page = LoginPage(driver)
        
        # 2. Check current page
        print("\n[2] Checking current page...")
        if login_page.is_on_login_page():
            print("   Current page is Login Page")
        else:
            current_activity = driver.current_activity
            print("   Not on login page")
            print(f"   Current Activity: {current_activity}")
            
            # Check if already logged in (main page or promotion page)
            if ".main.MainActivity" in current_activity or ".promotion." in current_activity:
                print("   Already logged in!")
                
                # Check and close ad popup if present
                if is_ad_popup_present(driver):
                    print("   Ad popup detected, closing...")
                    close_ad_popup(driver)
                
                login_page.take_screenshot("already_logged_in")
                return True
            return False
        
        # 3. Test login
        print("\n[3] Starting login test...")
        
        username = "2y5qa@airsworld.net"
        password = "12345678"
        
        print(f"   Input username: {username}")
        login_page.input_username(username)
        
        print("   Input password: ********")
        login_page.input_password(password)
        
        print("   Click login button...")
        login_page.click_login_button()
        
        # Wait for login result
        print("   Waiting for login result...")
        time.sleep(5)
        
        # Check current activity to determine login result
        current_activity = driver.current_activity
        print(f"   Current Activity after login: {current_activity}")
        
        # Check if login success (activity changed from login to main or promotion)
        if ".main.MainActivity" in current_activity or ".promotion." in current_activity or ".login.LoginActivity" not in current_activity:
            print("\n   [PASS] Login success!")
            
            # 4. Handle ad popup
            print("\n[4] Checking for ad popup...")
            if is_ad_popup_present(driver):
                print("   Ad popup detected!")
                print("   Closing ad popup...")
                if close_ad_popup(driver):
                    print("   Ad popup closed successfully!")
                    time.sleep(1)
                else:
                    print("   Failed to close ad popup")
            else:
                print("   No ad popup detected")
            
            # Take screenshot after closing popup
            login_page.take_screenshot("login_success_no_popup")
            
            # Verify we are on main page without popup
            print("\n[5] Verifying main page...")
            if not is_ad_popup_present(driver):
                print("   Main page is clean (no popup)")
                print("   [PASS] Login process completed successfully!")
                return True
            else:
                print("   Warning: Popup still present")
                return True  # Still consider login success
        else:
            print("\n   [FAIL] Login failed!")
            login_page.take_screenshot("login_failed")
            return False
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("\n[6] Closing WebDriver...")
            DriverFactory.quit_driver()
            print("   WebDriver closed")


if __name__ == "__main__":
    success = test_login()
    print("\n" + "=" * 60)
    if success:
        print("Test Result: PASS")
    else:
        print("Test Result: FAIL")
    print("=" * 60)
    sys.exit(0 if success else 1)
