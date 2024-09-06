import os
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import urllib3
import subprocess
import time
import random
import shutil
import json
import csv
import urllib.parse

current_dir = os.getcwd()
print("当前工作目录是：", current_dir)


#def update_json_field(json_file, field_name):
#    try:
#        with open(json_file, 'r') as file:
#            data = json.load(file)
#        
#        # 将特定字段的值修改为 "no"
#        if field_name in data:
#            data[field_name] = "no"
#        
#        # 保存更新后的数据回到 JSON 文件中
#        with open(json_file, 'w') as file:
#            json.dump(data, file, indent=4)
#        
#        print(f"成功将字段 '{field_name}' 的值修改为 'no'.")
#
#    except Exception as e:
#        print(f"修改字段 '{field_name}' 的值时出现错误：{e}")
#
## 指定 JSON 文件路径和要修改的字段名
#json_file_path = "script_file\\temp_filter.json"  #  JSON 文件路径
#field_to_update = "out"     # 要修改的字段名
#
## 调用函数更新字段值
#update_json_field(json_file_path, field_to_update)

# Bot Token 和目标 chat ID
TOKEN = '111'
OWNER_CHAT_ID = 1500662183
#ALLOW_CHAT_IDS = [1500662183, 6246444066, ]
#ALLOW_USERNAMES = {'Liusy01', 'ay_6698', 'username3'}

#获取授权用户名列表
def load_usernames(filename):
    # 从 JSON 文件中读取数据
    with open(filename, 'r') as file:
        data = json.load(file)

    # 提取用户名列表
    return data.get('user', [])

# 初始加载用户名列表
ALLOW_USERNAMES = load_usernames('script_file\\usernames.json')

# 创建一个 Telepot Bot 实例
bot = telepot.Bot(TOKEN)

#获取用户信息
def user_info_exists(user_info, filename="user_info.csv"):  
    # 检查文件是否存在  
    if not os.path.isfile(filename):  
        return False  # 文件不存在，直接返回False，表示用户信息不存在  
      
    user_id = user_info.get('user_id')  # 使用get方法可以从字典中安全地获取值，如果键不存在则返回None  
    if user_id is None:  
        return False  # 如果没有用户ID，则认为用户信息不存在  
      
    with open(filename, 'r', newline='', encoding='utf-8-sig') as csv_file:  
        reader = csv.DictReader(csv_file)  
        for row in reader:  
            if row['user_id'] == user_id:  
                return True  # 找到匹配的用户ID，返回True  
    return False  # 遍历完整个文件都没有找到匹配的用户ID，返回False  
  
