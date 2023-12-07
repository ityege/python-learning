from flask import Flask, send_from_directory
import os
import sys

app = Flask(__name__)
# 获取当前脚本的路径
path_arg = os.path.dirname(os.path.abspath(__file__))

@app.route('/<path:filename>')
def get_file(filename):
    # 使用 global 关键字引用全局变量
    global path_arg
    # 构建文件的完整路径
    file_path = os.path.join(path_arg, filename)
    # 检查文件是否存在
    if os.path.isfile(file_path):
        # 使用 send_from_directory 函数发送文件
        return send_from_directory(path_arg, filename)
    else:
        return '文件不存在'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 获取命令行参数中的路径
        path_arg = sys.argv[1]
        # 启动 Flask 应用
        app.run(port=80)
    else:
        print("使用当前路径作为文件路径!!!!!!!!")