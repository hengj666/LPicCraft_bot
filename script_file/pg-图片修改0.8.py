import os
from PIL import Image, ImageDraw, ImageFont
import json
import logging
file_name = os.path.basename(__file__)

logging.basicConfig(filename='error.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 记录任务开始执行的时间
logging.info("-------------------------------------------------")
logging.info(f"{file_name}任务开始执行")
logging.info(f"{file_name}在前置条件中，未经判断已经被引入了“script_file”工作目录(待后续版本更新)")

print(f"{file_name}当前工作目录:", os.getcwd())

# 检查当前工作目录是否为目标目录，如果不是则切换
if os.path.basename(os.getcwd()) != "script_file":
    try:
        os.chdir("script_file")
        print("已将工作目录更改为 'script_file'")
        logging.info("已经过判定条件将工作目录更改为“script_file”")
    except FileNotFoundError:
        print("目标目录 'script_file' 不存在！")
        logging.info("判定条件试图更改工作目录为“script_file”，但路径不存在，并打印了结果。")
else:
    print("当前工作目录已经是目标目录，无需更改。")
    logging.info("判定条件判断当前正在“script_file”目录中，未进行任何操作。")

logging.info("-------------------------------------------------")

def edit_image(original_image_path, output_image_path, text1, text2, overlay_image_path, top_left_position, bottom_right_position):
    try:
        # 打开原始图片
        logging.info("正在打开原始图片：%s", original_image_path)
        image = Image.open(original_image_path)
        
        # 创建一个可以在图像上绘制的对象
        draw = ImageDraw.Draw(image)
        
        # 选择一个字体
        font = ImageFont.truetype("..\\font\\Adobe Std R.otf", 56)
        
        # 定义文字1的坐标位置
        if "新澳门" in text1:
            text1_position = (123, 922)
        else:
            text1_position = (148, 922)
        
        # 在图像上绘制文本1
        logging.info("在图像上绘制文本1：%s", text1)
        draw.text(text1_position, text1, font=font, fill=(255, 255, 255, 255))
        
        # 在图像上绘制文本2
        logging.info("在图像上绘制文本2：%s", text2)
        draw.text((489, 922), text2, font=font, fill=(255, 255, 255, 255))

        # 打开要添加的图片
        logging.info("正在打开要添加的图片：%s", overlay_image_path)
        overlay = Image.open(overlay_image_path)

        # 图片坐标1
        target_width = bottom_right_position[0] - top_left_position[0]
        target_height = bottom_right_position[1] - top_left_position[1]
        
        # 强制拉伸要添加的图片
        logging.info("图片坐标1：%s", (target_width, target_height))
        overlay = overlay.resize((target_width, target_height))
        
        # 图片坐标2
        logging.info("图片坐标2：%s", top_left_position)
        image.paste(overlay, top_left_position)
        
        # 保存修改后的图像
        logging.info("正在保存修改后的图像：%s", output_image_path)
        image.save(output_image_path)
        logging.info("图片已保存至：%s", output_image_path)
    except Exception as e:
        logging.exception("编辑图片时发生错误：%s", e)
        logging.error("在编辑图片时发生错误，无法完成图像编辑。")

# 加载 JSON 文件中的文本信息和位置信息
with open("../TData/pg_Servo.json", "r", encoding="utf-8") as file:
    data = json.load(file)
logging.info("JSON 文件加载成功。")  # 在加载成功后打印消息

# 按照键的顺序处理JSON数据
for key in sorted(data.keys()):
    if key.startswith("pg"):
        # 获取当前键对应的值
        parent_data = data[key]

        # 获取子集值
        text1 = parent_data["text1"]
        text2 = parent_data["text2"]
        overlay_image_path = parent_data["overlay_image_path"]
        top_left_position = tuple(parent_data["top_left_position"])
        bottom_right_position = tuple(parent_data["bottom_right_position"])

        # 打印获取到的值
        logging.info("text1：%s", text1)
        logging.info("text2：%s", text2)
        logging.info("overlay_image_path：%s", overlay_image_path)
        logging.info("top_left_position：%s", top_left_position)
        logging.info("bottom_right_position：%s", bottom_right_position)

        # 指定原始图片文件路径
        original_image_path = "..\\templet\\pgt.jpg"
        logging.info("原始图片文件路径：%s", original_image_path)

        # 检查原始图片文件是否存在
        if os.path.exists(original_image_path):
            # 获取导出图片的文件名
            export_filename = parent_data["name"]
            
            # 自定义导出路径，替换为您想要的路径和文件名
            output_folder = "..\\output"  # 指定导出文件夹路径
            os.makedirs(output_folder, exist_ok=True)  # 确保导出文件夹存在
            
            # 设置导出图片的完整路径和文件名
            output_image_path = os.path.join(output_folder, f"{export_filename}.jpg")
            logging.info("导出图片的完整路径和文件名：%s", output_image_path)
            
            # 调用函数进行图片编辑
            edit_image(original_image_path, output_image_path, text1, text2, overlay_image_path, top_left_position, bottom_right_position)
        else:
            logging.error("原始图片文件不存在。")

# 记录任务执行结束的时间
logging.info(f"{file_name}任务执行结束")
logging.info("V pg.0.8.5")
logging.info("-------------------------------------------------")

import subprocess

# 指定要运行的Python脚本路径
logging.info("开始执行下一个脚本")
next_script_path = "cz-图片修改0.8.py"

# 执行指定的Python脚本
subprocess.run(["Python", next_script_path])
