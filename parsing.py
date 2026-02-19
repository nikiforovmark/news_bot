"""
Инструкция по парсингу сайтов:
1. Заходим на вебсайт
2. F12 - network - dock
2.1. Если видим весь контент - Server site rendering - используем bs4
2.2. Если нет - Client site rendering - xhr ищем api
"""
from decimal import *

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36 "
}


def bitcoin():
    """Получает котировки с сайта РБК Инвестиций и возвращает строку с курсом биткоина."""
    response = requests.get('https://www.rbc.ru/crypto/data/graph/166026/day/3', headers=headers)
    data = response.json()
    btc = str(format(data['result']['data'][-1][-1], '.2f'))
    response2 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/72413/w', headers=headers)
    data2 = response2.json()
    usd = str(format(data2['result']['data'][-1][-8], '.3f'))
    return f"Бирж. BTC: ${btc}\nБирж. BTC: ₽{str(format(float(btc) * float(usd), '.2f'))}"


def parsing_news():  # новости со ссылками
    """Получает новости с сайта Лента.ру и возвращает списки с пятью заголовками и ссылками."""
    response = requests.get('https://lenta.ru/', headers=headers)
    soap = BeautifulSoup(response.content, 'html.parser')
    titles = soap.findAll("h3", "card-mini__title")
    urls = soap.findAll("a", "card-mini _topnews")
    i = 0
    j = 0
    news_titles = []
    news_urls = []
    for data in titles:
        if i == 5:
            break
        else:
            news_titles.append(str(i + 1) + ". " + data.next)
            i += 1
    for data in urls:
        if j == 5:
            break
        else:
            if (data.attrs['href'])[:5] == "https":
                news_urls.append(f"{data.attrs['href']}")
            else:
                news_urls.append(f"https://lenta.ru{data.attrs['href']}")
            j += 1
    return news_titles, news_urls


def parsing_quotes():
    """Получает котировки с сайта РБК Инвестиций и возвращает список с курсом доллара и евро."""
    response = requests.get('https://www.rbc.ru/quote/data/ticker/graph/72413/w', headers=headers)
    data = response.json()
    usd = str(format(data['result']['data'][-1][-8], '.2f'))

    response1 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/72383/w', headers=headers)
    data1 = response1.json()
    eur = str(format(data1['result']['data'][-1][-8], '.2f'))
    return [f"ЦБ РФ USD: ₽{usd}", f"ЦБ РФ EUR: ₽{eur}"]


