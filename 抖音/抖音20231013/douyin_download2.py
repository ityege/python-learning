# 通过元素获取有一点问题,新的通过请求
import random
import time
import uuid
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
import hashlib

distinct = set();

# 指定驱动
service = Service('C:/devtools/chrome/chromedriver.exe')

# 创建 ChromeOptions 对象
chrome_options = Options()
# 指定数据目录
chrome_options.add_argument("--user-data-dir=D:/code/pythontest/data")
# 创建 WebDriver 对象并指定选项
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打开抖音，博主主页
driver.get("https://www.douyin.com/user/userid")

# 显式等待，等待10秒，直到元素可见
wait = WebDriverWait(driver, 20)
element = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "/html/body/div[2]/div[1]/div[3]/div[2]/div/div/div[3]/div[1]/div[2]/div/div[1]/div[1]/h2/span[2]")))

# 获取到作者有多少个视频
video_num = element.text
print("视频数量: ", video_num)

first_video = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                           '/html/body/div[2]/div[1]/div[3]/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/ul/li[1]/div/a/div/div[1]/img')))
# 打开第一个视频
first_video.click()
a = 0
for _ in range(int(video_num) - 1):
    # 模仿人,视频不能刷太快
    time.sleep(random.randint(8, 10))
    print(a, video_num)
    a += 1
    # 切换下一个视频
    actions = ActionChains(driver)
    actions.send_keys(Keys.DOWN)
    actions.perform()
a = 0
# 获取所有请求
for request in driver.requests:
    # 下面是处理视频
    if request.response == None:
        continue
    if request.response.headers['Content-Type'] == "video/mp4":
        # 下载视频
        response = requests.get(request.url)
        md5_hash = hashlib.md5(response.content).hexdigest()
        if md5_hash in distinct:
            pass
        else:
            distinct.add(md5_hash)
            # 保存视频 保存为flv再转码成mp4,不让导入pr音频有问题
            filename = "sp1/" + str(uuid.uuid4()) + ".flv"  # 保存的文件名
            with open(filename, "wb") as file:
                print(a, len(driver.requests), filename, request.url)
                file.write(response.content)

            a += 1

# 退出浏览器
driver.quit()
