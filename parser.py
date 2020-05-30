import requests
from bs4 import BeautifulSoup
import csv 

URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html(url, params=None):
    r =requests.get(url, headers=HEADERS, params=params)
    return r 

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else: 
        return 1
    print(pagination)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars = []
    for item in items: 
        uah_price = item.find('span', class_ = 'grey size13')
        if uah_price:
            uah_price = uah_price.get_text(strip=True)
        else:
            uah_price = 'Цену уточняйте'
        cars.append({
            'title': item.find('h3', class_= 'proposition_name').get_text(strip=True),
            'link': HOST + item.find('a').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
            'uah_price': uah_price,
            'city': item.find('svg', class_='svg-i16_pin').find_next('strong').get_text(),

        })
    return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в UAH', 'Город'])
        for item in items: 
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')        
    else:
        print('Error')


parse()