def parsing_invest_portfolio():
    """Получает стоимость портфеля на основе данных сайта РБК Инвестиций и возвращает список."""
    response = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59256/d', headers=headers)
    data = response.json()
    gazp = Decimal(format(data['result']['data'][-1][-8], '.2f'))

    old_my_gazp = Decimal(160.97) * 10
    new_my_gazp = gazp * 10
    profit_my_gazp = round(new_my_gazp - old_my_gazp, 2)

    old_gift_gazp = Decimal(163.82) * 1
    new_gift_gazp = gazp * 1
    profit_gift_gazp = round(new_gift_gazp - old_gift_gazp, 2)

    response1 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59883/d', headers=headers)
    data = response1.json()
    vtbr = Decimal(format(data['result']['data'][-1][-8], '.5f'))

    old_vtbr = Decimal(0.023035) * 10000
    new_vtbr = round(vtbr * 8, 2)
    profit_vtbr = round(new_vtbr - old_vtbr, 2)

    response2 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59363/d', headers=headers)
    data = response2.json()
    mtss = Decimal(format(data['result']['data'][-1][-8], '.2f'))

    old_mtss = Decimal(248.45) * 10
    new_mtss = mtss * 10
    profit_mtss = round(new_mtss - old_mtss, 2)

    response3 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59382/d', headers=headers)
    data = response3.json()
    nvtk = Decimal(format(data['result']['data'][-1][-8], '.2f'))

    old_nvtk = Decimal(1491.6) * 1
    new_nvtk = nvtk * 1
    profit_nvtk = round(new_nvtk - old_nvtk, 2)

    response4 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59402/d', headers=headers)
    data = response4.json()

    pikk = Decimal(format(data['result']['data'][-1][-8], '.2f'))
    old_pikk = Decimal(675.8) * 1
    new_pikk = pikk * 1
    profit_pikk = round(new_pikk - old_pikk, 2)

    response5 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59430/d', headers=headers)
    data = response5.json()

    rosn = Decimal(format(data['result']['data'][-1][-8], '.2f'))
    old_rosn = Decimal(593.45) * 11
    new_rosn = rosn * 11
    profit_rosn = round(new_rosn - old_rosn, 2)

    response6 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59762/d', headers=headers)
    data = response6.json()

    sber = Decimal(format(data['result']['data'][-1][-8], '.2f'))
    old_sber = Decimal(271.95) * 10
    new_sber = sber * 10
    profit_sber = round(new_sber - old_sber, 2)

    response7 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/59214/d', headers=headers)
    data = response7.json()

    chmf = Decimal(format(data['result']['data'][-1][-8], '.2f'))
    old_chmf = Decimal(1611.2) * 1
    new_chmf = chmf * 1
    profit_chmf = round(new_chmf - old_chmf, 2)

    response8 = requests.get('https://www.rbc.ru/quote/data/ticker/graph/69684/d', headers=headers)
    data = response8.json()

    yndx = Decimal(format(data['result']['data'][-1][-8], '.2f'))
    old_yndx = Decimal(2489.4) * 1
    new_yndx = yndx * 1
    profit_yndx = round(new_yndx - old_yndx, 2)

    # response9 = requests.get('https://quote.ru/api/v1/ticker/69684', headers=headers)
    # data = response9.json()
    # tbru = Decimal(format(data['data']['ticker']['lastPrice'], '.2f'))

    old_tbru = round(Decimal(5.82) * 200, 2)
    new_tbru = round(Decimal(5.81) * 200, 2)
    profit_tbru = round(new_tbru - old_tbru, 2)

    rub = round(Decimal(292.83), 2)

    all_sum = sum([new_my_gazp, new_gift_gazp, new_vtbr, new_mtss, new_nvtk, new_pikk, new_rosn, new_sber,
                  new_chmf, new_yndx, new_tbru, rub])

    all_profit = sum([profit_my_gazp, profit_gift_gazp, profit_vtbr, profit_mtss, profit_nvtk, profit_pikk, profit_rosn,
                      profit_sber, profit_chmf, profit_yndx, profit_tbru])

    return "\n".join([f"01. Газпром:          {new_my_gazp} ₽ (+{profit_my_gazp} ₽)",
                      f"02. 🎁Газпром:   {new_gift_gazp} ₽ (+{profit_gift_gazp} ₽)",
                      f"03. Банк ВТБ:         {new_vtbr} ₽ (+{profit_vtbr} ₽)",
                      f"04. МТС:                   {new_mtss} ₽ (+{profit_mtss} ₽)",
                      f"05. Новатэк:           {new_nvtk} ₽ ({profit_nvtk} ₽)",
                      f"06. ПИК:                   {new_pikk} ₽ (+{profit_pikk} ₽)",
                      f"07. Роснефть:        {new_rosn} ₽ ({profit_rosn} ₽)",
                      f"08. Сбербанк:        {new_sber} ₽ (+{profit_sber} ₽)",
                      f"09. Северсталь:    {new_chmf} ₽ (+{profit_chmf} ₽)",
                      f"10. Яндекс:              {new_yndx} ₽ (+{profit_yndx} ₽)",
                      f"11. TBRU:                 {new_tbru} ₽ ({profit_tbru} ₽)",
                      f"12. RUB:                    {rub} ₽",
                      f"За все время:        <b>{all_sum} (+{all_profit} ₽)</b>"])


def get_vk_photo_id():
    """Получает фото с альбома vk.com и выводит в консоль id фото."""
    response = requests.get('https://m.vk.com/album-184860963_00?rev=1', headers=headers)
    soap = BeautifulSoup(response.content, 'html.parser')
    info = soap.find_all("div", {"class": "PhotosPhotoItem__photo _image"})
    for item in info:
        print(f"photo{item['data-id']}")


def get_answer(termin):  # Поиск терминов
    new_termin = "+".join(termin.split())
    termin_for_wiki = "_".join(termin.split())
    response = requests.get(f"https://www.google.ru/search?q={new_termin}", headers=headers)
    soap = BeautifulSoup(response.text, "html.parser")
    text = soap.get_text("\n")
    res = text.split("\n")
    max_index = 0
    max_len = 0
    for x, item in enumerate(res):
        if item.startswith("ru.wikipedia.org"):
            index = res.index(item) + 1
            answer = res[index] + f"\nПодробнее: https://ru.wikipedia.org/wiki/{termin_for_wiki}"
            return answer
        if len(item) > max_len:
            max_len = len(item)
            max_index = x
    else:
        if res[max_index].startswith("This traffic"):
            return f"Превышено число запросов к серверу. Попробуйте позже или воспользуйтесь ссылкой ниже.\n" \
                   f"Поиск в Google: https://www.google.ru/search?q={new_termin}"
        else:
            return res[max_index] + f"\nПодробнее: https://www.google.ru/search?q={new_termin}"


if __name__ == '__main__':
    print()
