import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message, Chat, User
from aiogram.enums import ChatType

from app_bot.main import (
    cmd_instruction,
    get_referral_keyboard,
    check_sub_channel,
    instruction_text,
    not_sub_message,
    check_sub_menu,
    bot
)


@pytest.fixture
def message_factory():
    """Фабрика для создания моков сообщений"""

    def _factory(chat_type: ChatType = ChatType.PRIVATE, text: str = "/instruction"):
        return MagicMock(
            spec=Message,
            message_id=1,
            date=datetime.now(),
            chat=Chat(
                id=123,
                type=chat_type,
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
            answer=AsyncMock()
        )

    return _factory


@pytest.mark.asyncio
async def test_cmd_instruction_user_not_subscribed(message_factory):
    """Тест: пользователь не подписан в приватном чате"""
    message = message_factory()

    with (
        patch("app_bot.main.check_sub_channel", return_value=False),
        patch("os.environ.get", side_effect=lambda x: "MOCK_CHANNEL_ID" if x == "CHANNEL_ID" else "BOT_URL"),
        patch.object(bot, "get_chat_member", AsyncMock())
    ):
        await cmd_instruction(message)

        bot.get_chat_member.assert_awaited_once_with(
            chat_id="MOCK_CHANNEL_ID",
            user_id=456  # ID пользователя из message_factory
        )
        message.answer.assert_awaited_once_with(
            not_sub_message,
            reply_markup=check_sub_menu
        )


@pytest.mark.asyncio
async def test_cmd_instruction_subscribed(message_factory):
    """Тест: пользователь подписан в приватном чате"""
    message = message_factory()

    with (
        patch("app_bot.main.check_sub_channel", return_value=True),
        patch("os.environ.get", side_effect=lambda x: "MOCK_CHANNEL_ID" if x == "CHANNEL_ID" else "BOT_URL"),
        patch("app_bot.main.get_referral_keyboard") as mock_keyboard,
        patch.object(bot, "get_chat_member", AsyncMock())
    ):
        await cmd_instruction(message)

        mock_keyboard.assert_called_once_with(
            user_id=456,  # ID пользователя из message_factory
            bot_url="BOT_URL"
        )
        message.answer.assert_awaited_once_with(
            instruction_text,
            reply_markup=mock_keyboard.return_value
        )


@pytest.mark.asyncio
async def test_cmd_instruction_non_private_chat(message_factory):
    """Тест: не приватный чат"""
    message = message_factory(chat_type=ChatType.GROUP)

    with (
        patch("app_bot.main.check_sub_channel") as mock_check,
        patch("os.environ.get", return_value="MOCK_CHANNEL_ID"),
        patch.object(bot, "get_chat_member", AsyncMock()),
        patch.object(message, "answer", new_callable=AsyncMock)
    ):
        await cmd_instruction(message)

        mock_check.assert_not_called()
        bot.get_chat_member.assert_not_called()
        message.answer.assert_not_called()