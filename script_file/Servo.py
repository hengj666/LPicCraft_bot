import os
import tkinter as tk
from tkinter import messagebox
import json

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
TData_relative = os.path.join("..", "TData")

# 获取数据文件夹的绝对路径
absolute_TData = os.path.abspath(os.path.join(current_dir, TData_relative))

# 现在可以使用 absolute_TData 变量来引用数据文件夹中的内容
print(absolute_TData)

def merge_txt_files(source_folder, destination_file):
    # 打开目标文件以写入模式，使用UTF-8编码
    with open(destination_file, 'w', encoding='utf-8') as dest_file:
        # 遍历源文件夹中的所有文件
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                # 检查文件是否是txt文件
                if file.endswith(".txt"):
                    source_file_path = os.path.join(root, file)
                    # 读取源文件内容并写入目标文件
                    with open(source_file_path, 'r', encoding='utf-8') as src_file:
                        dest_file.writelines(src_file.readlines())
                    print(f"复制文件内容: {source_file_path}")

def delete_existing_servo_files(folder):
    servo_files = [f for f in os.listdir(folder) if "Servo" in f]
    if servo_files:
        msg = f"目标文件夹中已存在名称中含有“Servo”的文件:\n{', '.join(servo_files)}。\n是否删除这些文件并继续运行？"
        if messagebox.askokcancel("删除确认", msg):
            for file in servo_files:
                os.remove(os.path.join(folder, file))
            print("已删除现有的Servo文件。")
            return True
        else:
            messagebox.showinfo("运行中止", "目标文件夹存在已经生成的Servo文件，无法继续运行。")
            return False
    return True

# 源文件夹路径
source_folder = absolute_TData
# 目标文件路径
destination_file = os.path.join(source_folder, "Servo.txt")

# 检查并删除现有的Servo文件
if not delete_existing_servo_files(source_folder):
    exit()

# 执行合并操作
merge_txt_files(source_folder, destination_file)

print("合并完成，新文件已保存到:", destination_file)

# 读取Servo.txt文件并识别内容
with open(destination_file, 'r', encoding='utf-8') as servo_file:
    lines = servo_file.readlines()

# 检查是否有“跑狗”关键词，如果有，则提取包含该关键词及其下一行的内容，并将其保存到新的文件中
pg_output_file = os.path.join(source_folder, "pg_Servo.txt")
cz_output_file = os.path.join(source_folder, "cz_Servo.txt")
sbx_output_file = os.path.join(source_folder, "sbx_Servo.txt")

with open(pg_output_file, 'w', encoding='utf-8') as pg_servo_file:
    with open(cz_output_file, 'w', encoding='utf-8') as cz_servo_file:
        with open(sbx_output_file, 'w', encoding='utf-8') as sbx_servo_file:
            for i in range(len(lines) - 1):
                line = lines[i].strip()  # 删除行中的空格
                if "跑狗" in line:  
                    pg_servo_file.write(line + '\n')  
                    pg_servo_file.write(lines[i+1])
                elif "传真" in line or "马会" in line:
                    cz_servo_file.write(line + '\n')
                    cz_servo_file.write(lines[i+1])
                elif "四不像" in line:
                    sbx_servo_file.write(line + '\n')
                    sbx_servo_file.write(lines[i+1])

print("提取完成，新文件已保存到:", pg_output_file, ",", cz_output_file, "和", sbx_output_file)

# 转换为JSON格式并保存
for output_file in [pg_output_file, cz_output_file, sbx_output_file]:
    json_output_file = os.path.splitext(output_file)[0] + ".json"  # 替换文件扩展名为.json
    key = os.path.basename(output_file).split('_')[0]  # 根据文件名确定JSON中的键名
    json_data = {}
    if os.path.exists(json_output_file):
        with open(json_output_file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    with open(output_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            if key == "pg":
                json_data[f"{key}{i//2 + 1}"] = {  
                    "text1_original": lines[i].strip(),
                    "text2": lines[i+1].strip(),
                    "overlay_image_path": "",
                    "top_left_position": [188, 2],
                    "bottom_right_position": [778, 904]
                }
            elif key == "cz":
                json_data[f"{key}{i//2 + 1}"] = {  
                    "text1_original": lines[i].strip(),
                    "text2": lines[i+1].strip(),
                    "overlay_image_path": "",
                    "top_left_position": [166, 2],
                    "bottom_right_position": [850, 904]
                }
            elif key == "sbx":
                json_data[f"{key}{i//2 + 1}"] = {  
                    "text1_original": lines[i].strip(),
                    "text2": lines[i+1].strip(),
                    "overlay_image_path": "",
                    "top_left_position": [122, 2],
                    "bottom_right_position": [987, 904]
                }
    with open(json_output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    print(f"已生成JSON文件: {json_output_file}")

# 定义要删除文件的文件夹路径
folder_path = absolute_TData

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    # 检查文件是否是txt文件
    if file_name.endswith(".txt"):
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, file_name)
        # 删除文件
        os.remove(file_path)

print("已删除TData文件夹内所有txt文件。")

import subprocess

# 指定要运行的Python脚本路径
next_script_path = "json修改.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])
