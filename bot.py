import os
import requests
import schedule
import time
from dotenv import load_dotenv

# 1. Загружаем настройки из файла .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 2. Координаты Ангарска из вашей ссылки
LAT = 52.557085
LON = 103.888251

def get_weather():
    """Получает данные о погоде по координатам"""
    try:
        # Бесплатный API, не требует ключа, использует часовую зону Иркутска
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Irkutsk"
        response = requests.get(url).json()
        
        current = response['current_weather']
        daily = response['daily']
        
        temp = current['temperature']
        wind = current['windspeed']
        max_temp = daily['temperature_2m_max'][0]
        min_temp = daily['temperature_2m_min'][0]
        code = current['weathercode']
        
        # Расшифровка кодов погоды (WMO)
        weather_codes = {
            0: "Ясно ☀️", 1: "Преимущественно ясно 🌤", 2: "Переменная облачность ⛅", 3: "Пасмурно ☁️",
            45: "Туман 🌫", 48: "Изморозь 🌫",
            51: "Легкая морось 🌦", 53: "Морось 🌦", 55: "Сильная морось 🌧",
            61: "Небольшой дождь 🌧", 63: "Дождь 🌧", 65: "Сильный дождь 🌧",
            71: "Небольшой снег 🌨", 73: "Снег 🌨", 75: "Сильный снег ❄️",
            80: "Небольшой ливень 🌦", 81: "Ливень 🌧", 82: "Сильный ливень 🌧",
            95: "Гроза ⛈", 96: "Гроза с градом ⛈", 99: "Сильная гроза с градом ⛈"
        }
        desc = weather_codes.get(code, "Неизвестно 🌡")

        # Формируем красивое сообщение с поддержкой Markdown
        message = (
            f"🌤 *Погода в Ангарске на сегодня*\n\n"
            f"🌡 Сейчас: {temp}°C, {desc}\n"
            f"💨 Ветер: {wind} км/ч\n"
            f"📈 Днем до: {max_temp}°C\n"
            f"📉 Ночью до: {min_temp}°C\n\n"
            f"_Данные актуальны на {_get_current_time()}_"
        )
        return message
    except Exception as e:
        return f"⚠️ Ошибка получения погоды: {e}"

def _get_current_time():
    return time.strftime("%d.%m.%Y %H:%M", time.localtime())

def send_weather():
    """Отправляет сообщение в Telegram"""
    message = get_weather()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=params)
    
    if response.json().get("ok"):
        print(f"[{_get_current_time()}] ✅ Погода успешно опубликована!")
    else:
        print(f"[{_get_current_time()}] ❌ Ошибка: {response.json()}")

# 3. Настраиваем расписание: каждый день в 07:00
schedule.every().day.at("07:00").do(send_weather)

print("🤖 Бот запущен и ждет 07:00...")

# 🔽 РАСКОММЕНТИРУЙТЕ СТРОКУ НИЖЕ, ЧТОБЫ ПРОВЕРИТЬ РАБОТУ ПРЯМО СЕЙЧАС 🔽
send_weather()

# 4. Бесконечный цикл для работы планировщика
while True:
    schedule.run_pending()
    time.sleep(60) # Проверяем задачи каждую минуту, чтобы не грузить процессор