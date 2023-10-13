# 抖音视频下载,一开始要下载图片的,越处理越乱就不处理了,就只爬视频,随让爬取视频会重复就这么凑活用了。
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


import time
import random
import requests

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
wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "/html/body/div[2]/div[1]/div[3]/div[3]/div/div/div[3]/div[1]/div[2]/div/div[1]/div[1]/h2/span[2]")))

# 获取到作者有多少个视频
video_num = element.text
print("视频数量: ", video_num)

first_video = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                           '//*[@id="douyin-right-container"]/div[3]/div/div/div[3]/div[2]/div[2]/div[2]/ul/li[1]/div/a/div/div[1]/img')))
# 打开第一个视频
first_video.click()
a = 0
for _ in range(int(video_num)):
    # 模仿人,视频不能刷太快
    time.sleep(random.randint(3, 5))
    # 获取视频url
    try:

        source = driver.find_element(By.TAG_NAME, "source")
        url = source.get_property("src")
        print(a, url)
        a += 1
        # 下载视频
        response = requests.get(url)

        # 保存视频
        filename = "sp/" + str(int(time.time())) + ".flv"  # 保存的文件名
        with open(filename, "wb") as file:
            file.write(response.content)
    except NoSuchElementException:
        print(NoSuchElementException)

    except IndexError:
        print(IndexError)

    # 切换下一个视频
    actions = ActionChains(driver)
    actions.send_keys(Keys.DOWN)
    actions.perform()
# 退出浏览器
driver.quit()
