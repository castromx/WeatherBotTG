import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from weather import get_weather

load_dotenv()

TOKEN = os.getenv('TOKEN')

dp = Dispatcher()


@dp.message(CommandStart())
async def welcome(message: Message):
    await message.reply("Hello, type a /weather [city] for got information!")


@dp.message(F.text.startswith('/weather'))
async def weather(message: Message):
    try:
        city = message.text.split(' ')[1]
        info = get_weather(city)
        await message.answer(info)
    except IndexError:
        await message.answer("Please provide a city name after /weather")

async def main() -> None:
    bot = Bot(TOKEN)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())