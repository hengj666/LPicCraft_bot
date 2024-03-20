import os  
import glob  
import json  
import logging  

if os.path.exists('temp_filter.log'):  
        os.remove('temp_filter.log')

logging.basicConfig(filename='temp_filter.log', level=logging.DEBUG,  
                    format='- %(message)s')  
  
# 清空temp_filter.json中的所有值  
def clear_json_file(json_path):  
    with open(json_path, 'w') as file:  
        json.dump({}, file)  
  
# 计数具有特定扩展名的文件  
def count_files_with_extensions(folder, extensions):  
    count = 0  
    for ext in extensions:  
        count += len(glob.glob(os.path.join(folder, f'*.{ext}')))  
    return count  
  
# 检测文件是否存在  
def check_file_existence(folder, filename):  
    return os.path.isfile(os.path.join(folder, filename))  
  
# 检测多个文件是否都存在  
def check_multiple_files_existence(folder, filenames):  
    return all(check_file_existence(folder, filename) for filename in filenames)  
  
# 比较多种类型文件的数量是否相等  
def compare_file_counts(folder, extensions1, extension2):  
    count1 = sum(len(glob.glob(os.path.join(folder, f'*.{ext}'))) for ext in extensions1)  
    count2 = len(glob.glob(os.path.join(folder, f'*.{extension2}')))  
    return count1 == count2  
  
# 主函数  
def main():  
    json_path = "script_file/temp_filter.json"  
    font_folder = "font"  
    templet_folder = "templet"  
    data_file_folder = "data_file"  
  
    # 清空JSON文件  
    clear_json_file(json_path)  
  
    # 检测并更新JSON文件  
    data = {}  
    # 检查Adobe Std R.otf文件是否存在  
    data['error_msg1'] = 'yes' if check_file_existence(font_folder, "Adobe Std R.otf") else 'error'  
    if data['error_msg1'] == 'yes':  
        logging.info("字体文件加载成功")
    else:  
        print("Adobe Std R.otf文件不存在，检查失败。")  
        logging.info("字体文件加载失败，请检查font/Adobe Std R.otf路径")
  
    # 检查多个文件是否都存在  
    data['error_msg2'] = 'yes' if check_multiple_files_existence(templet_folder, ["mhcz.jpg", "pgt.jpg", "sbx.jpg"]) else 'error'  
    if data['error_msg2'] == 'yes':  
        logging.info("原始图片加载成功")
    else:  
        logging.info("原始图片加载失败，请检查templet路径")
  
    # 比较压缩文件和文本文件的数量  
    compress_extensions = ['zip', 'rar', 'tar', 'gz', 'bz2', '7z']  
    data['error_msg3'] = 'yes' if compare_file_counts(data_file_folder, compress_extensions, 'txt') else 'error'  
    if data['error_msg3'] == 'yes':  
        logging.info("压缩文件与文本文件匹配成功")  
    else:   
        logging.info("压缩文件与文本文件匹配失败，加入的压缩文件与文本文件数量不一致") 
  
    # 计算压缩文件和文本文件的数量（可选，因为已经在compare_file_counts中进行了比较）  
    compress_count = count_files_with_extensions(data_file_folder, compress_extensions)  
    txt_count = len(glob.glob(os.path.join(data_file_folder, '*.txt')))  
  
    # 检查压缩文件和文本文件是否都足够（大于2个）  
    data['gen_msg2'] = 'yes' if compress_count > 2 and txt_count > 2 else '文件较少'  
    if data['gen_msg2'] == 'yes':  
        print(f"压缩文件与文本文件均被成功识别")  
    else:  
        logging.info("压缩文件与文本文件的数量较少，可能没有完全加入")  
  
    # 根据error_msg字段的值设置out字段  
    data['out'] = 'yes' if all(value == 'yes' for key, value in data.items() if key.startswith('error_msg')) else 'error'  
    if data['out'] == 'yes':  
        logging.info("所有文件识别成功，允许进行下一步") 
    else:  
        logging.info("在文件识别中出现了错误，无法进行下一步")  
  
    # 将结果写入JSON文件  
    with open(json_path, 'w') as file:  
        json.dump(data, file, ensure_ascii=False, indent=4)  
  
if __name__ == "__main__":  
    main()