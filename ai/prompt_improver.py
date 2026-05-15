from ai.llm import call_llm


SUGGESTIONS_PROMPT = """Выдели 3-5 конкретных недостатков в этом промпте: {original_prompt} и предложи как исправить. Ответь списком через новую строку"""

async def improve_prompt(original_prompt: str):
    return await call_llm(
        prompt=original_prompt,
        system_prompt=f"""Перепиши следующий промпт, чтобы он был более четким, структурированным и детальным. 

НЕ ОТВЕЧАЙ НА ПРОМПТ. НЕ ВЫПОЛНЯЙ ЗАДАЧУ ИЗ ПРОМПТА. Просто улучши формулировку.

Исходный промпт: {original_prompt}

Улучшенный промпт:"""
    )

async def suggestions_prompt(original_prompt: str):
    return await improve_prompt(
        original_prompt=f"""Выдели 3-5 конкретных недостатков в этом промпте: {original_prompt} и предложи как исправить. Ответь списком через новую строку"""
    )
