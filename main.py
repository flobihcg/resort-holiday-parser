import requests
import json
from bs4 import BeautifulSoup
import time
from booking_parser import ParseBooking

main_url_rh = 'https://search.resort-holiday.com/search_hotel?'
headers = {
    	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-type': 'text/html; charset=utf-8', 
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.1.802 Yowser/2.5 Safari/537.36'
}

# пример
url_keys = {
    'STATEINC': '78',           # Код страны
    'CHECKIN_BEG': '20220731',  # Дата въезда С гггг.мм.дд
    'CHECKIN_END': '20220731',  # Дата въезда ПО гггг.мм.дд
    'NIGHTS_FROM': '3',         # Мин. кол-во ночей
    'NIGHTS_TILL': '7',         # Макс. кол-во ночей
    'ADULT': '2',               # Кол-во взрослых
    'CHILD': '0',               # Кол-во детей
    'CURRENCY': '1',            # Валюта [1: RUB, 3:EUR]
    'TOWNS': [
        
    ],   
    'HOTELS': [                 # Отели
        815, 418, 429,
    ],
    'MEALS': [                  # Питание (аналогично HOTELS)
        
    ],
    'STARS': [
        
    ],
    'FILTER': '1',              # НЕ ТРОГАТЬ! Дефолт
    'PRICEPAGE': 1,             # Страница
    'DOLOAD': 1                 # НЕ ТРОГАТЬ! Дефолт Загрузчик поиска
}

result_json = {}
mylist = []

def main():
    while True:
        url = main_url_rh
        for key, value in url_keys.items():
            if isinstance(value, list):
                if len(value) > 0:
                    url += key + '=' + str(value[0])
                    for i in range(1, len(value)):
                        url += '%2C' + str(value[i])
                    url += '&'
            else:
                url += key + '=' + str(value)
                url += '&'
        r = ''
        try:
            r = requests.get(url, headers=headers)
            h = r.text
            soup = BeautifulSoup(h, features="html.parser")
        except Exception as e:
            print(e)
        html_tags = soup.select_one(".resultset").select_one('tbody').select('tr')
    
        for i in html_tags:
            h = {}
            h['Name'] = i.select_one('.link-hotel').select_one('a').text.replace('\n', '')
            h['Date'] = i.select_one('.sortie').text.replace('\n', '')
            h['Nights'] = i.select_one('.c').text.replace('\n', '')
            h['Food'] = i.select('td:not([class])')[1].text.replace('\n', '')
            h['Room'] = i.select('td:not([class])')[2].text.replace('\n', '')
            h['Price'] = {}
            h['Price']['resort-holiday'] = i.select_one('.td_price').text.replace('\n', '')
            mylist.append(h)

        ParseBooking(mylist)
    
        break # только одна страница
    
        #if soup.select_one('.pager').select('span')[-1].get('class')[0] == 'current_page':
        #    break
        #url = main_url_rh
        #url_keys['PRICEPAGE'] += 1
    
    result_json['data'] = mylist
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()