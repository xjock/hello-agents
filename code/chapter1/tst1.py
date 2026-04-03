from openai import OpenAI

client = OpenAI(
    api_key="sk-YaoAb3bYs3tnemLkEIvKebOBJJrKSiTzeC1BNZHvdPJgXLNt",
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[
        {"role": "system",
         "content": "You are Kimi, an AI assistant provided by Moonshot AI. You are proficient in Chinese and English conversations. You provide users with safe, helpful, and accurate answers. You will reject any requests involving terrorism, racism, or explicit content. Moonshot AI is a proper noun and should not be translated."},
        {"role": "user", "content": "Hello, my name is Li Lei. What is 1+1?"}
    ]
)

# We receive a response from the Kimi large language model via the API (role=assistant)
print(completion.choices[0].message.content)

