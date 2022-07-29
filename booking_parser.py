from bs4 import BeautifulSoup
import requests
import json
import time

url_getid = 'https://accommodations.booking.com/autocomplete.json'
cok = {
    "query": None,
    "pageview_id": "f3ae6db9c405036b",
    "aid": 304142,
    "language": "ru",
    "size": 5
}
headers = {
            'Content-type': 'text/html; charset=UTF-8', 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.65'
    }

d = []
storage = {}

def ParseBooking(data):
    for el in data:    
        s = el['Name'].split('Guest House')[0].split('*')[0][:-1]
        if s in storage:
            pass
        else:
            cok["query"] = s
            r = requests.post(url_getid, json=cok)
            
            url_search = f'https://www.booking.com/searchresults.ru.html?dest_id={r.json()["results"][0]["dest_id"]}&dest_type=hotel'
            r = requests.get(url_search, headers=headers)
            soup = BeautifulSoup(r.text, features="html.parser")
            
            url_hotel = soup.select_one('.e13098a59f').get('href')
            r = requests.get(url_hotel, headers=headers)
            print(r)
            storage[s] = 1
            # soup = BeautifulSoup(r.text, features="html.parser")
            # storage[s] = data_of_soup...
            
            print(f'{s} added!')
    with open('itog.json', 'w', encoding='utf-8') as f:
        json.dump(storage, f, ensure_ascii=False, indent=4)
