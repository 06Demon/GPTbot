import asyncio
import os
from aiogram import Bot, Dispatcher

from app.handlers import router

with open("app/.venv", "r") as file:
    TOKEN = file.readline()


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
