"""
快速连接测试 - 验证 Appium 环境
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage


def test_connection():
    """测试 Appium 连接"""
    print("=" * 50)
    print("Appium Connection Test")
    print("=" * 50)
    
    try:
        print("\n[1] Creating WebDriver...")
        driver = DriverFactory.get_driver()
        print("   OK WebDriver created")
        print(f"   - Device: {driver.capabilities.get('deviceName', 'Unknown')}")
        print(f"   - Platform: {driver.capabilities.get('platformName', 'Unknown')}")
        print(f"   - Current Package: {driver.current_package}")
        print(f"   - Current Activity: {driver.current_activity}")
        
        print("\n[2] Creating LoginPage object...")
        login_page = LoginPage(driver)
        print("   OK LoginPage created")
        
        print("\n[3] Checking current page...")
        if login_page.is_on_login_page():
            print("   OK Current page is Login Page")
            
            # Get current country/region
            country = login_page.get_selected_country()
            print(f"   - Selected Country/Region: {country}")
            
            # Take screenshot
            screenshot = login_page.take_screenshot("connection_test")
            print(f"   - Screenshot saved: {screenshot}")
        else:
            print("   ! Not on login page")
            print(f"   - Current Activity: {driver.current_activity}")
        
        print("\n[4] Closing WebDriver...")
        DriverFactory.quit_driver()
        print("   OK WebDriver closed")
        
        print("\n" + "=" * 50)
        print("Connection test PASSED!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
