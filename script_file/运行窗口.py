import os
import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess

# 检查当前工作目录是否为目标目录，如果不是则切换
if os.path.basename(os.getcwd()) != "script_file":
    try:
        os.chdir("script_file")
        print("已将工作目录更改为 'script_file'")
    except FileNotFoundError:
        print("目标目录 'script_file' 不存在！")
else:
    print("当前工作目录已经是目标目录，无需更改。")


# 创建主窗口
root = tk.Tk()

# 设置窗口大小
root.geometry("400x300")  # 设置宽度为400像素，高度为300像素

# 创建按钮1
button1 = tk.Button(root, text="开始运行", command=lambda: execute_script("解压.py"))
button1.pack()


# 执行相应的Python文件
def execute_script(script_name):
    try:
        # 使用subprocess.run执行Python文件
        subprocess.run(["python", script_name], check=True)
        # 执行成功时弹出提示框
        messagebox.showinfo("Success", f" {script_name} 运行成功!")
    except subprocess.CalledProcessError as e:
        # 执行失败时弹出提示框显示异常信息
        messagebox.showerror("Error", f"Failed to execute script {script_name}:\n{e}")

# 运行主循环
root.mainloop()
