import tkinter as tk
import requests
import json
import threading
from tkinter import font

# 设置兼容 OpenAI API 的 URL 和 API 密钥
API_KEY = 'sk-vicundfyydemqsrjiolnmitpbkjkzkbejmhlumipzuxfeviq'  # 替换为你的API密钥
API_URL = 'https://api.siliconflow.cn/v1/chat/completions'

# 创建与 OpenAI 兼容 API 的对话
def chat_with_compatible_api(message):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",  # 使用指定的模型
        "messages": [
            {"role": "user", "content": message}
        ],
        "stream": False,  # 禁用流式请求
        "max_tokens": 512,
        "stop": None,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
    }

    try:
        # 发送 POST 请求到兼容 API
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")  # 输出状态码用于调试

        if response.status_code == 200:
            result = response.json()  # 直接解析整个 JSON 响应
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content']
            else:
                return "No content in response."
        else:
            print(f"Error: {response.status_code}, {response.text}")  # 输出错误信息
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        print(f"Exception: {str(e)}")  # 输出异常
        return f"Error: {str(e)}"

# 设置图形界面
def on_send():
    user_message = user_input.get()
    if user_message.lower() in ['exit', 'quit', 'bye']:
        root.quit()
    else:
        # 清空输入框
        user_input.delete(0, tk.END)
        # 显示用户消息
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"你: {user_message}\n")
        chat_display.config(state=tk.DISABLED)

        # 启动一个新线程来处理请求
        threading.Thread(target=handle_response, args=(user_message,)).start()

# 处理 API 响应
def handle_response(user_message):
    chat_display.config(state=tk.NORMAL)  # 允许编辑聊天框
    ai_response = chat_with_compatible_api(user_message)  # 获取 AI 回复
    chat_display.insert(tk.END, f"AI: {ai_response}\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)  # 自动滚动到底部

# 创建 Tkinter 窗口
root = tk.Tk()
root.title("OpenAI 兼容 API 聊天客户端")

# 设置窗口大小和背景颜色
root.geometry("500x600")
root.configure(bg="#f0f0f0")

# 使用自定义字体
chat_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=12, weight="bold")

# 创建聊天显示框
chat_display = tk.Text(root, width=50, height=20, state=tk.DISABLED, font=chat_font, bg="#e0e0e0", wrap=tk.WORD)
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# 添加滚动条
scrollbar = tk.Scrollbar(root, command=chat_display.yview)
scrollbar.grid(row=0, column=2, sticky="ns", padx=5, pady=10)
chat_display.config(yscrollcommand=scrollbar.set)

# 创建用户输入框
user_input = tk.Entry(root, width=40, font=chat_font, bg="#ffffff", bd=2, relief="solid")
user_input.grid(row=1, column=0, padx=10, pady=10)

# 创建发送按钮
send_button = tk.Button(root, text="发送", font=button_font, bg="#4CAF50", fg="white", command=on_send, relief="raised", height=2, width=10)
send_button.grid(row=1, column=1, padx=10, pady=10)

# 运行窗口的主循环
root.mainloop()
