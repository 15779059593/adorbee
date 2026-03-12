"""
Login Function Test - Using Real Account (Fixed)
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from appium.webdriver.common.appiumby import AppiumBy


def test_login():
    """Test login function"""
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
            print("   Not on login page")
            print(f"   Current Activity: {driver.current_activity}")
            
            # Check if already logged in (main page)
            if ".main.MainActivity" in driver.current_activity:
                print("   Already logged in!")
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
        
        # Check if login success (activity changed from login to main)
        if ".main.MainActivity" in current_activity or ".login.LoginActivity" not in current_activity:
            print("\n   [PASS] Login success!")
            
            # Try to close any popup
            try:
                # Try to find and click close button on popup
                close_btn = driver.find_element(AppiumBy.XPATH, "//*[@text='✕' or @text='×' or @text='Close']")
                close_btn.click()
                print("   Closed popup")
                time.sleep(1)
            except:
                pass
            
            login_page.take_screenshot("login_success")
            return True
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
            print("\n[4] Closing WebDriver...")
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
