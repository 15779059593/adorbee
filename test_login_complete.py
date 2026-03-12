"""
Adorbee APP Login Test - Complete Version
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from appium.webdriver.common.appiumby import AppiumBy


def close_ad_popup(driver):
    """Close ad popup by clicking X button"""
    try:
        close_btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='×']")
        close_btn.click()
        print("   [OK] Clicked ad popup close button (X)")
        time.sleep(1)
        return True
    except:
        try:
            close_btn = driver.find_element(AppiumBy.XPATH, "//*[@text='×' or @text='X']")
            close_btn.click()
            print("   [OK] Clicked ad popup close button")
            time.sleep(1)
            return True
        except:
            pass
    return False


def is_ad_popup_present(driver):
    """Check if ad popup is present"""
    try:
        driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='×']")
        return True
    except:
        pass
    
    try:
        driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Sale')]")
        return True
    except:
        pass
    
    return False


def logout_if_needed(driver, login_page):
    """Logout if already logged in"""
    try:
        current_activity = driver.current_activity
        if ".main.MainActivity" in current_activity or ".promotion." in current_activity:
            print("   Already logged in, restarting app...")
            
            if is_ad_popup_present(driver):
                close_ad_popup(driver)
            
            # 使用 terminate_app 和 activate_app 替代 reset
            driver.terminate_app("com.amv.adorbee")
            time.sleep(2)
            driver.activate_app("com.amv.adorbee")
            print("   [OK] App restarted, back to login page")
            time.sleep(5)
            return True
    except Exception as e:
        print(f"   Warning: logout failed: {e}")
    return False


def test_login_flow():
    """Complete login test flow"""
    print("=" * 70)
    print("Adorbee APP Login Automation Test")
    print("=" * 70)
    
    driver = None
    login_page = None
    
    try:
        # Step 1: Create WebDriver with clear data
        print("\n[Step 1] Creating WebDriver (with clear data)...")
        
        # 先清除APP数据
        print("   Clearing app data...")
        os.system("adb shell pm clear com.amv.adorbee")
        time.sleep(2)
        
        driver = DriverFactory.get_driver()
        print(f"   [OK] Device: {driver.capabilities.get('deviceModel', 'Unknown')}")
        print(f"   [OK] Activity: {driver.current_activity}")
        
        login_page = LoginPage(driver)
        
        # Step 2: Check current page
        print("\n[Step 2] Checking current page...")
        time.sleep(3)  # 等待APP启动
        current_activity = driver.current_activity
        print(f"   Current Activity: {current_activity}")
        
        # 等待进入登录页面
        max_wait = 15
        waited = 0
        while ".login.LoginActivity" not in current_activity and waited < max_wait:
            time.sleep(2)
            current_activity = driver.current_activity
            waited += 2
            print(f"   Waiting... Current: {current_activity}")
        
        if ".login.LoginActivity" in current_activity:
            print("   [OK] On login page")
        elif ".activities.LauncherActivity" in current_activity:
            # 启动页，等待跳转
            print("   On launcher, waiting for login page...")
            time.sleep(5)
            current_activity = driver.current_activity
            if ".login.LoginActivity" in current_activity:
                print("   [OK] On login page")
            else:
                print(f"   [WARNING] Current activity: {current_activity}")
                if login_page.is_on_login_page():
                    print("   [OK] Login page elements found")
                else:
                    print("   [FAIL] Not on login page")
                    return False
        else:
            print(f"   [WARNING] Current activity: {current_activity}")
            if login_page.is_on_login_page():
                print("   [OK] Login page elements found")
            else:
                print("   [FAIL] Not on login page")
                return False
        
        if not login_page.is_on_login_page():
            # 再次检查Activity
            current_activity = driver.current_activity
            if ".login.LoginActivity" not in current_activity:
                print("   [FAIL] Not on login page after check")
                print(f"   Current activity: {current_activity}")
                return False
            else:
                print("   [OK] On login page (by activity)")
        
        print("   [OK] Ready to login")
        
        # Step 3: Perform login
        print("\n[Step 3] Performing login...")
        username = "2y5qa@airsworld.net"
        password = "12345678"
        
        print(f"   Input username: {username}")
        login_page.input_username(username)
        
        print("   Input password: ********")
        login_page.input_password(password)
        
        print("   Click login button...")
        login_page.click_login_button()
        
        print("   Waiting for login result...")
        time.sleep(5)
        
        # Step 4: Verify login result
        print("\n[Step 4] Verifying login result...")
        current_activity = driver.current_activity
        print(f"   Activity after login: {current_activity}")
        
        if ".main.MainActivity" in current_activity or ".promotion." in current_activity:
            print("   [OK] Login successful!")
        else:
            print("   [FAIL] Login failed - still on login page")
            login_page.take_screenshot("login_failed")
            return False
        
        # Step 5: Handle ad popup
        print("\n[Step 5] Handling ad popup...")
        if is_ad_popup_present(driver):
            print("   Ad popup detected")
            if close_ad_popup(driver):
                print("   [OK] Ad popup closed")
            else:
                print("   [FAIL] Failed to close ad popup")
        else:
            print("   No ad popup detected")
        
        # Step 6: Verify main page
        print("\n[Step 6] Verifying main page...")
        time.sleep(2)
        
        if is_ad_popup_present(driver):
            print("   Warning: Popup still present")
        else:
            print("   [OK] Main page is clean")
        
        screenshot = login_page.take_screenshot("login_success_final")
        print(f"   [OK] Screenshot saved: {screenshot}")
        
        try:
            driver.find_element(AppiumBy.XPATH, "//*[@text='Devices' or @text='设备']")
            print("   [OK] Main page elements found")
        except:
            print("   Note: Main page elements check skipped")
        
        print("\n" + "=" * 70)
        print("TEST PASSED - Login flow completed successfully!")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        
        if login_page:
            try:
                login_page.take_screenshot("test_error")
            except:
                pass
        return False
        
    finally:
        if driver:
            print("\n[Cleanup] Closing WebDriver...")
            DriverFactory.quit_driver()
            print("   [OK] WebDriver closed")


if __name__ == "__main__":
    success = test_login_flow()
    sys.exit(0 if success else 1)