#处理文本消息与命令
def handle(msg):  
    ALLOW_USERNAMES = load_usernames('script_file\\usernames.json')
    content_type, chat_type, chat_id = telepot.glance(msg)  
    print(content_type, chat_type, chat_id)  
    if 'username' in msg['chat']:
        print("Username:", msg['chat']['username'])  # 打印用户的用户名
    else:
        print("用户没有提供用户名")

    #print("Message:", msg)  
      
    # 提取用户信息  
    user_info = {  
        "username": msg['from'].get('username', "Unknown"),  
        "user_id": msg['from'].get('id', "Unknown"),  # 注意这里应该获取'id'，而不是'from'['id']  
        "first_name": msg['from'].get('first_name', "Unknown"),  
        "last_name": msg['from'].get('last_name', "Unknown")  
    }  
      
    # 检查是否已经存在相同的用户信息  
    if not user_info_exists(user_info):  
        with open("user_info.csv", "a", newline='', encoding='utf-8-sig') as csv_file:  
            fieldnames = ["username", "user_id", "first_name", "last_name"]  
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  
              
            # 如果文件是空的（或者不存在），先写入标题行  
            if os.stat("user_info.csv").st_size == 0:  
                csv_writer.writeheader()  
              
            csv_writer.writerow(user_info)  # 写入用户信息  
            print("User info added to CSV.")  
    else:  
        print("User info already exists in CSV.") 

    # 获取用户名
    username = msg['from'].get('username', None)

    # 如果用户名为空，发送消息并中断
    if username is None:
        bot.sendMessage(chat_id, '抱歉，不支持空用户名的用户使用。\n请先在telegram的设置中设置你的用户名。')
        print(f"{chat_id}未提供用户名的用户")
        return


    # 鉴权：检查是否为允许的用户名
    if 'username' in msg['from'] and msg['from']['username'] in ALLOW_USERNAMES:
        print(f"{msg['from']['username']} 已授权用户")
    else:
        bot.sendMessage(chat_id, '抱歉，你无权使用此功能')
        print(msg['from']['username'], '未授权用户')
        return
    
    # 处理文本消息
    if content_type == 'text':
        text = msg['text']
        
        # 处理命令
        if text.startswith('/'):
            command = text.split()[0]
            
            if command == '/start':
                # 创建一个包含按钮的 InlineKeyboardMarkup 对象
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='运行前检查', callback_data='examine')],
                    [InlineKeyboardButton(text='开始运行', callback_data='operational')]
                ])

                # 发送消息并附带按钮
                bot.sendMessage(chat_id, '请运行检查命令', reply_markup=keyboard)

            elif command == '/help':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='重载字体文件', callback_data='font')],
                    [InlineKeyboardButton(text='重载原始图片', callback_data='image')],
                    [InlineKeyboardButton(text='清空临时文件夹', callback_data='clear')]
                ])

                # 发送消息并附带按钮
                bot.sendMessage(chat_id, 'HI,是否遇到了什么问题,请点击下方按钮解决', reply_markup=keyboard)

            elif command == '/history':
                bot.sendMessage(chat_id, '正在查找文件，大约需要20秒。\n仅保留最近7天内的20条文件。')
                # 运行脚本
                subprocess.run(['python', 'script_file\\qiniu_list.py'])

                # 读取 json 文件
                with open('script_file\\Temp Files\\qiniu_list_folder.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                # 根据数据创建消息内容
                random_number = random.randint(1, 1000000) 
                messages = []
                


                for item in data:
                    #print(item['time'], item['key'], item['private_url'])
                    message = f"{item['time']}   [{item['key']}]({item['private_url']}\n)"
                    messages.append (message)
                    #print("打印message", message)
                # 倒序排列messages列表
                messages.reverse()
                intro_message = f"以下是查找到的文件[.](http://lp.data.hengj.cn/{random_number}.ini)\n文件下载链接的有效期为5分钟，请及时下载。"  
                messages.insert(0, intro_message) 
                #print("打印messages列表", messages)
                #print('\n'.join(messages))
                messages_text = '\n'.join(messages)
                
                # 将消息内容拆分为每20行一页
                # 每页的消息数量（行数）  
                lines_per_page = 21 

                # 计算总页数  
                total_pages = len(messages) // lines_per_page + (1 if len(messages) % lines_per_page > 0 else 0)  

                # 初始化当前页码  
                current_page = 0  

                # 创建键盘标记  
                #keyboard = InlineKeyboardMarkup(inline_keyboard=[  
                #    [InlineKeyboardButton(text='下一页', callback_data='next_page')] if current_page < total_pages - 1 else []  
                #])  

                # 发送第一页消息  
                if messages:  
                    # 计算第一页的消息范围  
                    start_idx = current_page * lines_per_page  
                    end_idx = (current_page + 1) * lines_per_page  
                    page_messages = messages[start_idx:end_idx]  
                    page_text = '\n'.join(page_messages)  

                    bot.sendMessage(chat_id, page_text, parse_mode='Markdown')  

                



    # 处理文件消息  
    else:  
        # 处理文件消息
        if content_type == 'document':  # 这里添加了缩进块
            # 获取文件名
            file_name = msg['document']['file_name']
            # 获取文件拓展名
            file_extension = os.path.splitext(file_name)[1].lower()

            # 获取文件大小
            file_size = msg['document']['file_size']
            # 判断文件大小是否超过10MB
            if file_size <= 10 * 1024 * 1024:  # 10MB
            
                # 判断文件拓展名是否为支持的压缩文件格式或txt文件
                if file_extension in ['.zip', '.rar', '.7z', '.bz2', '.tar', '.gz', '.txt']:
                    # 发送“正在下载{文件名}”消息
                    download_msg = bot.sendMessage(chat_id, f"正在下载 {file_name} ...")

                    # 获取文件ID
                    file_id = msg['document']['file_id']
                    # 使用getFile方法获取文件信息
                    file_info = bot.getFile(file_id)
                    # 获取文件的相对路径
                    file_path = file_info['file_path']

                    # 获取基本网站地址
                    base_url = 'https://api.telegram.org/file/bot{}'.format(TOKEN)
                    # 构建完整的文件下载链接
                    file_url = base_url + '/' + file_path

                    # 下载文件
                    http = urllib3.PoolManager()
                    response = http.request('GET', file_url)

                    # 指定保存文件的文件夹
                    save_path = 'data_file'
                    # 指定保存文件的文件名（使用原始文件名）
                    file_name = os.path.join(save_path, msg['document']['file_name'])

                    # 保存文件
                    with open(file_name, 'wb') as f:
                        f.write(response.data)

                    # 编辑消息为“{文件名}下载成功”消息
                    bot.editMessageText((chat_id, download_msg['message_id']), f'{msg["document"]["file_name"]} 下载成功！')
                    print(f'{file_name} 下载成功！')
                else:
                    # 发送“不支持该文件格式”消息
                    bot.sendMessage(chat_id, '不支持该文件格式！')

            else:
                # 发送“压缩包文件过大”消息
                bot.sendMessage(chat_id, '压缩包文件过大，无法下载！')

#处理内联列表回调
def on_callback_query(msg):
    ALLOW_USERNAMES = load_usernames('script_file\\usernames.json')
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')  
    print('Callback Query:', query_id, from_id, query_data)

    # 获取用户名
    username = msg['from'].get('username', None)

    # 如果用户名为空，发送消息并中断
    if username is None:
        bot.sendMessage(from_id, '抱歉，不支持空用户名的用户使用。\n请先在telegram的设置中设置你的用户名。')
        print(f"{from_id}未提供用户名的用户")
        return


    # 鉴权：检查是否为允许的用户名
    if 'username' in msg['from'] and msg['from']['username'] in ALLOW_USERNAMES:
        print(f"{msg['from']['username']} 已授权用户")
    else:
        bot.sendMessage(from_id, '抱歉，你无权使用此功能')
        print(msg['from']['username'], '未授权用户')
        return

    if query_data == 'clear':
        try:
            # 清空data_file文件夹
            shutil.rmtree('data_file')
            # 重新创建空的data_file文件夹
            os.makedirs('data_file')
            # 发送处理结果给用户
            bot.sendMessage(from_id, '已清空临时文件夹')
        except Exception as e:
            # 发送错误消息给用户
            bot.sendMessage(from_id, f'清空临时文件夹时出错: {str(e)}')

    if query_data == 'font':
        try:
            # 获取data\font路径中的所有文件
            font_files = os.listdir('data\\font')

            # 将每个文件复制到.font文件夹中
            for file in font_files:
                src_path = os.path.join('data\\font', file)
                dst_path = os.path.join('.\\font', file)
                shutil.copy(src_path, dst_path)

            # 发送处理结果给用户
            bot.sendMessage(from_id, '已成功修复字体')
        except Exception as e:
            # 发送错误消息给用户
            bot.sendMessage(from_id, f'修复字体时出错: {str(e)}')

    if query_data == 'image':
        try:
            # 获取data\image路径中的所有文件
            font_files = os.listdir('data\\image')

            # 将每个文件复制到.font文件夹中
            for file in font_files:
                src_path = os.path.join('data\\image', file)
                dst_path = os.path.join('.\\templet', file)
                shutil.copy(src_path, dst_path)

            # 发送处理结果给用户
            bot.sendMessage(from_id, '已成功重载原始图片')
        except Exception as e:
            # 发送错误消息给用户
            bot.sendMessage(from_id, f'重载原始文件时出错: {str(e)}')


    if query_data == 'examine':
        try:
            # 启动子进程
            #subprocess.Popen(['python', "script_file\\temp_filter.py"])
            # 在本地运行另一个Python脚本
            process = subprocess.Popen(['python', "script_file\\temp_filter.py"])
            msg_sent = bot.sendMessage(from_id, '正在检查')
            # 等待子进程执行完成
            process.wait()
            # 子进程执行完成后，继续执行主进程的代码
            #bot.sendMessage(from_id, '检查完毕')

        except Exception as e:
            print(f"子进程发生异常：{e}")

        # 等待两秒钟
        # time.sleep(2)

        # 从指定的log文件中读取内容
        with open("temp_filter.log", "r", encoding="utf-8") as f:
            log_lines = f.readlines()

        if log_lines:
            # 获取之前发送的消息内容
            prev_msg = msg_sent['message_id']

            # 获取之前消息的文本
            prev_text = msg_sent['text']

            # 初始化新的消息文本
            new_text = prev_text

            # 初始化按钮条件
            contains_clear_keyword = False
            contains_operational_keyword = False

            # 逐行添加日志内容到新的消息文本
            for line in log_lines:
                new_text += '\n' + line.strip()
                if "清空" in line:
                    contains_clear_keyword = True
                elif "所有文件识别成功" in line:
                    contains_operational_keyword = True

            # 编辑之前发送的消息并将新的内容发送出去
            bot.editMessageText((from_id, prev_msg), new_text)

            # 生成随机等待时间，范围为0.8到2秒
            #wait_time = random.uniform(0.8, 2)
            #time.sleep(wait_time)

            # 构建键盘布局
            keyboard_buttons = []

            # 如果日志内容包含"清空"关键字，则添加一个清空操作按钮
            if contains_clear_keyword:
                clear_button = {'text': '清空临时文件夹', 'callback_data': 'clear'}
                keyboard_buttons.append([clear_button])

            # 如果日志内容包含"所有文件识别成功"，则添加一个运行按钮
            if contains_operational_keyword:
                run_button = {'text': '运行', 'callback_data': 'operational'}
                keyboard_buttons.append([run_button])

            # 如果日志内容包含任何关键字，则发送带有按钮的消息
            if keyboard_buttons:
                keyboard_layout = {'inline_keyboard': keyboard_buttons}
                bot.editMessageReplyMarkup((from_id, prev_msg), reply_markup=keyboard_layout)
            else:
                print("输出内容为空，无法发送消息循环内")
        else:
            print("输出内容为空，无法发送消息")



    elif query_data == 'operational':  
        # 读取 JSON 文件
        with open("script_file\\temp_filter.json", "r") as json_file:
            data = json.load(json_file)     

        # 获取 out 字段的值
        out_value = data.get("out")     

        print("原始 data 字典:", data)

#        # 根据 out 字段的值执行不同的动作
#        if out_value == "yes":
#            # 在本地运行另一个Python脚本
#            process = subprocess.Popen(['python', "script_file\\解压.py"])
#            download_msg = bot.sendMessage(from_id, '已开始运行,大约需要20秒')
#            # 等待子进程执行完成
#            process.wait()
#            # 子进程执行完成后，继续执行主进程的代码
#            #bot.sendMessage(from_id, '已完成')
#            bot.editMessageText((from_id, download_msg['message_id']), f'运行成功！')
#            # 等待操作完成
#            #time.sleep(2)
#            # 读取output文件夹中的文件并发送给用户
#            output_folder = 'output'
#            for filename in os.listdir(output_folder):
#                filepath = os.path.join(output_folder, filename)
#                with open(filepath, 'rb') as file:
#                    bot.sendDocument(from_id, file)

        
        if out_value == "yes":
            # 在本地运行另一个Python脚本
            process = subprocess.Popen(['python', "script_file\\解压.py"])
            download_msg = bot.sendMessage(from_id, '已开始运行,大约需要20秒')
            # 等待子进程执行完成
            process.wait()
            
            # 判断 output 文件夹中是否存在文件
            output_folder = 'output'
            if any(os.listdir(output_folder)):
                # 如果存在文件，则发送文件给用户
                bot.editMessageText((from_id, download_msg['message_id']), f'运行成功！发送文件中...')
                for filename in os.listdir(output_folder):
                    filepath = os.path.join(output_folder, filename)
                    with open(filepath, 'rb') as file:
                        bot.sendDocument(from_id, file)
            else:
                # 如果不存在文件，则发送 error.txt 文件的内容给用户
                error_file_path = "script_file\error.txt"
                if os.path.exists(error_file_path):
                    with open(error_file_path, "r", encoding='utf-8') as error_file:
                        error_message = error_file.read()
                        bot.editMessageText((from_id, download_msg['message_id']), f'运行失败！\n\n{error_message}')
                else:
                    bot.editMessageText((from_id, download_msg['message_id']), '运行失败！未找到错误信息。')

                    
            process = subprocess.Popen(['python', "script_file\\upload_to_qiniu.py"])
            process.wait()
            print('-----------------------------------------------')
            print('运行完成。')
            print('-----------------------------------------------')
            print('等待后续命令，请保持窗口在后台运行！！！！！\n' * 5)

            # 修改 JSON 文件中的 "out" 字段值为 "no"  
            data["out"] = "no"   

        elif out_value == "no":
            # 发送“请先执行运行前检查”，附带运行前检查的按钮
            keyboard = {'inline_keyboard': [[{'text': '运行前检查', 'callback_data': 'examine'}]]}
            bot.sendMessage(from_id, '请先执行运行前检查', reply_markup=keyboard)
        elif out_value == "error":
            # 发送“运行前检查出现错误”，附带清空临时文件夹按钮
            keyboard = {'inline_keyboard': [[{'text': '清空临时文件夹', 'callback_data': 'clear'}]]}
            bot.sendMessage(from_id, '运行前检查出现错误', reply_markup=keyboard)
              
        # 将修改后的数据写回到 JSON 文件中  
        json_file_path = "script_file\\temp_filter.json"  
        try:  
            with open(json_file_path, "w", encoding="utf-8") as json_file:  
                json.dump(data, json_file, ensure_ascii=False, indent=4)  
            print("数据已成功写入文件")  
        except Exception as e:  
            print(f"写入文件时发生错误: {e}") 

 
#def user_info_exists(user_info, filename="user_info.csv"):  
#    user_id = user_info['user_id']  
#    with open(filename, 'r', newline='', encoding='utf-8-sig') as csv_file:  
#        reader = csv.DictReader(csv_file)  
#        for row in reader:  
#            if row['user_id'] == user_id:  
#                return True  
#    return False

# 注册消息处理程序
bot.message_loop({'chat': handle, 'callback_query': on_callback_query})

# 发送上线消息给指定的 chat ID
bot.sendMessage(OWNER_CHAT_ID, '机器人已上线！')

print('启动成功，请保持当前窗口在后台运行！！！！！\n' * 5)

# 保持程序运行
while True:
    pass
