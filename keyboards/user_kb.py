from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


def sponsors_kb(sponsors):
    keyboard = []

    for sponsor in sponsors:
        keyboard.append([
            InlineKeyboardButton(
                text=sponsor[3],
                url=sponsor[2]
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="✅ Я подписался",
            callback_data="check_subs"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⭐ Заработать"),
                KeyboardButton(text="👤 Профиль")
            ],
            [
                KeyboardButton(text="🎁 Бонус"),
                KeyboardButton(text="📤 Вывод")
            ]
        ],
        resize_keyboard=True
    )
