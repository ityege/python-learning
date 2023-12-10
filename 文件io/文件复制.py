source_file_path = "source.txt"  # 源文件路径
destination_file_path = "destination.txt"  # 目标文件路径

with (open(source_file_path, "r") as source_file,
      open(destination_file_path, "w") as destination_file):
    line = source_file.readline()
    while line:
        destination_file.write(line)
        line = source_file.readline()

print("文件复制完成。")
