import tkinter as tk
import socket

def submit():
    difficulty = difficulty_var.get()
    keywords = keywords_entry.get().split(',')
    start_problem = start_var.get()
    end_problem = end_var.get()
    
    # 如果没有输入起始题号，默认为最大区间
    if not start_problem:
        start_problem = "1000"
    # 如果没有输入结束题号，默认为最大区间
    if not end_problem:
        end_problem = "1049"
    
    # 验证起始题号不能大于结束题号
    if start_problem and end_problem and int(start_problem) > int(end_problem):
        result_label.config(text="起始题号不能大于结束题号")
        return
    
    # 如果起始题号大于结束题号，显示错误消息并返回
    if int(start_problem) > int(end_problem):
        result_label.config(text="起始题号不能大于结束题号")
        return
    
    if int(end_problem)-int(start_problem)+1 > 100:
        result_label.config(text="最大查询100条记录，请重新输入范围")
        return
    
        # 准备要发送的数据，包括起始和结束题号
    data_to_send = {
        "难度": difficulty,
        "关键词": ', '.join(keywords),
        "起始题号": start_problem,
        "结束题号": end_problem
    }

    # 创建客户端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 服务器地址和端口
    server_address = ('localhost', 12345)

    try:
        # 连接服务器
        client_socket.connect(server_address)

        # 发送数据给服务器
        client_socket.send(str(data_to_send).encode('utf-8'))

        # 接收服务器的响应
        response = client_socket.recv(1024)  # 接收最多1024字节的数据

        result_label.config(text="若提交按钮重新亮起则已完成收集，请查看您的工作目录文件夹")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        # 关闭套接字
        client_socket.close()

# 创建主窗口
window = tk.Tk()
window.title("洛谷题目筛选器")

# 创建难度选择部件
difficulty_label = tk.Label(window, text="选择题目难度：(默认为全选)")
difficulty_label.grid(row=0, column=0)

difficulty_var = tk.StringVar()
difficulty_var.set("")  # 默认选择入门
difficulty_menu = tk.OptionMenu(window, difficulty_var, "","暂无评定","入门", "普及-", "普及/提高−", "普及+/提高", "提高+/省选−", "省选/NOI−", "NOI/NOI+/CTSC")
difficulty_menu.grid(row=0, column=1)

# 创建关键词输入部件
keywords_label = tk.Label(window, text="输入关键词（如算法/来源/标题/题目编号等，用逗号分隔）：")
keywords_label.grid(row=1, column=0)

keywords_entry = tk.Entry(window)
keywords_entry.grid(row=1, column=1)

# 创建起始题号输入部件
start_label = tk.Label(window, text="起始题号：")
start_label.grid(row=2, column=0)

start_var = tk.StringVar()
start_entry = tk.Entry(window, textvariable=start_var, validate="key")
start_entry.grid(row=2, column=1)

# 创建结束题号输入部件
end_label = tk.Label(window, text="结束题号：")
end_label.grid(row=3, column=0)

end_var = tk.StringVar()
end_entry = tk.Entry(window, textvariable=end_var, validate="key")
end_entry.grid(row=3, column=1)

# 创建提交按钮
submit_button = tk.Button(window, text="提交", command=submit)
submit_button.grid(row=4, columnspan=2)

# 创建结果标签
result_label = tk.Label(window, text="")
result_label.grid(row=5, columnspan=2)

# 启动Tkinter事件循环
window.mainloop()
