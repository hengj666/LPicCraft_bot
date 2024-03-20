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

# 定义权重字典，用于确定前缀在overlay_image_path中的位置
prefix_priority = {
    "tk-": 5,
    "tw-": 4,
    "xam-": 3,
    "lam-": 2,
    "xg-": 1
}

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

                    # 检查"text1_original"字段中是否包含"传真"
                    if "text1_original" in item and "传真" in item["text1_original"]:
                        # 如果包含，继续修改"overlay_image_path"值
                        overlay_path = item.get("overlay_image_path", "")
                        if overlay_path.startswith("cz.jpg"):
                            overlay_path = overlay_path.replace("cz.jpg", "")
                        else:
                            overlay_path = overlay_path + "cz.jpg"
                        item["overlay_image_path"] = overlay_path

                    # 检查"text1_original"字段中是否包含"跑狗"
                    if "text1_original" in item and "跑狗" in item["text1_original"]:
                        # 如果包含，继续修改"overlay_image_path"值
                        overlay_path = item.get("overlay_image_path", "")
                        if overlay_path.startswith("pgt.jpg"):
                            overlay_path = overlay_path.replace("pgt.jpg", "")
                        else:
                            overlay_path = overlay_path + "pgt.jpg"
                        item["overlay_image_path"] = overlay_path

                    # 检查"text1_original"字段中是否包含"四不像"
                    if "text1_original" in item and "四不像" in item["text1_original"]:
                        # 如果包含，继续修改"overlay_image_path"值
                        overlay_path = item.get("overlay_image_path", "")
                        if overlay_path.startswith("sbx.jpg"):
                            overlay_path = overlay_path.replace("sbx.jpg", "")
                        else:
                            overlay_path = overlay_path + "sbx.jpg"
                        item["overlay_image_path"] = overlay_path

                    # 检查"text1_original"字段中是否包含"台湾"
                    if "text1_original" in item and "台湾" in item["text1_original"]:
                        # 如果包含，继续修改"overlay_image_path"值
                        overlay_path = item.get("overlay_image_path", "")
                        if overlay_path.startswith("tw-"):
                            overlay_path = overlay_path.replace("tw-", "")
                        else:
                            overlay_path = "tw-" + overlay_path
                        item["overlay_image_path"] = overlay_path
                        
                    # 检查"text1_original"字段中是否包含"=澳门"
                    if "text1_original" in item and "=澳门" in item["text1_original"]:
                        # 如果包含，继续修改"overlay_image_path"值
                        overlay_path = item.get("overlay_image_path", "")
                        if overlay_path.startswith("lam-"):
                            overlay_path = overlay_path.replace("lam-", "")
                        else:
                            overlay_path = "lam-" + overlay_path
                        item["overlay_image_path"] = overlay_path
                        
                    # 检查"text1_original"字段中是否包含"新澳门"
                    if "text1_original" in item and "新澳门" in item["text1_original"]:
                        # 如果包含，继续修改"overlay_image_path"值
                        overlay_path = item.get("overlay_image_path", "")
                        if overlay_path.startswith("xam-"):
                            overlay_path = overlay_path.replace("xam-", "")
                        else:
                            overlay_path = "xam-" + overlay_path
                        item["overlay_image_path"] = overlay_path
                        
                    # 检查"text1_original"字段中是否包含"香港"
                    if "text1_original" in item and "香港" in item["text1_original"]:
                        # 如果包含，继续修改"overlay_image_path"值
                        overlay_path = item.get("overlay_image_path", "")
                        if overlay_path.startswith("xg-"):
                            overlay_path = overlay_path.replace("xg-", "")
                        else:
                            overlay_path = "xg-" + overlay_path
                        item["overlay_image_path"] = overlay_path

                    # 检查"text1_original"字段中是否包含"图库"
                    if "text1_original" in item and "图库" in item["text1_original"]:
                        # 如果包含，修改"overlay_image_path"值
                        item["overlay_image_path"] = "tk-" + item["overlay_image_path"]

                    # 在所有"overlay_image_path"中的最前方添加data_file\Temp_data
                    if "overlay_image_path" in item:
                        item["overlay_image_path"] = "data_file\\Temp_data\\" + item["overlay_image_path"]

                # 保存修改后的JSON文件
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                    
                print(f"已修改文件: {file_path}")
                
            except json.JSONDecodeError:
                print(f"无法解析JSON文件: {file_path}")

print("所有JSON文件处理完成。")

import subprocess

# 指定要运行的Python脚本路径
next_script_path = "最终json生成.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])
