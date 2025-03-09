import pytest
import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message, Chat, User
from aiogram.enums import ChatType

# Замените 'app_bot.main' на реальное имя вашего модуля
from app_bot.main import (
    cmd_start,
    check_sub_channel,
    add_user,
    referral_reg,
    start_text,
    not_sub_message,
    check_sub_menu,
    bot
)


@pytest.fixture
def message_factory():
    """Фабрика для создания моков сообщений"""

    def _factory(text: str = "/start"):
        mock_message = MagicMock(
            spec=Message,
            message_id=1,
            date=datetime.now(),
            chat=Chat(
                id=123,
                type=ChatType.PRIVATE,
                title="Test Chat",
                username="test_chat"
            ),
            from_user=User(
                id=456,
                is_bot=False,
                first_name="Test",
                username="test_user",
                language_code="en"
            ),
            text=text,
            reply_markup=None,
            entities=[],
            message_thread_id=None,
            is_topic_message=None,
            new_chat_members=None,
            left_chat_member=None,
            forum_topic_created=None,
            forum_topic_closed=None,
            forum_topic_reopened=None,
            has_media_spoiler=None,
            media_group_id=None
        )
        mock_message.answer = AsyncMock()
        return mock_message

    return _factory


@pytest.mark.asyncio
async def test_cmd_start_user_not_subscribed(message_factory):
    """Тест: пользователь не подписан на канал"""
    message = message_factory()

    with (
        patch("app_bot.main.check_sub_channel", return_value=False),
        patch.object(bot, "get_chat_member", AsyncMock()),  # Мокаем вызов к API Telegram
        patch("os.environ.get", return_value="TEST_CHANNEL_ID")  # Мокаем переменные окружения
    ):
        await cmd_start(message)

        message.answer.assert_awaited_once_with(
            not_sub_message,
            reply_markup=check_sub_menu
        )
        # Проверяем что get_chat_member вызывался с правильными параметрами
        bot.get_chat_member.assert_awaited_once_with(
            chat_id="TEST_CHANNEL_ID",
            user_id=message.from_user.id
        )


@pytest.mark.asyncio
async def test_cmd_start_subscribed_no_referral(message_factory):
    """Тест: пользователь подписан, нет реферала"""
    message = message_factory()

    with (
        patch("app_bot.main.check_sub_channel", return_value=True),
        patch("app_bot.main.add_user") as mock_add_user,
        patch.object(bot, "get_chat_member", AsyncMock())
    ):
        await cmd_start(message)

        mock_add_user.assert_called_once_with(message)
        message.answer.assert_awaited_once_with(start_text)


@pytest.mark.asyncio
async def test_cmd_start_with_valid_referral(message_factory):
    """Тест: валидный реферальный ID"""
    message = message_factory(text="/start ref_123")

    with (
        patch("app_bot.main.check_sub_channel", return_value=True),
        patch("app_bot.main.add_user"),
        patch("app_bot.main.referral_reg") as mock_referral_reg,
        patch.object(bot, "get_chat_member", AsyncMock())
    ):
        await cmd_start(message)

        mock_referral_reg.assert_called_once_with(message, "123")


@pytest.mark.asyncio
async def test_cmd_start_with_invalid_referral(message_factory):
    """Тест: невалидный реферальный ID"""
    message = message_factory(text="/start ref_abc")

    with (
        patch("app_bot.main.check_sub_channel", return_value=True),
        patch("app_bot.main.add_user"),
        patch("app_bot.main.referral_reg") as mock_referral_reg,
        patch.object(bot, "get_chat_member", AsyncMock())
    ):
        await cmd_start(message)

        mock_referral_reg.assert_not_called()