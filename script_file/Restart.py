import tkinter as tk  
import random  
from threading import Timer  
import subprocess  
import os

print(f"当前工作目录:", os.getcwd())

# 检查当前工作目录是否为目标目录，如果不是则切换
if os.path.basename(os.getcwd()) != "script_file":
    try:
        os.chdir("script_file")
        print("已将工作目录更改为 'script_file'")
    except FileNotFoundError:
        print("目标目录 'script_file' 不存在！")
else:
    print("当前工作目录已经是目标目录，无需更改。")
  
def close_window(window):  
    """关闭窗口的函数"""  
    if window.winfo_exists():  
        window.destroy()  
  
def run_new_script():  
    """执行新的Python脚本"""  
    subprocess.run(["python", "..\\LPicCraft.py"], check=True)  
  
def create_waiting_popup():  
    """创建无边框等待提示框"""  
    root = tk.Tk()  
    root.overrideredirect(True)  
    root.configure(bg='white')  
  
    # 设置窗口的大小  
    window_width = 200  
    window_height = 100  
  
    # 居中窗口  
    screen_width = root.winfo_screenwidth()  
    screen_height = root.winfo_screenheight()  
    x_coordinate = (screen_width - window_width) // 2  
    y_coordinate = (screen_height - window_height) // 2  
    root.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')  
  
    # 创建Canvas并添加一个旋转的圆圈（此部分代码与之前的示例相同）  
    canvas = tk.Canvas(root, bg='white', highlightthickness=0)  
    canvas.pack(fill=tk.BOTH, expand=True)  
      
    angle = 0  # 初始化角度变量
    def animate_circle(angle):  
        """更新圆圈的动画"""  
        canvas.delete("arc")  # 删除旧的弧线  
        x = canvas.winfo_width() // 2  
        y = canvas.winfo_height() // 2  
        radius = min(x, y) - 10  # 确保弧线适应窗口大小  
        canvas.create_arc(x - radius, y - radius, x + radius, y + radius,  
                          start=angle, extent=270, style="arc", tags="arc")  
        # 更新角度并重新调用animate_circle  
        new_angle = (angle + 10) % 360  
        root.after(100, animate_circle, new_angle)  # 使用root.after来递归调用  
  
    # 开始动画，传入初始角度  
    animate_circle(angle)  
  
    # 添加标签  
    label = tk.Label(root, text="正在重启...", font=("Helvetica", 16), bg='white')  
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  
  
    # 显示窗口  
    root.deiconify()  
  
    # 设置定时器在随机时间后关闭窗口，并再等待0.5秒后执行新脚本  
    delay = random.uniform(2, 5)  
    Timer(delay, lambda: close_window(root)).start()  
    Timer(delay + 0.5, run_new_script).start()  
  
    # 启动Tkinter事件循环  
    root.mainloop()  
  
if __name__ == "__main__":  
    create_waiting_popup()