from bs4 import BeautifulSoup
import requests
import time
import re

base_url = 'https://www.kleiderkreisel.de/damenmode/korsetts?size_id[]=275&time=1484499311&page='
page = 1

def build_url(base_url, page):
    url = requests.get(base_url + str(page))
    return url

def get_soup(url):
    soup = BeautifulSoup(url.text, "lxml")
    return soup

def get_items(soup, page):
    items = []
    items_current = soup.find_all('div', class_='item-box__container')

    while True:
        items.append(items_current)
        print('Now scraping page: ' + str(page))
        page += 1
        url = build_url(base_url, page)
        soup = get_soup(url)
        items_current = soup.find_all('div', class_='item-box__container')
        if len(items_current) == 0:
            break
    print('Finished scraping')
    return items

def get_price(item):
    price_current = item.find('div', class_='item-box__title').getText()
    price_current = re.findall(r"[-+]?\d*\,\d+|\d+", price_current)
    price = float(price_current[0].replace(',', '.'))
    return price

def store_items(hearts, price, image, url):
    row = [hearts, price, image, url]
    return row

def get_item_data(items):
    item_data = []
    for item_page in items:
        for item in item_page:
            hearts = item.find('span', class_='favourites-count').getText()
            if hearts != '':
                hearts = int(hearts)
                if hearts > 1:
                    price = get_price(item)
                    image = item.find('img')['data-src']
                    url = 'https://www.kleiderkreisel.de' + item.find('a', class_='js-item-link')['href']
                    item_data.append(store_items(hearts, price, image, url))
    return item_data

def sort(item_data):
    item_data = sorted(item_data, key=lambda x: x[0], reverse=True)
    return item_data

def main():
    url = build_url(base_url, page)
    soup = get_soup(url)
    items = get_items(soup, page)
    item_data = get_item_data(items)
    item_data = sort(item_data)
    print('')

if __name__ == '__main__':
    start_time = time.time()
    main()
    print('--------------------')
    print("Execution time is %s seconds" % "%0.2f" % (time.time() - start_time))
