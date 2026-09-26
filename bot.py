import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LAT = 52.557085
LON = 103.888251

def get_weather():
    # Добавили параметр hourly=temperature_2m,weathercode для почасового прогноза
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&hourly=temperature_2m,weathercode&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Irkutsk"
    response = requests.get(url).json()
    
    current = response['current_weather']
    daily = response['daily']
    hourly = response['hourly']
    
    weather_codes = {
        0: "Ясно ☀️", 1: "Преимущественно ясно 🌤", 2: "Переменная облачность ⛅", 3: "Пасмурно ☁️",
        45: "Туман 🌫", 48: "Изморозь 🌫",
        51: "Легкая морось 🌦", 53: "Морось 🌦", 55: "Сильная морось 🌧",
        61: "Небольшой дождь 🌧", 63: "Дождь 🌧", 65: "Сильный дождь 🌧",
        71: "Небольшой снег 🌨", 73: "Снег 🌨", 75: "Сильный снег ❄️",
        80: "Небольшой ливень 🌦", 81: "Ливень 🌧", 82: "Сильный ливень 🌧",
        95: "Гроза ⛈", 96: "Гроза с градом ⛈", 99: "Сильная гроза с градом ⛈"
    }
    
    desc_now = weather_codes.get(current['weathercode'], "Неизвестно 🌡")
    
    # Формируем почасовой прогноз на ключевые часы дня
    target_hours = ["T09:00", "T12:00", "T15:00", "T18:00", "T21:00"]
    hourly_forecast = []
    
    for t in target_hours:
        # Ищем индекс нужного часа в массиве данных (например, "2023-10-27T09:00")
        idx = next((i for i, time_str in enumerate(hourly['time']) if t in time_str), None)
        if idx is not None:
            temp = hourly['temperature_2m'][idx]
            code = hourly['weathercode'][idx]
            desc = weather_codes.get(code, "Неизвестно 🌡")
            hour_str = t.replace("T", "") # Превращаем "T09:00" в "09:00"
            hourly_forecast.append(f"   🕒 {hour_str} — {temp}°C, {desc}")
            
    hourly_text = "\n".join(hourly_forecast)
    
    # Собираем итоговое сообщение
    message = (
        f"🌤 *Погода в Ангарске*\n\n"
        f"🌡 *Сейчас:* {current['temperature']}°C, {desc_now}\n"
        f"💨 *Ветер:* {current['windspeed']} км/ч\n\n"
        f"📊 *Прогноз на день:*\n{hourly_text}\n\n"
        f"📈 *Днем до:* {daily['temperature_2m_max'][0]}°C\n"
        f"📉 *Ночью до:* {daily['temperature_2m_min'][0]}°C"
    )
    return message

if __name__ == "__main__":
    message = get_weather()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=params)
    print("Результат отправки:", response.json())
