import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

URL = 'https://coinmarketcap.com/ru/'

storage = 'result.csv'

coins = {}
def scrolling_save():
    try:
        driver.get(url=URL)
        action = ActionChains(driver)
        while flag := driver.find_element(By.CLASS_NAME, "sc-428ddaf3-0"):
            if driver.find_element(By.CLASS_NAME, "sc-428ddaf3-0"):
                action.move_to_element(flag).perform()
            time.sleep(1)
    except Exception:
        with open("str.html", 'w', encoding="utf-8") as file:
            file.write(driver.page_source)
    finally:
        driver.close()
        driver.quit()
        with open('str.html', encoding='utf-8') as file:
            src = file.read()

    soup = BeautifulSoup(src, 'html.parser')

    return soup.find_all('tr')

def save_csv(path, items):
    with open(path, 'w', encoding='utf-8', newline='') as file:
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

def main():
    cards = scrolling_save()

    for card in cards:
        changes = card.find_all('td')
        try:
            title = card.find('p', {'class': 'sc-4984dd93-0 kKpPOn'}).text  # название монеты

            prise = card.find(class_='sc-bc83b59-0').text # цена монеты

            h_1 = calculating_the_sign(changes[4]) # изменения за час

            h_24 = calculating_the_sign(changes[5]) # изменения за день

            week = calculating_the_sign(changes[6]) # изменения за неделю

            market_capitalization = changes[7].find('span').text # капитализация

            coins[title] = {'price': prise, 'changes per hour': h_1, 'changes per day': h_24, 'changes per week': week,
                            'market capitalization': market_capitalization}
        except AttributeError:
            continue
    save_csv(storage, coins)
    print(coins)

if __name__ == '__main__':
    main()

