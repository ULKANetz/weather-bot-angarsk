import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LAT = 52.557085
LON = 103.888251

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Irkutsk"
    response = requests.get(url).json()
    
    current = response['current_weather']
    daily = response['daily']
    
    weather_codes = {
        0: "Ясно ☀️", 1: "Преимущественно ясно 🌤", 2: "Переменная облачность ⛅", 3: "Пасмурно ☁️",
        45: "Туман 🌫", 61: "Небольшой дождь 🌧", 63: "Дождь 🌧", 71: "Небольшой снег 🌨", 
        75: "Сильный снег ❄️", 95: "Гроза ⛈"
    }
    desc = weather_codes.get(current['weathercode'], "Неизвестно 🌡")
    
    message = (
        f"🌤 *Погода в Ангарске*\n\n"
        f"🌡 Сейчас: {current['temperature']}°C, {desc}\n"
        f"💨 Ветер: {current['windspeed']} км/ч\n"
        f"📈 Днем до: {daily['temperature_2m_max'][0]}°C\n"
        f"📉 Ночью до: {daily['temperature_2m_min'][0]}°C"
    )
    return message

if __name__ == "__main__":
    message = get_weather()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(url, json=params)
    print("Результат отправки:", response.json())
