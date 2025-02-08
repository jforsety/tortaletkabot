"""Обращение к GigaChat с помощью GigaChain"""
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from app_bot.database import profile_attempts, edit_attempts


def start_gigachat(message):
    attempt_user = profile_attempts(message)
    if attempt_user is not None:
        # Авторизация в GigaChat
        model = GigaChat(
            credentials=os.environ.get("AUTHORIZATION_KEY"),
            scope="GIGACHAT_API_PERS",
            model="GigaChat",
            # Отключает проверку наличия сертификатов НУЦ Минцифры
            verify_ssl_certs=False,
        )

        messages = [
            SystemMessage(
                content="Ты эмпатичный бот, профессионал, который помогает пользователю решить его проблемы."
            )
        ]

        user_input = message.text
        if user_input == "/reset":
            return
        messages.append(HumanMessage(content=user_input))
        res = model.invoke(messages)
        messages.append(res)
        edit_attempts(message)
        return f"{res.content}\n\nНажмите /reset, чтобы сбросить историю запросов."