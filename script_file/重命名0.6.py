import os
import json
import re
import tkinter as tk
from tkinter import messagebox
print("当前工作目录:", os.getcwd())

# 检查当前工作目录是否为目标目录，如果不是则切换
if os.path.basename(os.getcwd()) != "script_file":
    try:
        os.chdir("script_file")
        print("已将工作目录更改为 'script_file'")
    except FileNotFoundError:
        print("目标目录 'script_file' 不存在！")
else:
    print("当前工作目录已经是目标目录，无需更改。")

# 允许的图片文件扩展名
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

def get_image_files(root_folder):
    """
    获取文件夹内所有图片文件的名称列表。
    返回一个字典，其中键是文件夹路径，值是该文件夹内所有图片文件的名称列表。
    """
    image_files = {}
    for root, dirs, files in os.walk(root_folder):
        image_files[root] = [file for file in files if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS]
    return image_files

def rename_files_based_on_json(json_file_path, root_folder):
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 用于记录未成功重命名的文件
    unmatched_files = {}

    # 遍历JSON数据中的每一项
    for item in data:
        folder_name_pattern = item['FolderNamePattern']
        old_file_name = item['OldFileName']
        new_file_name = item['NewFileName']

        # 遍历根文件夹下的所有项目（文件夹或文件）
        for root, dirs, files in os.walk(root_folder):
            # 对于每个文件夹，检查是否与文件夹名模式匹配
            for dir_name in dirs:
                if re.match(folder_name_pattern, dir_name):
                    folder_path = os.path.join(root, dir_name)

                    # 构建文件路径
                    old_file_path = os.path.join(folder_path, old_file_name)

                    # 如果文件存在，则尝试重命名
                    if os.path.exists(old_file_path):
                        try:
                            # 构建新的文件路径
                            new_file_path = os.path.join(folder_path, new_file_name)

                            # 重命名文件
                            os.rename(old_file_path, new_file_path)
                            print(f"已将文件 {old_file_name} 重命名为 {new_file_name}")
                        except Exception as e:
                            # 记录未成功重命名的文件
                            unmatched_files.setdefault(folder_path, []).append(old_file_name)
                            print(f"重命名文件 {old_file_name} 时出错：{str(e)}")

    # 获取所有图片文件列表
    image_files = get_image_files(root_folder)

    # 遍历图片文件列表，将未成功重命名的图片文件记录下来
    for folder, files in image_files.items():
        for file in files:
            for item in data:
                if file == item['NewFileName']:
                    break
            else:
                unmatched_files.setdefault(folder, []).append(file)

    # 如果存在未成功重命名的文件，弹出错误提示窗口
    if unmatched_files:
        error_message = "以下图片文件未按照标准命名方式命名：\n"
        for folder, files in unmatched_files.items():
            error_message += f"{folder}:\n"
            for file in files:
                error_message += f" - {file}\n"
        error_message += "\n解决方式：\n1. 查看命名标准修改文件命名。\n2. 在Rename.json文件中添加匹配规则。"
        messagebox.showerror("获取信息图片错误", error_message)

# 示例
json_file_path = r'Rename.json'  # JSON文件路径
root_folder = r'../data_file'  # 根文件夹路径
rename_files_based_on_json(json_file_path, root_folder)

import subprocess

# 指定要运行的Python脚本路径
next_script_path = "id.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])