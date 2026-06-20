'''Фабрика LLM клиента.
Возвращает настроенный ChatOpenAI: все параметры (base_url, api_keyб
модель, температура) подтягиваются из 'app.config.settings'. Работает 
с любым провайдером, поддерживающим API OpenRouter.
'''

from langchain_openai import ChatOpenAI
from langchain_core.caches import BaseCache  # добавить импорт
from app.config import settings

def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
    )