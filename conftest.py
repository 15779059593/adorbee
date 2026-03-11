# Pytest 配置文件

import pytest
import os
import sys

# 添加项目根目录到路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


def pytest_configure(config):
    """
    Pytest 配置
    """
    # 创建报告目录
    report_dir = os.path.join(BASE_DIR, 'reports')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # 创建日志目录
    log_dir = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def pytest_collection_modifyitems(config, items):
    """
    修改测试项
    """
    # 自动添加标记
    for item in items:
        # 根据测试类名自动添加标记
        if "device" in item.nodeid.lower():
            item.add_marker(pytest.mark.device)
        if "live" in item.nodeid.lower():
            item.add_marker(pytest.mark.live)


@pytest.fixture(scope="session")
def driver():
    """
    全局 WebDriver fixture
    
    在整个测试会话期间共享同一个 WebDriver
    """
    from utils.driver_factory import DriverFactory
    
    driver = DriverFactory.get_driver()
    yield driver
    DriverFactory.quit_driver()


@pytest.fixture(scope="function")
def fresh_driver():
    """
    每个测试函数创建新的 WebDriver
    
    用于需要干净环境的测试
    """
    from utils.driver_factory import DriverFactory
    
    driver = DriverFactory.restart_driver()
    yield driver
    DriverFactory.quit_driver()
