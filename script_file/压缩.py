import os
import shutil
from datetime import datetime
import zipfile
import logging

# 检查当前工作目录是否为目标目录，如果不是则切换
if os.path.basename(os.getcwd()) != "script_file":
    try:
        os.chdir("script_file")
        print("已将工作目录更改为 'script_file'")
    except FileNotFoundError:
        print("目标目录 'script_file' 不存在！")
else:
    print("当前工作目录已经是目标目录，无需更改。")

logging.basicConfig(filename='file_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前日期，格式为yymmdd
today_date = datetime.now().strftime("%y%m%d")
info_today_date = datetime.now().strftime("%Y年%m月%d日%H:%M:%S")

logging.info(f"运行日期：{info_today_date}")
  
def move_existing_archives(directory):  
    # 压缩文件的扩展名列表  
    archive_extensions = ['.zip', '.rar', '.tar', '.gz', '.bz2', '.7z']  
    history_folder = os.path.join(directory, 'history')  
      
    # 如果history文件夹不存在，则创建它  
    if not os.path.exists(history_folder):  
        os.makedirs(history_folder)  
      
    # 遍历文件夹中的所有文件  
    for filename in os.listdir(directory):  
        # 检查文件扩展名是否在压缩文件扩展名列表中  
        _, ext = os.path.splitext(filename)  
        if ext.lower() in archive_extensions:  
            # 构建源文件和目标文件的完整路径  
            source_path = os.path.join(directory, filename)  
            destination_path = os.path.join(history_folder, filename)  
              
            # 如果是一个文件（而不是文件夹），则移动它  
            if os.path.isfile(source_path):  
                shutil.move(source_path, destination_path)  
                # 打印文件名和新位置  
                logging.info(f"已将旧版本的压缩包 {filename} 移动到 {destination_path}")
  
# 设置要搜索的文件夹路径  
directory_path = '..\\output'  
# 调用函数  
move_existing_archives(directory_path)

def find_image_files(directory):  
    # 支持的图片文件扩展名列表  
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  
    image_files = []  
      
    # 遍历文件夹中的所有文件  
    for filename in os.listdir(directory):  
        # 检查文件扩展名是否在支持的列表中  
        _, ext = os.path.splitext(filename)  
        if ext.lower() in image_extensions:  
            image_files.append(filename)  
      
    # 如果没有找到图片文件，返回None  
    if not image_files:  
        return None  
      
    return image_files  
  
# 设置你要搜索的文件夹路径  
directory_path = '..\\output'  # 替换为你的文件夹路径  
  
# 调用函数  
image_files = find_image_files(directory_path)  
  
# 输出结果或打印提示  
if image_files is None:  
    logging.info("没有检测到图片文件。")
else:  
    for image_file in image_files:  
        print(image_file)
        logging.info(f"{image_file}")

# 创建目标文件夹路径
output_folder = "..\\output"
target_folder1 = os.path.join(output_folder, f"{today_date}-导出")
target_folder2 = os.path.join(output_folder, f"{today_date}-图库-导出")

# 创建目标文件夹
os.makedirs(target_folder1, exist_ok=True)
os.makedirs(target_folder2, exist_ok=True)

# 遍历output文件夹中的所有文件
for filename in os.listdir(output_folder):
    source_file = os.path.join(output_folder, filename)
    
    # 检查是否为文件
    if os.path.isfile(source_file):
        # 检查文件名中是否包含“图库”
        if "图库" in filename:
            # 将文件移动到“图库”文件夹
            target_file = os.path.join(target_folder2, filename)
            shutil.move(source_file, target_file)
            print(f"Moved {filename} to {target_folder2}")
        else:
            # 将文件移动到普通导出文件夹
            target_file = os.path.join(target_folder1, filename)
            shutil.move(source_file, target_file)
            print(f"Moved {filename} to {target_folder1}")

print("Classification completed.")

logging.info("对图片文件进行分类，添加进对应的文件夹")

# 分别压缩两个文件夹
for folder in [target_folder1, target_folder2]:
    zip_filename = os.path.join(output_folder, f"{os.path.basename(folder)}.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder))

    print(f"Compression completed: {zip_filename}")

logging.info("将文件夹进行压缩")

logging.info("-------------------------------------------------")
logging.info(f"保存了{target_folder1}.zip与{target_folder2}.zip文件")
logging.info("-------------------------------------------------")

    # 删除原文件夹
for folder in [target_folder1, target_folder2]:
    shutil.rmtree(folder)
    print(f"删除了原文件夹: {folder}")

logging.info(f"保留压缩文件，删除原始文件夹")

# 弹出的文件夹路径
folder_path = "..\\output"

# 打开文件夹
os.startfile(folder_path)

print("原文件夹删除完成。")
logging.info(f"运行结束")
