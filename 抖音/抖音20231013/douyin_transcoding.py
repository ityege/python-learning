# 抖音爬虫批量视频转码
# 直接下载的视频有点问题，pr不识别flv格式视频，转成mp4
# 直接使用ffmpeg转就行
import os

os.chdir("sp")
# 获取当前目录
current_dir = os.getcwd()

# 获取当前目录中的所有文件
files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]

# 获取文件名（不包括后缀名）
file_names = [os.path.splitext(f)[0] for f in files]

# 打印文件名（不包括后缀名）
for file_name in file_names:
    ml = f"ffmpeg -i {file_name}.flv {file_name}.mp4"
    os.system(ml)
