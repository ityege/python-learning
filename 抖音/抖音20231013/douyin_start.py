import os

download_dict = {}

# 打开文本文件
with open('paqu.txt', 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 处理每一行的内容
        split = line.split("=")
        download_dict[split[0]] = split[1][:-1]
print(download_dict)
print(len(download_dict))
for key, value in download_dict.items():
    # 爬取视频
    os.system(f"python douyin_download2.py {key} {value}")
    # 视频转码
    os.system(f"python douyin_transcoding.py {key}")
