import requests


def get_mail_ru_weather(city="москва"):
    url = f"https://pogoda.mail.ru/api/v1/city?name={city}"
    response = requests.get(url)
    city_id = response.json()["data"]["id"]

    weather_url = f"https://pogoda.mail.ru/api/v1/weather/{city_id}/now/"
    weather_data = requests.get(weather_url).json()

    return f"""
Погода в {city}:
🌡 Температура: {weather_data['temperature']['now']}°C
💨 Ветер: {weather_data['wind']['speed']} м/с
"""


if __name__ == "__main__":
    print(get_mail_ru_weather())
