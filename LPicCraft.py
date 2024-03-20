import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMessageBox, QTextEdit, QCheckBox
from PyQt5.QtCore import Qt, QPoint, QTimer
import subprocess
import json  
from PyQt5.QtGui import QFont

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 添加标题标签
        self.title_label = QLabel("LPicCraft", self)
        self.title_label.setGeometry(20, 15, 200, 30)
        font = QFont("Arial", 18)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: black; background-color: transparent;")

        # 添加最小化按钮和关闭按钮
        self.minimize_button = QPushButton("", self)
        self.minimize_button.setGeometry(700, 15, 30, 30)
        self.minimize_button.setStyleSheet("background-color: transparent; border-image: url(font/icon/Minimize-2.png);")
        self.minimize_button.clicked.connect(self.parent.showMinimized)

        self.close_button = QPushButton("", self)
        self.close_button.setGeometry(750, 15, 30, 30)
        self.close_button.setStyleSheet("background-color: transparent; border-image: url(font/icon/Shut down-2.png);")
        self.close_button.clicked.connect(self.parent.close)

        self.setStyleSheet("background-color: #34495e;")
        self.setFixedHeight(50)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.parent.offset)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.offset = QPoint()
        self.log_file_path = "temp_filter.log"  # 日志文件路径
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_log)
        self.timer.start(1000)  # 每1000毫秒（1秒）触发一次更新
        self.colorize_checkbox_state = False  # 记录勾选框状态

    def init_ui(self):  
        self.setWindowFlags(Qt.FramelessWindowHint)  
        self.setWindowTitle('My First PyQt5 App')  
        self.setGeometry(300, 300, 800, 590)  
  
        # 添加自定义标题栏  
        self.title_bar = TitleBar(self)  

        # 创建日志框
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setGeometry(15, 405, 500, 170)
        self.log_text_edit.setReadOnly(True)  # 设置为只读
        self.log_text_edit.setStyleSheet("background-color: white; color: black; font-family: Courier; font-size: 18px;")  # 设置样式

        # 创建一个按钮并设置其点击事件处理函数  
        self.button = QPushButton('开始运行', self)  
        self.button.setGeometry(100, 30, 100, 30)  
        self.button.clicked.connect(self.run_script) 

        # 创建一个勾选框和相关的文字描述
        self.colorize_checkbox = QCheckBox("根据关键词着色", self)
        self.colorize_checkbox.setGeometry(100, 80, 200, 30)
        self.colorize_checkbox.stateChanged.connect(self.toggle_colorize)

        # 创建一个勾选框和相关的文字描述
        self.colorize_checkbox = QCheckBox("根据关键词着色", self)
        self.colorize_checkbox.setGeometry(100, 80, 200, 30)
        self.colorize_checkbox.stateChanged.connect(self.toggle_colorize)

    def run_script(self):  
        # 在日志框中记录日志
        self.log_text_edit.append("开始运行脚本...")

        # 读取和解析JSON文件  
        try:  
            with open('script_file/temp_filter.json', 'r') as file:  
                data = json.load(file)  
                out_value = data.get('out', '')  
  
                # 根据"out"字段的值来决定后续操作  
                if out_value == 'yes':  
                    subprocess.run(["python", "script_file\\解压.py"])  
                    self.log_text_edit.append("脚本运行完成。")
                elif out_value == 'no':  
                    QMessageBox.warning(self, '警告', '请先完成文件筛选再进行后续操作。')  
                elif out_value == 'error':  
                    QMessageBox.critical(self, '错误', '文件筛选中出现错误，请先处理错误信息。')  
                else:  
                    self.log_text_edit.append("初始化信息错误，可能是在程序自动检测文件时被意外中断，请尝试重启软件。")

        except FileNotFoundError:  
            QMessageBox.critical(self, '错误', '无法找到JSON文件，请确保文件路径正确。')  

    def update_log(self):
        # 读取日志文件内容并显示在日志框中
        try:
            with open(self.log_file_path, 'r') as log_file:
                log_content = log_file.read()
                self.log_text_edit.setPlainText(log_content)
        except FileNotFoundError:
            self.log_text_edit.setPlainText("日志文件不存在或路径错误。")

        # 将滚动条滚动到最后一行
        self.log_text_edit.verticalScrollBar().setValue(self.log_text_edit.verticalScrollBar().maximum())

    def toggle_colorize(self, state):
        if state == Qt.Checked:
            self.colorize_checkbox_state = True
        else:
            self.colorize_checkbox_state = False

    def update_log(self):
        # 读取日志文件内容并显示在日志框中
        try:
            with open(self.log_file_path, 'r') as log_file:
                log_content = log_file.read()
                self.log_text_edit.setPlainText(log_content)
        except FileNotFoundError:
            self.log_text_edit.setPlainText("日志文件不存在或路径错误。")

        # 如果勾选框处于勾选状态，则进行着色判断
        if self.colorize_checkbox_state:
            self.colorize_log_text()

    def colorize_log_text(self):
        keyword_colors = {
            "成功": "green",
            "失败": "red",
            "错误": "red",
            "较少": "orange"
        }
        text = self.log_text_edit.toPlainText()
        for keyword, color in keyword_colors.items():
            text = text.replace(keyword, f'<font color="{color}">{keyword}</font>')
        self.log_text_edit.setHtml(text)

# 主函数  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    my_app = MyApp()  
    my_app.show()  
    sys.exit(app.exec_())
