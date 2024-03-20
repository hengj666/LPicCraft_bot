from PIL import Image, ImageDraw, ImageFont
import os

def edit_image(input_image_path, output_image_path, text1, text2, image_path, top_left_position, bottom_right_position):
    # 打开原始图片
    print("正在打开原始图片：", input_image_path)
    image = Image.open(input_image_path)
    
    # 创建一个可以在图像上绘制的对象
    draw = ImageDraw.Draw(image)
    
    # 选择一个字体
    font = ImageFont.truetype(r"font\Adobe Std R.otf", 56)
    
    # 在图像上绘制文本1
    print("在图像上绘制文本1：", text1)
    draw.text((154, 922), text1, font=font, fill=(255, 255, 255, 255))
    
    # 保存包含文本1的图像
    print("正在保存包含文本1的图像：", output_image_path)
    image.save(output_image_path)
    print("图像已保存至：", output_image_path)
    
    # 打开保存的图像以便后续绘制文本2和添加图片
    print("重新打开已保存的图像：", output_image_path)
    image = Image.open(output_image_path)
    draw = ImageDraw.Draw(image)

    
    # 在图像上绘制文本2
    print("准备在图像上绘制文本2")
    print("在图像上绘制文本2：", text2)
    draw.text((489, 922), text2, font=font, fill=(255, 255, 255, 255))
    
    # 打开要添加的图片
    print("正在打开要添加的图片：", image_path)
    overlay = Image.open(image_path)
    
    # 计算要添加的图片的目标大小
    target_width = bottom_right_position[0] - top_left_position[0]
    target_height = bottom_right_position[1] - top_left_position[1]
    
    # 强制拉伸要添加的图片
    print("计算要添加的图片的目标大小：", (target_width, target_height))
    overlay = overlay.resize((target_width, target_height))
    
    # 在指定位置叠加图片
    print("在指定位置叠加图片：", top_left_position)
    image.paste(overlay, top_left_position)
    
    # 保存修改后的图像
    print("正在保存修改后的图像：", output_image_path)
    image.save(output_image_path)
    print("图像已保存至：", output_image_path)

# 指定输入和输出路径
input_image_path = r"I:\自动化测试\运行环境\templet\pgt.jpg"
output_image_path_with_text1 = r"I:\自动化测试\运行环境\output\pgt_with_text1.jpg"

# 绘制文本1并保存包含文本1的图像
edit_image(input_image_path, output_image_path_with_text1, "台湾075期", "", "", (0, 0), (0, 0))

# 调用函数进行图片编辑，替换参数为你想要添加的文本内容、图片路径以及位置
edit_image(output_image_path_with_text1, output_image_path_with_text1, "", "虎鸡兔     猴蛇猪", r"I:\自动化测试\运行环境\data_file\Temp_data\tk-tw-pgt.jpg", (188, 2), (778, 904))
