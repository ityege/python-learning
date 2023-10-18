# 抖音爬虫批量视频转码
# 直接下载的视频有点问题，pr不识别flv格式视频，转成mp4
# 直接使用ffmpeg转就行
import os
import logging
from tqdm import tqdm
import subprocess
import sys

arguments = sys.argv
# 创建日志记录器
logger = logging.getLogger(__name__)
# 配置日志文件路径和格式
log_file = 'log_douyin_transcoding.log'
log_format = '%(asctime)s - %(levelname)s - %(message)s'

# 创建文件处理器并添加到日志记录器
file_handler = logging.FileHandler(log_file, mode='a')
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)

# 设置日志级别
logger.setLevel(logging.INFO)

os.chdir(arguments[1])
# 获取当前目录
current_dir = os.getcwd()

# 获取当前目录中的所有文件
files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]

# 获取文件名（不包括后缀名）
file_names = [os.path.splitext(f)[0] for f in files]
a = 0;
print("开始转码视频",arguments[1])
# 打印文件名（不包括后缀名）
for file_name in tqdm(file_names, desc='Processing', unit='file'):
    a += 1
    # ml = f"ffmpeg -i {file_name}.flv {file_name}.mp4"
    # return_value = os.system(ml)
    # 执行命令，将输出重定向到空设备
    ml = f'ffmpeg -i {file_name}.flv {file_name}.mp4 >> run.log 2>&1'
    # print(ml)
    return_value = subprocess.call(ml, shell=True)
    logger.info("转码返回值:{},转码进度:{},总视频数量:{}".format(return_value, a, len(file_names)))
    os.remove(f"{file_name}.flv")
