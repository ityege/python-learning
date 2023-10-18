import os

download_dict = {
                 "名称":"https://www.douyin.com/user/uerid",
                 }
for key, value in download_dict.items():
    # 爬取视频
    os.system(f"python douyin_download2.py {key} {value}")
    # 视频转码
    os.system(f"python douyin_transcoding.py {key}")

