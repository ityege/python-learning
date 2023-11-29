# 通过元素获取有一点问题,新的通过请求
import os
import glob
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
import logging
from tqdm import tqdm
import sys

arguments = sys.argv

# 使用 os.path.exists() 方法判断目录是否存在
if not os.path.exists(arguments[1]):
    # 如果目录不存在，则使用 os.makedirs() 方法创建目录
    os.makedirs(arguments[1])
    print("目录已创建")
else:
    print("目录已存在")
    # 使用 glob 模块匹配目录下的所有 FLV 文件
    flv_files = glob.glob(os.path.join(arguments[1], "*.flv"))
    mp4_files = glob.glob(os.path.join(arguments[1], "*.mp4"))
    # 判断是否存在 FLV 文件
    if len(flv_files)  > 0 or len(mp4_files) > 0:
        print("目录下存在 flv,mp4 文件")
        exit(0)
    else:
        print("目录下不存在 flv,mp4 文件")

# 创建日志记录器
logger = logging.getLogger(__name__)
# 配置日志文件路径和格式
log_file = f'{arguments[1]}/log_douyin_download.log'
log_format = '%(asctime)s - %(levelname)s - %(message)s'

# 创建文件处理器并添加到日志记录器
file_handler = logging.FileHandler(log_file, mode='a')
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)

# 设置日志级别
logger.setLevel(logging.INFO)

distinct = set();

# 指定驱动
service = Service('C:/devtools/chrome/chromedriver.exe')

# 创建 ChromeOptions 对象
chrome_options = Options()
# 指定数据目录
chrome_options.add_argument("--user-data-dir=D:/code/pythontest/data")
# 创建 WebDriver 对象并指定选项
driver = webdriver.Chrome(service=service, options=chrome_options)
#窗口最大化
driver.maximize_window()
# 打开抖音，博主主页
driver.get(arguments[2])


# 显式等待，等待10秒，直到元素可见
wait = WebDriverWait(driver, 20)
element = wait.until(EC.visibility_of_element_located(

    (By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[2]/div/div/div[3]/div/div/div[1]/div[2]/div/div[1]/div[1]/h2/span[2]")))

# 获取到作者有多少个视频
video_num = element.text
print("视频数量: ", video_num)
logger.info("视频数量: {}".format(video_num))

first_video = wait.until(EC.visibility_of_element_located((By.XPATH,

                                                           '/html/body/div[2]/div[1]/div[4]/div[2]/div/div/div[3]/div/div/div[2]/div[2]/div[2]/ul/li[1]/div/a/div/div[1]/img')))
# 打开第一个视频
print("开始爬取视频",arguments[1])
logger.info("开始爬取视频: {}".format(arguments[1]))
first_video.click()
a = 0
for _ in tqdm(range(int(video_num) - 1), desc='Processing', unit='video'):
    # 模仿人,视频不能刷太快
    time.sleep(random.randint(8, 10))
    logger.info("爬取进度: {},总视频数量:{}".format(a, video_num))
    a += 1
    # 切换下一个视频
    actions = ActionChains(driver)
    actions.send_keys(Keys.DOWN)
    actions.perform()
a = 0
# 获取所有请求
print("开始下载视频",arguments[1])
logger.info("开始下载视频: {}".format(arguments[1]))
# print("正在保存视频url")
# for request in tqdm(driver.requests, desc='Processing', unit='request'):
#     if request.response.headers['Content-Type'] == "video/mp4":
#         logger.info(request.url)
# print("正在下载视频")
for request in tqdm(driver.requests, desc='Processing', unit='request'):
    # 下面是处理视频
    if request.response == None:
        # logger.info(
        #     "请求体为空:下载进度: {},总视频数量:{},请求url:{}".format(a, len(driver.requests),request.url))
        # a+=1
        continue
    if request.response.headers['Content-Type'] == "video/mp4":
        # 下载视频
        try:
            response = requests.get(request.url,timeout=30)

        #无论遇到什么异常,一律捕获继续处理下一个视频
        except Exception as e:
            print(f"捕获到异常：{e}")
            continue
        md5_hash = hashlib.md5(response.content).hexdigest()
        if md5_hash in distinct:
            pass
        else:
            distinct.add(md5_hash)
            # 保存视频 保存为flv再转码成mp4,不让导入pr音频有问题
            filename = arguments[1] + "/" + str(uuid.uuid4()) + ".flv"  # 保存的文件名
            with open(filename, "wb") as file:
                logger.info(
                    "下载:下载进度: {},总视频数量:{},文件名称:{},请求url:{}".format(a, len(driver.requests), filename,
                                                                               request.url))
                file.write(response.content)
            a += 1
    # else:
    #      logger.info(
    #          "没有下载:下载进度: {},总视频数量:{},请求url:{}".format(a, len(driver.requests), request.url))
    #     a += 1

# 退出浏览器
driver.quit()
