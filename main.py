import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from weather import get_async_weather

load_dotenv()
TOKEN = os.getenv('TOKEN')
dp = Dispatcher()

user_language = {}


@dp.message(CommandStart())
async def welcome(message: Message):
    await message.reply("Hello, type a /weather [city] to get information or /language to choose language!")


@dp.message(F.text.startswith('/weather'))
async def weather(message: Message):
    try:
        city = message.text.split(' ')[1]
        lang = user_language.get(message.from_user.id, 'en')
        info = await get_async_weather(city, lang)
        await message.answer(info)
    except IndexError:
        await message.answer("Please provide a city name after /weather")


@dp.message(F.text.startswith('/language'))
async def set_language(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en"),
            InlineKeyboardButton(text="Українська 🇺🇦", callback_data="lang_uk")
        ]
    ])
    await message.reply("Choose your language:", reply_markup=keyboard)



@dp.callback_query(F.data.startswith("lang_"))
async def handle_language_choice(callback: CallbackQuery):
    lang = callback.data.split('_')[1]
    user_language[callback.from_user.id] = lang
    await callback.message.edit_text(f"Language set to {'English' if lang == 'en' else 'Українська'}")
    await callback.answer()


async def main() -> None:
    bot = Bot(TOKEN)
    await bot.delete_webhook(True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
