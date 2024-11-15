import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from aiogram.utils.i18n import I18n, gettext as _
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
from weather import get_async_weather

load_dotenv()
TOKEN = os.getenv('TOKEN')
dp = Dispatcher()


i18n = I18n(path="locales", default_locale="en", domain="messages")
dp.message.middleware(SimpleI18nMiddleware(i18n))

user_language = {}


@dp.message(CommandStart())
async def welcome(message: Message):
    lang = user_language.get(message.from_user.id, 'en')
    i18n.ctx_locale.set(lang)
    print(f"Language set to {lang} for user {message.from_user.id}")
    await message.reply(_("Hello, type a /weather [city] to get information or /language to choose language!"))


@dp.message(F.text.startswith('/weather'))
async def weather(message: Message):
    try:
        city = message.text.split(' ')[1]
        lang = user_language.get(message.from_user.id, 'en')
        i18n.ctx_locale.set(lang)
        info = await get_async_weather(city, lang)
        await message.answer(info)
    except IndexError:
        await message.answer(_("Please provide a city name after /weather"))



@dp.message(F.text.startswith('/language'))
async def set_language(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en"),
            InlineKeyboardButton(text="Українська 🇺🇦", callback_data="lang_uk")
        ]
    ])
    await message.reply(_("Choose your language:"), reply_markup=keyboard)



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
