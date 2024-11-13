import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
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
    await message.reply(_("welcome"))


@dp.message(F.text.startswith('/weather'))
async def weather(message: Message):
    try:
        city = message.text.split(' ')[1]
        lang = user_language.get(message.from_user.id, 'en')
        i18n.ctx_locale.set(lang)
        info = await get_async_weather(city, lang)
        await message.answer(info)
    except IndexError:
        await message.answer(_("enter_city"))


@dp.message(F.text.startswith('/language'))
async def set_language(message: Message):
    try:
        lang = message.text.split(' ')[1]
        if lang in ['en', 'uk']:
            user_language[message.from_user.id] = lang
            i18n.ctx_locale.set(lang)
            await message.reply(_("language_set"))
        else:
            await message.reply(_("available_languages"))
    except IndexError:
        await message.reply(_("provide_language_code"))


async def main() -> None:
    bot = Bot(TOKEN)
    await bot.delete_webhook(True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
