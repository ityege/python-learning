# 录制抖音直播,直接使用ffmpeg录制就行了
import os
import time
# 直播间推流url
url=""
ml=f'ffmpeg -i "{url}" -c copy {int(time.time())}.flv'
print(ml)
os.system(ml)