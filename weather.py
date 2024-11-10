import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OW_API")
def get_weather(city_name, api_key=API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return f"Weather: {weather}, Temperature: {temperature}°C, Humidity: {humidity}%"
    else:
        return "Error retrieving weather data"
