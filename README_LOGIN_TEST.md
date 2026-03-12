# Adorbee APP 登录功能自动化测试

## 测试框架结构

```
D:\Test\adorbee
├── common/                 # 公共模块
│   ├── base_page.py       # 页面基类
│   ├── base_test.py       # 测试基类
│   └── logger.py          # 日志工具
├── config/                # 配置模块
│   ├── config.py          # 全局配置
│   └── capabilities.py    # Appium 配置
├── data/                  # 测试数据
│   ├── accounts.yaml      # 测试账号配置
│   └── test_config.yaml   # 测试配置
├── pages/                 # 页面对象
│   ├── login_page.py      # 登录页面
│   └── device_page.py     # 设备列表页
├── testcases/             # 测试用例
│   └── test_login.py      # 登录测试用例
├── reports/               # 测试报告
│   ├── allure-results/    # Allure 结果
│   └── screenshots/       # 截图
├── logs/                  # 日志文件
├── conftest.py            # Pytest 配置
└── run_login_test.py      # 测试执行脚本
```

## 环境要求

1. **Python 3.8+**
2. **Appium Server**
3. **Android 设备或模拟器**（已连接并开启USB调试）
4. **Adorbee APP**（已安装）

## 安装依赖

```bash
cd D:\Test\adorbee
pip install -r requirements.txt
```

依赖包括：
- appium-python-client
- pytest
- pytest-allure
- pyyaml
- selenium

## 配置测试账号

编辑 `data/accounts.yaml` 文件，添加真实测试账号：

```yaml
test_accounts:
  - name: "测试账号1"
    username: "your_real_email@example.com"  # 替换为真实账号
    password: "your_real_password"            # 替换为真实密码
    region: "CN"
```

⚠️ **注意**: 此文件包含敏感信息，请勿提交到Git仓库！

## 启动测试

### 方式1：使用Python脚本（推荐）

```bash
cd D:\Test\adorbee
python run_login_test.py
```

然后按菜单选择要运行的测试。

### 方式2：使用批处理脚本

```bash
cd D:\Test\adorbee
run_login_tests.bat
```

### 方式3：直接使用pytest

```bash
# 运行所有登录测试
pytest testcases/test_login.py -v

# 运行冒烟测试
pytest testcases/test_login.py -v -m smoke

# 运行安全测试
pytest testcases/test_login.py::TestLoginSecurity -v

# 生成Allure报告
pytest testcases/test_login.py -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 测试用例说明

### 1. 正常登录测试 (TestNormalLogin)
- `test_login_with_valid_credentials`: 使用有效账号密码登录
- `test_login_shows_device_list`: 验证登录后显示设备列表

### 2. 异常登录测试 (TestAbnormalLogin)
- `test_login_with_wrong_password`: 错误密码登录
- `test_login_with_nonexistent_user`: 不存在账号登录
- `test_login_with_empty_username`: 空账号登录
- `test_login_with_empty_password`: 空密码登录

### 3. 安全测试 (TestLoginSecurity)
- `test_sql_injection_attempt`: SQL注入攻击测试
- `test_xss_attempt`: XSS攻击测试

### 4. UI交互测试 (TestLoginUI)
- `test_password_visibility_toggle`: 密码显示/隐藏切换
- `test_forgot_password_link`: 忘记密码链接
- `test_register_link`: 注册链接

### 5. 隐私政策测试 (TestPrivacyPolicy)
- `test_privacy_popup_on_first_launch`: 首次启动隐私弹窗

## 查看测试报告

### 实时报告
```bash
allure serve reports/allure-results
```

### 生成静态报告
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

然后打开 `reports/allure-report/index.html`

## 常见问题

### 1. Appium Server 未启动
```bash
# 启动 Appium Server
appium
```

### 2. 设备未连接
```bash
# 检查设备连接
adb devices

# 如果列表为空，检查：
# 1. USB调试是否开启
# 2. 驱动是否正确安装
# 3. 数据线是否正常
```

### 3. 元素定位失败
- 检查APP版本是否匹配
- 使用 Appium Inspector 重新获取元素定位
- 修改 `pages/login_page.py` 中的元素定位器

### 4. 测试账号问题
- 确保 `data/accounts.yaml` 中的账号密码正确
- 确保账号可以正常登录APP

## 扩展测试

如需添加更多测试用例，编辑 `testcases/test_login.py`：

```python
@allure.feature("登录模块")
@allure.story("你的测试场景")
class TestYourFeature:
    
    @allure.title("你的测试用例")
    def test_your_case(self, driver):
        login_page = LoginPage(driver)
        # 你的测试代码
```

## 维护说明

1. **元素定位器更新**: 当APP UI变化时，更新 `pages/login_page.py` 中的定位器
2. **测试数据更新**: 在 `data/accounts.yaml` 中添加/修改测试账号
3. **新增测试**: 在 `testcases/test_login.py` 中添加新的测试类和方法

## 联系支持

如有问题，请联系测试团队。
