from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def admin_panel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Добавить спонсора",
                    callback_data="add_sponsor"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Список спонсоров",
                    callback_data="list_sponsors"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Удалить спонсора",
                    callback_data="delete_sponsor"
                )
            ]
        ]
    )


def delete_sponsors_kb(sponsors):
    keyboard = []

    for sponsor in sponsors:
        keyboard.append([
            InlineKeyboardButton(
                text=f"❌ {sponsor[3]}",
                callback_data=f"delete_{sponsor[0]}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
