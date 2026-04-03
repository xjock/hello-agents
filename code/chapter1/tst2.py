# 使用OpenAI Python库调用Moonshot API (v1版本)
# 安装: pip install openai

from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key="sk-YaoAb3bYs3tnemLkEIvKebOBJJrKSiTzeC1BNZHvdPJgXLNt",  # 替换为你的Moonshot API Key
    base_url="https://api.moonshot.cn/v1"  # Moonshot API v1端点
)

# 发起请求
response = client.chat.completions.create(
    model="kimi-k2.5",  # 可选: moonshot-v1-8k/32k/128k
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好，请介绍一下Thought-Action模式。"}
    ],
    temperature=1
)

print(response.choices[0].message.content)