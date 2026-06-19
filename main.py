import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database.sponsors import init_db
from handlers.start import router as start_router
from handlers.admin import router as admin_router


async def main():
    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(start_router)

    await init_db()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())