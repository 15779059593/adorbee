# Adorbee APP 自动化测试框架

基于 Python + Appium 的移动端自动化测试框架

## 项目结构

```
adorbee/
├── config/                 # 配置文件
│   ├── config.py          # 全局配置
│   └── capabilities.py    # Appium 设备配置
├── common/                # 公共模块
│   ├── base_page.py       # 页面基类
│   ├── base_test.py       # 测试用例基类
│   └── logger.py          # 日志工具
├── pages/                 # 页面对象
│   ├── login_page.py      # 登录页
│   ├── device_page.py     # 设备列表页
│   ├── live_page.py       # 直播页
│   ├── settings_page.py   # 设置页
│   └── ...
├── testcases/             # 测试用例
│   ├── test_login.py      # 登录测试
│   ├── test_device.py     # 设备管理测试
│   ├── test_live.py       # 直播功能测试
│   └── ...
├── utils/                 # 工具类
│   ├── driver_factory.py  # 驱动工厂
│   ├── element_helper.py  # 元素操作辅助
│   └── data_helper.py     # 数据处理
├── data/                  # 测试数据
│   ├── test_data.json     # 测试数据
│   └── accounts.yaml      # 账号信息
├── reports/               # 测试报告
├── logs/                  # 日志文件
├── conftest.py           # Pytest 配置
├── pytest.ini            # Pytest 配置
├── requirements.txt      # 依赖包
└── README.md             # 项目说明
```

## 环境要求

- Python 3.8+
- Appium Server
- Android SDK / Xcode (iOS)
- 真机或模拟器

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行指定模块
pytest testcases/test_login.py

# 生成报告
pytest --html=reports/report.html
```

## 配置说明

1. 修改 `config/config.py` 中的设备信息
2. 在 `data/accounts.yaml` 中配置测试账号
3. 根据实际设备修改 `config/capabilities.py`

## 页面对象模式

每个页面对象继承自 `BasePage`，封装页面元素和操作方法：

```python
class LoginPage(BasePage):
    def input_username(self, username):
        self.send_keys(self.username_input, username)
    
    def click_login(self):
        self.click(self.login_button)
```

## 测试用例编写

```python
class TestLogin(BaseTest):
    def test_login_success(self):
        login_page = LoginPage(self.driver)
        login_page.login("username", "password")
        assert login_page.is_logged_in()
```
