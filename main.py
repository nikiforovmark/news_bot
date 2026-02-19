"""
aiogram-2.25.1
"""

import os
import time
import datetime
import asyncio
import logging

import requests
from aiogram import Bot, Dispatcher, executor, types

import config
import dmb
import parsing
import weather
import serializer

bot = Bot(token=config.TOKEN)  # from BotFather
dp = Dispatcher(bot=bot)

cache_news = cache_quotes = cache_invest = ""
cache_time_news = cache_time_quotes = cache_time_invest = datetime.datetime.now()

# file_log = logging.FileHandler("sample.log", mode="w")
file_log = logging.FileHandler("sample.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO)


@dp.message_handler(commands=['narfu'])
async def narfu(message: types.Message):
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    out = False
    while not out:
        try:
            print("starting...")
            requests.get('https://mail.narfu.ru')
            out = True
        except requests.exceptions.ConnectionError as ex:
            print(ex)
            time.sleep(300)
    mess = f'May be it works! The end.'
    await bot.send_message(message.chat.id, mess, parse_mode='html')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    if message.from_user.last_name:
        mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>\n' \
               f'Используй команды, например, /news'
    else:
        mess = f'Привет, <b>{message.from_user.first_name}</b>\nИспользуй команды, например, /news'
    await bot.send_message(message.chat.id, mess, parse_mode='html')


@dp.message_handler(commands=['bitcoin'])
async def show_bitcoin(message: types.Message):
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    mess = parsing.bitcoin()
    await bot.send_message(message.chat.id, mess, parse_mode='html')


@dp.message_handler(commands=['dzen'])
async def show_dzen(message: types.Message):
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить веб-сайт", url="https://dzen.ru"))
    await message.reply('Перейди на сайт', reply_markup=markup)


@dp.message_handler(commands=['dmb'])
async def show_dmb(message: types.Message):
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    if str(message.from_user.id) == config.BASE_ID:  # Проверка на доступ к команде
        mess = dmb.dmb(message.from_user.id)
    else:
        mess = "<b>У вас пока нет доступа к этой команде, обратитесь к разработчику</b>"
    await bot.send_message(message.chat.id, mess, parse_mode='html')


@dp.message_handler(commands=['setdmb'])
async def set_dmb(message: types.Message):
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    if str(message.from_user.id) != config.BASE_ID:
        await bot.send_message(message.chat.id, "Доступ запрещён", parse_mode='html')
        return

    args = message.text.split()
    if len(args) != 4:
        await bot.send_message(message.chat.id, "Формат: /setdmb ДД ММ ГГГГ", parse_mode='html')
        return

    try:
        day = int(args[1])
        month = int(args[2])
        year = int(args[3])
        # Простейшая проверка корректности даты
        datetime.datetime(year, month, day)
    except (ValueError, TypeError):
        await bot.send_message(message.chat.id, "Некорректная дата. Используйте числа.", parse_mode='html')
        return

    dmb.set_date(message.from_user.id, day, month, year)
    await bot.send_message(message.chat.id, f"Дата ДМБ установлена: {day:02d}.{month:02d}.{year}", parse_mode='html')


@dp.message_handler(commands=['courses'])
async def show_quotes(message: types.Message):
    global cache_quotes
    global cache_time_quotes
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    if cache_quotes == "" or datetime.datetime.now() - datetime.timedelta(minutes=15) > cache_time_quotes:
        quotes = parsing.parsing_quotes()
        mess = f"{quotes[0]}\n{quotes[1]}"
        await bot.send_message(message.chat.id, mess, parse_mode='html')
        cache_quotes = mess
        cache_time_quotes = datetime.datetime.now()
    else:
        await bot.send_message(message.chat.id, cache_quotes, parse_mode='html')


@dp.message_handler(commands=['news'])
async def show_news(message: types.Message):
    global cache_news
    global cache_time_news
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    if str(message.from_user.id) != 0:
        if cache_news == "" or datetime.datetime.now() - datetime.timedelta(minutes=15) > cache_time_news:
            news = parsing.parsing_news()
            mess = ""
            for i in range(0, 5):
                mess += f"<a href=\"{news[1][i]}\">{news[0][i]}</a>\n"
            await bot.send_message(message.chat.id, mess, parse_mode='html')
            cache_news = mess
            cache_time_news = datetime.datetime.now()
        else:
            await bot.send_message(message.chat.id, cache_news, parse_mode='html')
    else:
        mess = "<b>У вас нет доступа к этой команде</b>"
        await bot.send_message(message.chat.id, mess, parse_mode='html')


@dp.message_handler(commands=['weather'])
async def show_weather(message: types.Message):
    uid = message.from_user.id
    city = message.text[9:]
    logging.info(f"{uid} {time.asctime()} {message.text}")

    data = serializer.get_data()
    if str(uid) not in data["users"]:
        data["users"][f"{uid}"] = {
            "requests_count": 0,
            "weather_city": city
        }

    if city == data["users"][f"{uid}"]["weather_city"] == "":
        mess = "<b>Укажите город, например: '/weather Архангельск'</b>"
        data["users"][f"{uid}"]["requests_count"] += 1
        serializer.write(data)
        await bot.send_message(message.chat.id, mess, parse_mode='html')
        return 0

    tasks = []

    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if city != "":
        data["users"][f"{uid}"]["weather_city"] = city

    data["users"][f"{uid}"]["requests_count"] += 1
    serializer.write(data)
    current_weather = asyncio.create_task(weather.get_weather(data["users"][f"{uid}"]["weather_city"]))
    tasks.append(current_weather)

    await bot.send_message(message.chat.id, await list(asyncio.as_completed(tasks))[0], parse_mode='html')


@dp.message_handler(commands=['test'])
async def get_answer(message: types.Message):
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    termin = message.text[6:]
    if termin != "":
        mess = parsing.get_answer(termin)
        await bot.send_message(message.chat.id, mess, parse_mode='html')
    else:
        await bot.send_message(message.chat.id, "Пустое сообщение", parse_mode='html')


@dp.message_handler(commands=['invest'])
async def show_quotes(message: types.Message):
    global cache_invest
    global cache_time_invest
    logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
    if cache_invest == "" or datetime.datetime.now() - datetime.timedelta(minutes=15) > cache_time_invest:
        portfolio = parsing.parsing_invest_portfolio()
        # mess = f"{portfolio[0]}\n{portfolio[1]}"
        mess = portfolio
        await bot.send_message(message.chat.id, mess, parse_mode='html')
        cache_invest = mess
        cache_time_invest = datetime.datetime.now()
    else:
        await bot.send_message(message.chat.id, cache_invest, parse_mode='html')


# @dp.message_handler(commands=['help'])
# async def buttons(message: types.Message):
#     logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     _website = types.KeyboardButton('/Дзен')
#     _bitcoin = types.KeyboardButton('/Биткоин')
#     news = types.KeyboardButton('/Новости')
#     _dmb = types.KeyboardButton('/ДМБ')
#     quotes = types.KeyboardButton('/Котировки')
#     btn_weather = types.KeyboardButton('/Погода')
#     if str(message.from_user.id) == config.BASE_ID:
#         markup.add(_website, _bitcoin, news, _dmb, quotes, btn_weather)
#     else:
#         markup.add(_website, _bitcoin, news, quotes, btn_weather)
#     await message.reply('Держи кнопочки ↓', reply_markup=markup)
#
#
# @dp.message_handler(func=lambda message: True)
# async def echo_all(message: types.Message):
#     logging.info(f"{message.from_user.id} {time.asctime()} {message.text}")
#     text = message.text.lower()
#     if text == "hello" or text == "привет" or text == "hi" or text == "прив":
#         await bot.send_message(message.chat.id, 'И тебе привет!')
#     elif text == "id":
#         await bot.send_message(message.chat.id, f'Твой ID: {message.from_user.id}')
#     elif text == "all":
#         await bot.send_message(message.chat.id, f'Всё что есть: \n{message}')
#     else:
#         await message.reply('Не понял')


if __name__ == "__main__":
    executor.start_polling(dp)
