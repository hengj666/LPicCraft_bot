import os
import telepot
import urllib3
import subprocess
import time

# Bot Token 和目标 chat ID
TOKEN = '111'
TARGET_CHAT_ID = 1500662183

# 创建一个 Telepot Bot 实例
bot = telepot.Bot(TOKEN)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    # 处理文本消息
    if content_type == 'text':
        text = msg['text']
        
        # 处理命令
        if text.startswith('/'):
            command = text.split()[0]
            
            if command == '/start':
                bot.sendMessage(chat_id, '可以开始运行')
            elif command == '/help':
                bot.sendMessage(chat_id, '请将所有的的压缩包和txt文件发送给我，然后发送 /operational 命令')
            elif command == '/operational':
                # 在本地运行另一个Python脚本
                subprocess.Popen(['python', "script_file\\解压.py"])
                bot.sendMessage(chat_id, '正在执行')

                # 等待解压完成
                time.sleep(3)

                # 读取output文件夹中的文件
                output_folder = 'output'
                for filename in os.listdir(output_folder):
                    filepath = os.path.join(output_folder, filename)
                    # 发送文件给用户
                    with open(filepath, 'rb') as file:
                        bot.sendDocument(chat_id, file)

        else:
            bot.sendMessage(chat_id, '')

    # 处理文件消息
    elif content_type == 'document':
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

# 注册消息处理程序
bot.message_loop(handle)

# 发送上线消息给指定的 chat ID
bot.sendMessage(TARGET_CHAT_ID, '机器人已上线！')

print('Listening for messages...')

# 保持程序运行
while True:
    pass
