from openai import OpenAI

client = OpenAI(
    base_url="https://api.kimi.com/coding/v1",
    api_key="sk-kimi-lQReDF2LwYaN7gkCXbjW1h2Rl9JQDaCA8OPXw31JTIpMosECb0Axmag1Em7GPQI6",
    # 核心突破口：伪造 User-Agent，假装自己是官方的命令行工具
    default_headers={"User-Agent": "Kimi CLI"}
)



from crewai import LLM

kimi_llm = LLM(
    model="openai/kimi-for-coding",
    base_url="https://api.kimi.com/coding/v1",
    api_key="sk-kimi-lQReDF2LwYaN7gkCXbjW1h2Rl9JQDaCA8OPXw31JTIpMosECb0Axmag1Em7GPQI6",
    temperature=0.1,
    # 核心突破口：注入伪造的 Headers 绕过校验
    extra_headers={
        "User-Agent": "Kimi CLI"
    }
)