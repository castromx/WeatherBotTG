import os
import aiohttp
from dotenv import load_dotenv
from aiogram.utils.i18n import gettext as _

load_dotenv()

API_KEY = os.getenv("OW_API")


async def get_async_weather(city_name, lang='en', api_key=API_KEY):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang={lang}"
        data = await session.get(url)
        if data.status == 200:
            data = await data.json()
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            return _(f"Weather: {weather}, Temperature: {temperature}°C, Humidity: {humidity}%")
        else:
            return _("Error retrieving weather data")
