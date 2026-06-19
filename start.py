from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from database.sponsors import get_sponsors
from keyboards.user_kb import sponsors_kb, main_menu

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    sponsors = await get_sponsors()

    if sponsors:
        photo = FSInputFile("images/sponsors.png")

        await message.answer_photo(
            photo=photo,
            caption=(
                "🎁 Чтобы пользоваться ботом,\n"
                "подпишитесь на все каналы ниже."
            ),
            reply_markup=sponsors_kb(sponsors)
        )
    else:
        photo = FSInputFile("images/menu.png")

        await message.answer_photo(
            photo=photo,
            caption="✨ Добро пожаловать!",
            reply_markup=main_menu()
        )


@router.callback_query(F.data == "check_subs")
async def check_subs(callback: CallbackQuery, bot: Bot):
    sponsors = await get_sponsors()

    for sponsor in sponsors:
        try:
            member = await bot.get_chat_member(
                chat_id=sponsor[1],
                user_id=callback.from_user.id
            )

            if member.status in ("left", "kicked"):
                await callback.answer(
                    text="❌ Вы подписались не на все каналы.",
                    show_alert=True
                )
                return

        except Exception:
            await callback.answer(
                text="⚠️ Ошибка проверки подписки.",
                show_alert=True
            )
            return

    await callback.message.delete()

    photo = FSInputFile("images/menu.png")

    await callback.message.answer_photo(
        photo=photo,
        caption="✨ Добро пожаловать!",
        reply_markup=main_menu()
    )

    await callback.answer()