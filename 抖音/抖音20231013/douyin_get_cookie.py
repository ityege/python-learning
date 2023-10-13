# 通过cookie保存用户登录状态,没有这个必要,可以直接通过指定数据目录保存浏览器状态
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json


# 设置 ChromeDriver 路径

# 登录成功后获取和保存本地存储数据
def get_login_data():
    service = Service('C:/devtools/chrome/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    # 执行登录操作
    # ...
    driver.get("https://www.douyin.com")

    # 获取当前浏览器会话的 cookie 数据
    cookies = driver.get_cookies()
    # 关闭浏览器
    driver.quit()

    # 保存本地存储数据到文件或数据库中
    save_data(cookies, "login_data.txt")


# 启动浏览器并设置本地存储数据
def start_browser_with_data(data):
    driver = webdriver.Chrome()
    # 加载保存的 cookie 数据
    # cookies=dict(data)
    cookies=data
    driver.get("https://www.douyin.com")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    # 加载保存的会话数据



# 保存数据到文件
def save_data(data, filename):
    print("save_data", data, type(data), filename, type(filename))
    # 将 JSON 数据写入文件
    with open(filename, "w") as file:
        json.dump(data, file)


# 从保存的文件中加载数据
def load_data(filename):
    print("load_data", filename, type(filename))
    # 从文件中读取 JSON 数据
    with open(filename, "r") as file:
        data = json.load(file)
        print(data)
    return data

    # 从文件或数据库中读取保存的数据
    # ...


# 示例用法
get_login_data()

# 在重新启动浏览器时读取并设置本地存储数据
data = load_data("login_data.txt")
start_browser_with_data(data)

