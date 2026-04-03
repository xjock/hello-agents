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
    messages=[{'role': 'system', 'content': '\n你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。\n\n# 可用工具:\n- `get_weather(city: str)`: 查询指定城市的实时天气。\n- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。\n\n# 输出格式要求:\n你的每次回复必须严格遵循以下格式，包含一对Thought和Action：\n\nThought: [你的思考过程和下一步计划]\nAction: [你要执行的具体行动]\n\nAction的格式必须是以下之一：\n1. 调用工具：function_name(arg_name="arg_value")\n2. 结束任务：Finish[最终答案]\n\n# 重要提示:\n- 每次只输出一对Thought-Action\n- Action必须在同一行，不要换行\n- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束\n\n请开始吧！\n'}, {'role': 'user', 'content': '用户请求: 你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。'}],
    # temperature=1
)
print(response.choices[0].message.content)

# --- 2. 初始化 ---
user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "=" * 40)

