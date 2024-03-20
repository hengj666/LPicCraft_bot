import tkinter as tk  
from tkinter import messagebox  
  
def show_popup(message):  
    # 创建一个隐藏的Tk窗口实例  
    root = tk.Tk()  
    root.withdraw()  # 隐藏主窗口  
  
    # 显示消息框  
    messagebox.showinfo("提示", message)  
  
    # 销毁Tk窗口实例  
    root.destroy()  
  
# 自定义你的消息内容  
custom_message = "按钮触发成功！"  
  
# 调用函数显示提示框  
show_popup(custom_message)