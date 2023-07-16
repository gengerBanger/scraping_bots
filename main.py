import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://coinmarketcap.com/ru/'

storage = 'result.csv'

HEADERS ={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79',
          'accept': '*/*'}

r = requests.get(URL, headers=HEADERS)

soup = BeautifulSoup(r.content, 'html.parser')

cards = soup.find_all('tr')

coins = {}

def save_csv(path, items):
    with open(path, 'w',encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['coin', 'price', 'changes per hour', 'changes per day', 'changes per week','market capitalization'])
        for coin in coins:
            writer.writerow([coin, coins[coin]['price'], coins[coin]['changes per hour'],
                             coins[coin]['changes per day'], coins[coin]['changes per week'],
                             coins[coin]['market capitalization']])

def calculating_the_sign(time_interval):
    if time_interval.find_all('span')[-2].span.attrs['class'] == ['icon-Caret-down']:
        return '-' + time_interval.text
    else:
        return '+' + time_interval.text

for card in cards:

    changes = card.find_all('td')

    try:

        title = card.find('p', {'class': 'sc-4984dd93-0 kKpPOn'})# название монеты
        if not title:
            title = card.find(class_='crypto-symbol').text
        else:
            title = title.text

        prise = card.find(class_='sc-bc83b59-0')# цена монеты
        if not prise:
            prise = card.find_all('td')[-2].find('span').text
        else:
            prise = prise.text

        try:

            h_1 = calculating_the_sign(changes[4])

            h_24 = calculating_the_sign(changes[5])

            week = calculating_the_sign(changes[6])

            market_capitalization = changes[7].find('span').text

        except IndexError:
            h_1 = ''
            h_24 = ''
            week = ''
            market_capitalization = ''

        coins[title] = {'price': prise, 'changes per hour': h_1, 'changes per day': h_24, 'changes per week': week, 'market capitalization': market_capitalization}
    except AttributeError:
            continue
save_csv(storage, coins)
print(coins)



