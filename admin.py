from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMINS
from states.admin_states import AddSponsor
from keyboards.admin_kb import (
    admin_panel_kb,
    delete_sponsors_kb
)
from database.sponsors import (
    add_sponsor,
    get_sponsors,
    delete_sponsor
)

router = Router()


@router.message(Command("apanel"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return

    await message.answer(
        "⚙️ Админ-панель",
        reply_markup=admin_panel_kb()
    )


@router.callback_query(F.data == "add_sponsor")
async def add_start(
    callback: CallbackQuery,
    state: FSMContext
):
    if callback.from_user.id not in ADMINS:
        return

    await state.set_state(AddSponsor.channel_id)

    await callback.message.answer(
        "Отправьте ID канала:"
    )

    await callback.answer()


@router.message(AddSponsor.channel_id)
async def get_channel_id(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        channel_id=message.text
    )

    await state.set_state(AddSponsor.channel_link)

    await message.answer(
        "Отправьте ссылку на канал:"
    )


@router.message(AddSponsor.channel_link)
async def get_link(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        channel_link=message.text
    )

    await state.set_state(AddSponsor.title)

    await message.answer(
        "Введите название кнопки:"
    )


@router.message(AddSponsor.title)
async def save_sponsor(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    await add_sponsor(
        channel_id=data["channel_id"],
        channel_link=data["channel_link"],
        title=message.text
    )

    await state.clear()

    await message.answer(
        "✅ Спонсор добавлен"
    )


@router.callback_query(F.data == "list_sponsors")
async def list_sponsors(
    callback: CallbackQuery
):
    if callback.from_user.id not in ADMINS:
        return

    sponsors = await get_sponsors()

    if not sponsors:
        await callback.answer(
            "Список пуст",
            show_alert=True
        )
        return

    text = "📋 Спонсоры:\n\n"

    for sponsor in sponsors:
        text += (
            f"ID: {sponsor[0]}\n"
            f"Название: {sponsor[3]}\n\n"
        )

    await callback.message.answer(text)

    await callback.answer()


@router.callback_query(F.data == "delete_sponsor")
async def delete_menu(
    callback: CallbackQuery
):
    if callback.from_user.id not in ADMINS:
        return

    sponsors = await get_sponsors()

    if not sponsors:
        await callback.answer(
            "Список пуст",
            show_alert=True
        )
        return

    await callback.message.answer(
        "Выберите спонсора:",
        reply_markup=delete_sponsors_kb(sponsors)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def delete_item(
    callback: CallbackQuery
):
    if callback.from_user.id not in ADMINS:
        return

    sponsor_id = int(
        callback.data.split("_")[1]
    )

    await delete_sponsor(sponsor_id)

    await callback.message.edit_text(
        "✅ Спонсор удалён"
    )

    await callback.answer()