import os
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

# 定义TData文件夹路径
folder_path = absolute_TData

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    # 检查文件是否是JSON文件
    if file_name.endswith(".json"):
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, file_name)
        
        # 打开JSON文件进行处理
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                # 加载JSON数据
                json_data = json.load(json_file)
                
                # 遍历JSON数据中的每个键值对
                for key, item in json_data.items():
                    # 检查是否存在"text1_original"字段
                    if "text1_original" in item:
                        # 获取"text1_original"字段的值
                        text1_original = item["text1_original"]
                        
                        # 提取"="后的信息作为期数
                        text1 = text1_original.split("=")[-1].strip()
                        
                        # 删除"text1"中所有的空格
                        text1 = text1.replace(" ", "")
                        
                        # 获取"text1_original"中“=”后“ ”前的内容作为地区信息
                        area = text1_original.split("=")[-1].split(" ")[0]
                        
                        # 获取"text1_original"中“=”前的内容作为分类信息
                        class_info = text1_original.split("=")[0]
                        class_info = class_info.replace("图库", "")
                        
                        # 添加新的字段
                        item["text1"] = text1

                        expect = text1_original.split(" ")[-1].split("期")[0]
                        
                        # 设置"name"字段
                        if "图库" in text1_original:
                            item["name"] = f"{expect}_图库_{area}_{class_info}"
                        else:
                            item["name"] = f"{expect}_{area}_{class_info}"
                        
                        # 设置"expect"字段
                        
                        item["expect"] = expect
                        
                        # 设置"area"字段
                        item["area"] = area
                        
                        # 设置"class"字段
                        item["class"] = class_info
                        
                        # 检查是否存在"text2"字段
                    if "text2" in item:
                        # 获取"text2"字段的值
                        text2 = item["text2"]

                        # 删除"text2"中冒号（":"）或者中文冒号（"："）前的文字
                        text2 = text2.split(":")[-1].strip()
                        text2 = text2.split("：")[-1].strip()
                        
                        # 删除冒号（":"）或者中文冒号（"："）
                        text2 = text2.replace(":", "")
                        text2 = text2.replace("：", "")
                        
                        # 添加新的字段
                        item["text2"] = text2

                    if "overlay_image_path" in item:
                        # 获取"overlay_image_path"字段的值并在前面添加"..\\"前缀
                        overlay_image_path = "..\\" + item["overlay_image_path"]

                        # 添加新的字段
                        item["overlay_image_path"] = overlay_image_path

                        # 保存修改后的JSON文件
                        with open(file_path, 'w', encoding='utf-8') as updated_json_file:
                            json.dump(json_data, updated_json_file, indent=4, ensure_ascii=False)
                    
                print(f"已修改文件: {file_path}")
                
            except json.JSONDecodeError:
                print(f"无法解析JSON文件: {file_path}")

print("所有JSON文件处理完成。")

import subprocess

# 指定要运行的Python脚本路径
next_script_path = "pg-图片修改0.8.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])
