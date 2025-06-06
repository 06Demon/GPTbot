import asyncio
from aiogram import Bot, Dispatcher
import os

from app.handlers import router

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


async def main():
    print("Bot activated")

    bot = Bot(token=f"{TOKEN}")
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot disactivated")
