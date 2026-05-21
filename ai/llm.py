import httpx

async def call_llm(prompt: str, system_prompt: str) -> str: 
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5",
                "prompt":f"""<SYSTEM> {system_prompt} </SYSTEM>
                <USER> {prompt} </USER>""",
                "stream": False
            },
        timeout=60.0
    )
    return res.json()["response"]

