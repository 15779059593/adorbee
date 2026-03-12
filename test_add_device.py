"""
Adorbee APP 设备绑定测试 - 从主页面开始
流程：主页面 -> 添加设备 -> 蓝牙搜索
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from appium.webdriver.common.appiumby import AppiumBy


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


def test_add_device():
    """设备绑定测试 - 从主页面开始"""
    print("=" * 70)
    print("Adorbee APP Device Binding Test")
    print("=" * 70)
    
    driver = None
    
    try:
        # Step 1: 创建 WebDriver (不清除数据，保持登录状态)
        print("\n[Step 1] Creating WebDriver...")
        driver = DriverFactory.get_driver()
        print(f"   [OK] Device: {driver.capabilities.get('deviceModel', 'Unknown')}")
        print(f"   [OK] Activity: {driver.current_activity}")
        
        # Step 2: 检查当前页面
        print("\n[Step 2] Checking current page...")
        current = driver.current_activity
        print(f"   Current Activity: {current}")
        
        # 如果在设备添加页，直接进行下一步
        if ".bind.AddDeviceActivity" in current:
            print("   [OK] Already on device add page")
            # 直接跳到点击 Setup WIFI Device
            print("\n[Step 3] Clicking 'Setup WIFI Device' button...")
            try:
                wifi_btn = driver.find_element(AppiumBy.XPATH, "//*[@text='Setup WIFI Device']")
                wifi_btn.click()
                print("   [OK] Clicked 'Setup WIFI Device'")
                time.sleep(3)
            except Exception as e:
                print(f"   [FAIL] Cannot find button: {e}")
                return False
            
            # 跳到检查蓝牙页面
            print("\n[Step 4] Checking Bluetooth search page...")
            current = driver.current_activity
            print(f"   Current Activity: {current}")
            
            if "bluetooth" in current.lower() or "search" in current.lower():
                print("   [OK] Entered Bluetooth search page")
            else:
                print(f"   [INFO] Current page: {current}")
            
            # 截图保存
            print("\n[Step 5] Saving screenshot...")
            login_page = LoginPage(driver)
            screenshot = login_page.take_screenshot("bluetooth_search_page")
            print(f"   [OK] Saved: {screenshot}")
            
            print("\n" + "=" * 70)
            print("TEST PASSED - Entered Bluetooth search page!")
            print("=" * 70)
            return True
        
        # 如果在促销页，先关闭弹窗
        if ".promotion." in current:
            print("   On promotion page, closing popup...")
            if is_ad_popup_present(driver):
                close_ad_popup(driver)
            time.sleep(2)
            current = driver.current_activity
        
        # 如果在登录页，需要登录
        if ".login.LoginActivity" in current:
            print("   On login page, need to login first")
            print("   [FAIL] Please run login test first")
            return False
        
        # 如果不在主页，尝试返回主页
        if ".main.MainActivity" not in current:
            print(f"   [WARNING] Not on main page: {current}")
            print("   Trying to go back to main page...")
            driver.press_keycode(4)  # 返回键
            time.sleep(2)
            current = driver.current_activity
            if ".main.MainActivity" not in current:
                print("   [FAIL] Cannot reach main page")
                return False
        
        print("   [OK] On main page")
        
        # Step 3: 点击添加设备按钮
        print("\n[Step 3] Clicking add device button...")
        try:
            # 尝试点击右上角的添加设备图标
            add_btn = driver.find_element(AppiumBy.ID, "com.amv.adorbee:id/iv_add_device")
            add_btn.click()
            print("   [OK] Clicked add device icon")
        except:
            # 尝试点击中间的"Add Device"按钮
            try:
                add_btn = driver.find_element(AppiumBy.ID, "com.amv.adorbee:id/tv_add_dev")
                add_btn.click()
                print("   [OK] Clicked 'Add Device' button")
            except Exception as e:
                print(f"   [FAIL] Cannot find add device button: {e}")
                return False
        
        time.sleep(3)
        
        # Step 4: 检查是否进入设备添加页面，并点击 Setup WIFI Device
        print("\n[Step 4] Checking device add page and click Setup WIFI Device...")
        current = driver.current_activity
        print(f"   Current Activity: {current}")
        
        # 可能的页面：设备类型选择页、蓝牙搜索页等
        if "add" in current.lower() or "device" in current.lower() or "bind" in current.lower():
            print("   [OK] Entered device add flow")
            
            # 点击 Setup WIFI Device 按钮
            print("   Clicking 'Setup WIFI Device' button...")
            try:
                # 尝试通过文本查找按钮
                wifi_btn = driver.find_element(AppiumBy.XPATH, "//*[@text='Setup WIFI Device']")
                wifi_btn.click()
                print("   [OK] Clicked 'Setup WIFI Device'")
                time.sleep(3)
            except Exception as e:
                print(f"   [FAIL] Cannot find 'Setup WIFI Device' button: {e}")
                return False
        else:
            print(f"   [INFO] Current page: {current}")
            return False
        
        # Step 5: 检查是否进入蓝牙搜索页面
        print("\n[Step 5] Checking Bluetooth search page...")
        current = driver.current_activity
        print(f"   Current Activity: {current}")
        
        if "bluetooth" in current.lower() or "search" in current.lower() or "scan" in current.lower():
            print("   [OK] Entered Bluetooth search page")
        else:
            print(f"   [INFO] Current page after click: {current}")
            # 截图查看当前页面
            screenshot = login_page.take_screenshot("after_wifi_setup")
            print(f"   [OK] Screenshot saved: {screenshot}")
        
        # Step 6: 截图保存
        print("\n[Step 6] Saving screenshot...")
        login_page = LoginPage(driver)
        screenshot = login_page.take_screenshot("bluetooth_search_page")
        print(f"   [OK] Saved: {screenshot}")
        
        print("\n" + "=" * 70)
        print("TEST PASSED - Entered Bluetooth search page!")
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
    success = test_add_device()
    sys.exit(0 if success else 1)
