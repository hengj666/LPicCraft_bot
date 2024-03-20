import os
import shutil

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

def move_images_to_temp_data(root_folder):
    temp_data_path = os.path.join(root_folder, "Temp_data")
    
    # 创建 Temp_data 文件夹（如果不存在）
    if not os.path.exists(temp_data_path):
        os.makedirs(temp_data_path)
    
    # 遍历根文件夹下的所有文件夹
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        
        # 如果当前路径是文件夹且不是 Temp_data 文件夹
        if os.path.isdir(folder_path) and folder_name != "Temp_data":
            # 遍历文件夹中的所有文件
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                # 检查文件是否是图片文件（这里只检查文件扩展名）
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # 移动文件到 Temp_data 文件夹
                    shutil.move(file_path, temp_data_path)
                    
                    print(f"文件 {file_name} 已移动到 Temp_data 文件夹")
                    
            # 删除原文件夹
            shutil.rmtree(folder_path)
            print(f"文件夹 {folder_name} 已删除")

# 指定根文件夹路径
root_folder_path = absolute_data_file

# 调用函数移动图片文件到 Temp_data 文件夹并删除原文件夹
move_images_to_temp_data(root_folder_path)

import subprocess

# 指定要运行的Python脚本路径
next_script_path = "文档修改0.5.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])
