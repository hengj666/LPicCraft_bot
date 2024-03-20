import os
import rarfile
import zipfile

# 检查当前工作目录是否为目标目录，如果不是则切换
if os.path.basename(os.getcwd()) != "script_file":
    try:
        os.chdir("script_file")
        print("已将工作目录更改为 'script_file'")
    except FileNotFoundError:
        print("目标目录 'script_file' 不存在！")
else:
    print("当前工作目录已经是目标目录，无需更改。")

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 指定数据文件夹相对于当前脚本所在目录的相对路径
data_file_relative = os.path.join("..", "data_file")

# 获取数据文件夹的绝对路径
absolute_data_file = os.path.abspath(os.path.join(current_dir, data_file_relative))

# 现在可以使用 absolute_data_file 变量来引用数据文件夹中的内容
print(absolute_data_file)



def unrar_file(file_path, output_folder):
    # 获取文件的文件名（不带扩展名）
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # 创建用于存放解压文件的文件夹
    os.makedirs(output_folder, exist_ok=True)

    if file_path.endswith('.rar'):
        # 解压缩RAR文件
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(output_folder)
    elif file_path.endswith('.zip'):
        # 解压缩ZIP文件
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)

    print(f"已解压缩文件到目录: {output_folder}")

    # 删除源文件
    os.remove(file_path)
    print(f"已删除源文件: {file_path}")

def unrar_all_files_in_data_file():
    # 获取"data_file"文件夹路径
    current_directory = os.getcwd()
    data_file = absolute_data_file

    # 检查"data_file"文件夹是否存在
    if os.path.exists(data_file):
        # 遍历"data_file"文件夹中的所有文件
        for filename in os.listdir(data_file):
            file_path = os.path.join(data_file, filename)
            # 检查是否为RAR或ZIP文件
            if filename.endswith('.rar') or filename.endswith('.zip'):
                # 解压文件
                unrar_file(file_path, os.path.join(absolute_data_file, os.path.splitext(filename)[0]))

# 调用函数解压"data_file"文件夹中的所有RAR和ZIP文件，并删除源文件
unrar_all_files_in_data_file()

import subprocess

# 指定要运行的Python脚本路径
next_script_path = "重命名0.6.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])
