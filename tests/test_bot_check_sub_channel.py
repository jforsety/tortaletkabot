import pytest
from unittest.mock import Mock

from app_bot.main import check_sub_channel


@pytest.mark.parametrize(
    "status, expected",
    [
        ("member", True),
        ("administrator", True),
        ("creator", True),
        ("restricted", True),
        ("left", False),
        ("kicked", True),  # Проверяем, что функция возвращает True, если статус не 'left'
    ],
)
def test_check_sub_channel(status, expected):
    chat_member = Mock()
    chat_member.status = status
    assert check_sub_channel(chat_member) == expected