import uuid

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import requests
import time
import random

md_file_name = "古希腊神话故事"

if not os.path.exists(md_file_name):
    # 如果目录不存在，则使用 os.makedirs() 方法创建目录
    os.mkdir(md_file_name)
    os.mkdir(md_file_name + "/img")
    print("目录已创建")
else:
    print("目录已存在")
    # shutil.rmtree(md_file_name)
    # os.mkdir(md_file_name)
    # os.mkdir(md_file_name + "/img")

# 指定驱动
service = Service('C:/devtools/chrome/chromedriver.exe')

# 创建 ChromeOptions 对象
chrome_options = Options()
# 指定数据目录
chrome_options.add_argument("--user-data-dir=D:/code/pythontest/data")
# 创建 WebDriver 对象并指定选项
driver = webdriver.Chrome(service=service, options=chrome_options)
# 窗口最大化
driver.maximize_window()
# 打开抖音，博主主页
driver.get("https://book.qq.com/")
print("这里加断点,用于人工干预打开需要爬虫的网页")

# 获取所有标签页的句柄
window_handles = driver.window_handles

# 切换到新标签页
new_window_handle = window_handles[-1]
driver.switch_to.window(new_window_handle)

md_file = open(md_file_name + "/" + md_file_name + ".md", "a")


def analysis_label(parentNode):
    childsNode = parentNode.find_elements(By.XPATH, "./*")
    # 具有子节点
    if len(childsNode) > 0:
        text = parentNode.text
        if text != "":
            md_file.write(text + "\n\n")
        for chid in childsNode:
            analysis_label(chid)
    else:
        tag_name = parentNode.tag_name
        class_name = parentNode.get_attribute('class')
        if tag_name == "h1":
            md_file.write("# " + parentNode.text + "\n\n")
        elif tag_name == "h2":
            md_file.write("## " + parentNode.text + "\n\n")
        elif tag_name == "h3":
            md_file.write("### " + parentNode.text + "\n\n")
        elif tag_name == "h4":
            md_file.write("#### " + parentNode.text + "\n\n")
        elif tag_name == "h5":
            md_file.write("#### " + parentNode.text + "\n\n")
        elif tag_name == "h6":
            md_file.write("##### " + parentNode.text + "\n\n")
        elif tag_name == "p" and class_name == "tuti":
            pass
            # md_file.write(parentNode.text + "\n\n")
        elif tag_name == "i":
            pass
        elif tag_name == "sub":
            pass
        elif tag_name == "li":
            pass
        elif tag_name == "del":
            pass
        elif tag_name == "em":
            pass
        elif tag_name == "sup":
            pass
        elif tag_name == "code":
            pass
        elif tag_name == "strong":
            pass
        elif tag_name == "br":
            pass
        elif tag_name == "hr":
            pass
        elif tag_name == "span":
            pass
        elif tag_name == "a":
            pass
        elif tag_name == "p" and class_name=="imgtitle":
            pass
        elif tag_name == "p":
            md_file.write(parentNode.text + "\n\n")
        elif tag_name == "b":
            md_file.write(parentNode.text + "\n\n")
        elif tag_name == "img":
            url = parentNode.get_attribute("src")
            # 从URL中获取文件名
            file_name = str(uuid.uuid4()) + ".png"
            with open(md_file_name + "/img/" + file_name, "wb") as file:
                try:
                    response = requests.get(url, timeout=30)
                except Exception as e:
                    print(f"捕获到异常：{e}")
                file.write(response.content)
                file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]
                md_file.write("![" + file_name_without_extension + "](""img/" + file_name + ")" + "\n\n")
        elif tag_name == "pre":
            md_file.write("~~~python\n" + parentNode.text + "\n~~~\n\n")

        else:
            raise Exception("未知标签:"+tag_name+"->"+class_name)


while True:
    # 找到父元素
    wait = WebDriverWait(driver, 20)
    chapter = wait.until(EC.visibility_of_element_located(
        (By.ID, "article")))

    # 获取父元素的全部子元素
    child_elements = chapter.find_elements(By.XPATH, "./*")
    for chid in child_elements:
        analysis_label(chid)
    nextZhangs = driver.find_elements(By.CLASS_NAME, 'ypc-btn')
    flag=True
    for nextZhang in nextZhangs:
        if nextZhang.text == "下一章":
            nextZhang.click()
            flag=False
    if flag==True:
        driver.quit()
        exit(100)
    time.sleep(random.randint(8, 10))
    print("断点")
