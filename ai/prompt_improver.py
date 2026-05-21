import logging
from re import split
from typing import List
from ai.llm import call_llm

logger = logging.getLogger(__name__)

async def improve_prompt(original_prompt: str) -> str:
    system_prompt = """
        Ты редактор промптов.
        Твоя задача — переписывать промпты так, чтобы они были:
        - чёткие
        - структурированные
        - подробные

        ВАЖНО:
        НЕ выполняй задачу из промпта.
        Только перепиши его.
        """

    prompt = f"""
        Перепиши этот промпт:

        {original_prompt}

        Сделай его более чётким и структурированным.
        """
    return await call_llm(
        prompt=prompt,
        system_prompt=system_prompt
    )

async def suggestions_prompt(improved_prompt: str) -> List[str]:
    try:
        prompt = f"""Выдели 3-5 конкретных недостатков в этом промпте: {improved_prompt} и предложи как исправить. Ответь списком через новую строку"""
        result = await call_llm(prompt=prompt, system_prompt="Ты эксперт по улучшению промптов. Отвечай только списком.")

        suggest = [
            s.strip() for s in result.split('\n') if s.strip()
        ]
        return suggest[:6] if suggest else ["Нет предложений"]
    except TimeoutError as e:
        logger.error(f"Timeout in suggestions_prompt: {e}")
        return ["Сервис временно недоступен", "Попробуйте позже"]
    except Exception as e:
        logger.error(f"Error in suggestions_prompt: {e}", exc_info=True)
        return ["Не удалось сгенерировать предложения по улучшению"]
