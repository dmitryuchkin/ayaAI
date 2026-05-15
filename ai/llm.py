import httpx

async def call_llm(prompt: str, system_prompt: str): 
    final_prompt = prompt
    if system_prompt: 
        final_prompt = f"{system_prompt}\n\n{prompt}"
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5",
                "prompt": final_prompt,
                "stream": False
            },
        timeout=60.0
    )
    return res.json()["response"]

