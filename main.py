import requests
import json

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "Qwen/Qwen2.5-32B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": "你好"
        }
    ],
    "stream": True
}

headers = {
    "Authorization": "Bearer sk-geoxrhltgamdczziqtiojkubhewxkcxbmdlhtrvxmaktplhh",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, stream=True)

if response.status_code == 200:
    full_text = ""
    for chunk in response.iter_lines():
        if chunk:
            try:
                # 解码每个返回的JSON响应部分
                message = json.loads(chunk.decode('utf-8'))
                # 获取助手的回复内容
                assistant_content = message.get('choices', [{}])[0].get('message', {}).get('content', '')
                if assistant_content:
                    full_text += assistant_content  # 拼接流式返回的文本
                    print(assistant_content, end='')  # 逐步打印
            except json.JSONDecodeError:
                print("解码错误")
else:
    print(f"请求失败，状态码：{response.status_code}")
