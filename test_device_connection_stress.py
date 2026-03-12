"""
摄像机连接功能压力测试
流程：蓝牙搜索 -> 点击设备 -> WiFi配网 -> 检查WiFi列表
异常判定：WiFi配网页面15秒内未出现WiFi列表
"""
import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from appium.webdriver.common.appiumby import AppiumBy


class DeviceConnectionTest:
    """设备连接测试类"""
    
    def __init__(self):
        self.driver = None
        self.login_page = None
        self.test_results = []
        
    def setup(self):
        """初始化WebDriver"""
        print("\n[Setup] Creating WebDriver...")
        self.driver = DriverFactory.get_driver()
        self.login_page = LoginPage(self.driver)
        print(f"   [OK] Device: {self.driver.capabilities.get('deviceModel', 'Unknown')}")
        return True
        
    def teardown(self):
        """清理资源"""
        if self.driver:
            print("\n[Teardown] Closing WebDriver...")
            DriverFactory.quit_driver()
            print("   [OK] Done")
    
    def wait_for_device(self, timeout=120):
        """
        等待设备出现
        
        Args:
            timeout: 最大等待时间（秒），默认2分钟
            
        Returns:
            device_element: 设备元素，如果超时返回None
        """
        print(f"\n[Step 1] Waiting for device to appear (max {timeout}s)...")
        start_time = time.time()
        check_interval = 3  # 每3秒检查一次
        
        while time.time() - start_time < timeout:
            try:
                # 查找设备元素（根据截图中的设备信息）
                # 设备通常包含SN号或MAC地址
                device = self.driver.find_element(
                    AppiumBy.XPATH, 
                    "//*[contains(@text, 'SN:') or contains(@text, 'ay_ipc') or contains(@resource-id, 'device')]"
                )
                elapsed = time.time() - start_time
                print(f"   [OK] Device found after {elapsed:.1f}s")
                return device
            except:
                # 未找到设备，继续等待
                time.sleep(check_interval)
                print(f"   Searching... ({int(time.time() - start_time)}s)")
        
        print(f"   [FAIL] Device not found within {timeout}s")
        return None
    
    def click_device(self, device):
        """点击设备进行连接"""
        print("\n[Step 2] Clicking device...")
        try:
            device.click()
            print("   [OK] Device clicked")
            time.sleep(3)  # 等待页面跳转
            return True
        except Exception as e:
            print(f"   [FAIL] Failed to click device: {e}")
            return False
    
    def wait_for_wifi_list(self, timeout=20, fail_threshold=15):
        """
        等待WiFi列表出现
        
        Args:
            timeout: 最大等待时间（秒），默认20秒
            fail_threshold: 异常判定时间（秒），默认15秒
            
        Returns:
            (success, is_abnormal): 
                success - 是否找到WiFi列表
                is_abnormal - 是否超过异常阈值
        """
        print(f"\n[Step 3] Waiting for WiFi list (max {timeout}s, abnormal if >{fail_threshold}s)...")
        start_time = time.time()
        check_interval = 1  # 每秒检查一次
        
        while time.time() - start_time < timeout:
            elapsed = time.time() - start_time
            
            try:
                # 查找WiFi列表元素
                # 根据截图，WiFi列表包含WiFi名称选项
                wifi_list = self.driver.find_element(
                    AppiumBy.XPATH,
                    "//*[@text='Wi-Fi Name (SSID)' or contains(@text, 'ayivision') or contains(@text, '2.4G')]"
                )
                print(f"   [OK] WiFi list appeared after {elapsed:.1f}s")
                return True, False
            except:
                # 检查是否超过异常阈值
                if elapsed > fail_threshold:
                    print(f"   [ABNORMAL] WiFi list not appeared after {elapsed:.1f}s (threshold: {fail_threshold}s)")
                    # 截图保存异常状态
                    screenshot = self.login_page.take_screenshot(f"abnormal_wifi_{datetime.now().strftime('%H%M%S')}")
                    print(f"   [OK] Screenshot saved: {screenshot}")
                    return False, True
                
                time.sleep(check_interval)
                if int(elapsed) % 5 == 0:  # 每5秒打印一次
                    print(f"   Waiting... ({elapsed:.1f}s)")
        
        print(f"   [FAIL] WiFi list not found within {timeout}s")
        return False, False
    
    def run_single_test(self, test_num):
        """运行单次测试"""
        print(f"\n{'='*70}")
        print(f"Test #{test_num} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        result = {
            'test_num': test_num,
            'start_time': datetime.now(),
            'device_found': False,
            'device_found_time': None,
            'wifi_list_found': False,
            'wifi_list_time': None,
            'is_abnormal': False,
            'status': 'FAIL'
        }
        
        try:
            # Step 1: 等待设备出现
            device = self.wait_for_device(timeout=120)
            if not device:
                print("   [FAIL] No device found")
                result['status'] = 'NO_DEVICE'
                return result
            
            result['device_found'] = True
            result['device_found_time'] = time.time()
            
            # Step 2: 点击设备
            if not self.click_device(device):
                result['status'] = 'CLICK_FAIL'
                return result
            
            # Step 3: 等待WiFi列表
            wifi_found, is_abnormal = self.wait_for_wifi_list(timeout=20, fail_threshold=15)
            result['wifi_list_found'] = wifi_found
            result['wifi_list_time'] = time.time()
            result['is_abnormal'] = is_abnormal
            
            if is_abnormal:
                result['status'] = 'ABNORMAL'
                print("\n   [ABNORMAL] Test stopped, page kept for recording")
                # 保持页面不变，返回结果
                return result
            elif wifi_found:
                result['status'] = 'PASS'
                print("\n   [PASS] WiFi list found successfully")
                # 点击返回按钮，回到蓝牙搜索页
                print("\n[Step 4] Clicking back button to return to Bluetooth search page...")
                try:
                    back_btn = self.driver.find_element(AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Navigate up'] | //*[@content-desc='Navigate up'] | //android.widget.ImageButton")
                    back_btn.click()
                    print("   [OK] Back button clicked")
                    time.sleep(2)
                    
                    # 验证是否回到蓝牙搜索页
                    current = self.driver.current_activity
                    print(f"   Current Activity: {current}")
                    if 'AddDevice' in current or 'Bluetooth' in current or 'bind' in current.lower():
                        print("   [OK] Returned to Bluetooth search page")
                    else:
                        print(f"   [INFO] Current page: {current}")
                except Exception as e:
                    print(f"   [WARNING] Failed to click back: {e}")
                    # 尝试使用系统返回键
                    self.driver.press_keycode(4)
                    print("   [OK] Used system back key")
                    time.sleep(2)
            else:
                result['status'] = 'TIMEOUT'
                print("\n   [FAIL] WiFi list timeout")
            
            return result
            
        except Exception as e:
            print(f"\n[ERROR] Test #{test_num} failed: {e}")
            result['status'] = 'ERROR'
            return result
    
    def print_summary(self):
        """打印测试摘要"""
        print(f"\n{'='*70}")
        print("Test Summary")
        print(f"{'='*70}")
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        abnormal = sum(1 for r in self.test_results if r['status'] == 'ABNORMAL')
        failed = total - passed - abnormal
        
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Abnormal: {abnormal}")
        print(f"Failed: {failed}")
        print(f"Success rate: {passed/total*100:.1f}%" if total > 0 else "N/A")
        
        if abnormal > 0:
            print("\nAbnormal cases (WiFi list >15s):")
            for r in self.test_results:
                if r['is_abnormal']:
                    print(f"  Test #{r['test_num']}: {r['start_time'].strftime('%H:%M:%S')}")


def run_stress_test(iterations=10):
    """运行压力测试"""
    print("="*70)
    print("Device Connection Stress Test")
    print("="*70)
    print(f"Iterations: {iterations}")
    print("Timeout: Device search 120s, WiFi list 20s")
    print("Abnormal threshold: WiFi list >15s")
    print("="*70)
    
    test = DeviceConnectionTest()
    
    try:
        # 初始化
        if not test.setup():
            print("[FAIL] Setup failed")
            return
        
        # 运行多次测试
        for i in range(1, iterations + 1):
            result = test.run_single_test(i)
            test.test_results.append(result)
            
            # 如果遇到异常情况，停止测试并保持页面
            if result['is_abnormal']:
                print(f"\n{'='*70}")
                print(f"ABNORMAL detected at Test #{i}, stopping stress test")
                print(f"{'='*70}")
                break
            
            # 测试间隔
            if i < iterations:
                print(f"\nWaiting 5s before next test...")
                time.sleep(5)
        
        # 打印摘要
        test.print_summary()
        
    finally:
        # 如果有异常情况，询问是否关闭WebDriver
        has_abnormal = any(r['is_abnormal'] for r in test.test_results)
        if has_abnormal:
            print("\n[NOTE] Abnormal case detected, keeping page for recording")
            print("       Please manually check the device and press Enter to close...")
            try:
                input()
            except:
                pass
        
        test.teardown()


if __name__ == "__main__":
    # 默认运行10次压力测试
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    run_stress_test(iterations)
