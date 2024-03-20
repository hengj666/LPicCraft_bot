import re
import os
from opencc import OpenCC
from datetime import datetime

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
TData_relative = os.path.join("..", "TData")

# 获取数据文件夹的绝对路径
absolute_data_file = os.path.abspath(os.path.join(current_dir, data_file_relative))
absolute_TData = os.path.abspath(os.path.join(current_dir, TData_relative))

# 现在可以使用 absolute_data_file 变量来引用数据文件夹中的内容
print(absolute_data_file)
print(absolute_TData)

# 初始化简繁体转换器
converter = OpenCC('t2s')  # 繁体转简体

# 定义要匹配的模式
pattern1 = r'(\d+)期(.*?)(跑狗图)'
pattern2 = r'(\d+)期(.*?)(四不像)'
pattern3 = r'(\d+)期(.*?)(马会传真)'
pattern4 = r'解得(:|：|)\s*([鼠牛虎兔龙蛇马羊猴鸡狗猪\s]+)'
pattern5 = r'本期重点(:|：|)\s*([鼠牛虎兔龙蛇马羊猴鸡狗猪\s]+)'
pattern6 = r'(澳门|新澳门|台湾|香港)'
pattern7 = r'(\d+)期'

# 获取当前日期并格式化为年月日字符串
# current_date = datetime.now().strftime("%y%m%d")

# 用户输入文件夹路径
input_folder = rf"..\\data_file"

# 确保输出文件夹存在
output_dir = absolute_TData
os.makedirs(output_dir, exist_ok=True)

# 打开文本文件进行读取和处理
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file_path = os.path.join(input_folder, filename)
        # 打开文本文件进行读取
        with open(input_file_path, "r", encoding="utf-8") as file:
            # 读取第一行并进行简繁体转换
            first_line = converter.convert(file.readline().strip())
            
            # 使用正则表达式进行匹配，找到第一行中的指定字符串
            match_first_line = re.search(pattern6, first_line)
            if match_first_line:
                # 使用正则表达式匹配第一行中的期号信息
                match_second_line = re.search(pattern7, first_line)
                if match_second_line:
                    # 提取匹配到的部分作为文件名
                    file_name = match_first_line.group(0) + match_second_line.group(1).zfill(3) + "期"
                    
                    # 添加“(图库)”字符串到文件名中
                    if "图库" in filename:
                        file_name = "(图库)" + file_name
                    
                    # 创建一个新的文本文件用于写入匹配结果
                    output_file_path = os.path.join(output_dir, f"{file_name}.txt")
                    with open(output_file_path, "w", encoding="utf-8") as output_file:
                        # 重新打开文件并逐行读取
                        file.seek(0)
                        for line in file:
                            # 进行简繁体转换
                            line = converter.convert(line.strip())
                            # 在每一行中查找目标字符串
                            if "解得" in line or "本期重点" in line:
                                # 在目标所在行的倒数第三位字符前添加五个空格
                                if len(line) >= 3:
                                    line = line[:-3] + "     " + line[-3:]
                            # 使用正则表达式进行匹配
                            match1 = re.search(pattern1, line)
                            match2 = re.search(pattern2, line)
                            match3 = re.search(pattern3, line)
                            match4 = re.search(pattern4, line)
                            match5 = re.search(pattern5, line)
                            
                            # 如果找到匹配项，则写入匹配到的内容到新文件中
                            if match1:
                                result = match1.group(3) + "=" + match1.group(2).replace("新版", "") + " " + match1.group(1).zfill(3) + "期"
                                output_file.write(result + "\n")
                            elif match2:
                                result = match2.group(3) + "=" + match2.group(2).replace("新版", "") + " " + match2.group(1).zfill(3) + "期"
                                output_file.write(result + "\n")
                            elif match3:
                                result = match3.group(3) + "=" + match3.group(2).replace("新版", "") + " " + match3.group(1).zfill(3) + "期"
                                output_file.write(result + "\n")
                            elif match4:
                                output_file.write(match4.group(0) + "\n")
                            elif match5:
                                output_file.write(match5.group(0) + "\n")
        
        print(f"文件 {filename} 的匹配结果已写入到新文件中。")

print("所有文件处理完成。")


# 遍历TData文件夹中的所有TXT文件
for filename in os.listdir(output_dir):
    if filename.endswith(".txt") and "图库" in filename:
        file_path = os.path.join(output_dir, filename)
        temp_file_path = os.path.join(output_dir, "temp_" + filename)
        with open(file_path, "r", encoding="utf-8") as input_file:
            with open(temp_file_path, "w", encoding="utf-8") as temp_file:
                for i, line in enumerate(input_file, 1):
                    if i % 2 != 0:  # 如果是奇数行
                        temp_file.write("图库" + line)  # 在行首添加“图库”
                    else:
                        temp_file.write(line)  # 写入原始行内容
        os.remove(file_path)  # 删除原始文件
        os.rename(temp_file_path, file_path)  # 重命名临时文件为原始文件名
        print(f"文件 {filename} 的处理已完成。")

import subprocess

# 指定要运行的Python脚本路径
next_script_path = "Servo2.0.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])
