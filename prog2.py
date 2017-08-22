import sqlite3
import requests
import csv
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

class Database():

    def __init__(self):
        self.conn = sqlite3.connect("result.db")
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE if EXISTS pudb")
        self.cur.execute("CREATE TABLE IF NOT EXISTS pudb (name text, price integer, link text, image text, details text)")
        self.conn.commit()

    def insert(self, name, price, link, image, details):
        self.cur.execute("INSERT INTO pudb VALUES (?, ?, ?, ?, ?)",(name, price, link, image, details))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM pudb")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def __del__(self):
        self.conn.close()

class PUParser():
    def conn(self, link):
        cont = requests.get(link)
        soup = BeautifulSoup(cont.content, "html.parser")
        return soup

    def cr_links(self, i, min_price, max_price):
        """creates urls to parse"""
        link = "http://price.ua/catc839t1/page" + str(i) + ".html?price[min]=" + min_price + "&price[max]=" + max_price + ".html"
        return link

    def get_amount(self, soup):
        """gets number of the last page"""
        amount = soup.find("span", id="top-paginator-max")
        amount = int(amount.get_text())
        return amount

    def get_wrap(self, html):
        wrap_list = html.find_all("div", class_='product-item')
        return wrap_list

    def parse(self, wraps, i, f):
        price_wrap = wraps[i].find("div", class_="price-wrap")
        price_wrap = price_wrap.get_text().replace('\xa0', '')
        numbers = re.findall('(\d+)', price_wrap)
        price = int("".join(numbers))
        try:
            name = wraps[i].find("a", class_='model-name')
            name = name.get('title').replace('Цены на ', '').replace(' в Ивано-Франковске', '')
        except AttributeError:
            name = wraps[i].find("a", class_='ga_card_simple_pic')
            name = name.get('title')
            name_ar = name.split(" ")
            name_ar = name_ar[1: -2]
            name = " ".join(name_ar)
        image = wraps[i].find('img')
        image = image.get('data-original')
        try :
            link = wraps[i].find("a", class_='model-name')
            link = link.get('href')
        except AttributeError:
            link2 = wraps[i].find("a", class_='ga_card_simple_pic')
            link = link2.get('href')
        try:
            det_page_soup = pu.conn(link)
            det_n  = det_page_soup.find_all("td", class_ = "td-name")
            det = det_page_soup.find_all("td", class_ = "td-value")
            details = ""
            for i in range(1, len(det_n) - 2):
                details += det_n[i].get_text() + " " + det[i].get_text() + " "
        except:
            details = " "
        db.insert(name, price, link, image, details)
        to_csv(f, name, price, link, image, details)
        print(price, name, image, link, details)


def to_csv(f, name, price, link, image, details):
    writer = csv.writer(f)
    writer.writerow((name, price, link, image, details))

def main():
    min_price = str(input('input min price'))
    max_price = str(input("input max price"))
    a = datetime.now()
    print(a)
    f = open("result.csv", 'w')
    max = pu.get_amount(pu.conn(pu.cr_links(1, min_price, max_price)))
    print(max)
    for i in range(1, 10):
        print(i + 1)
        wraps = pu.get_wrap(pu.conn(pu.cr_links(i, min_price, max_price)))
        for j in range(len(wraps)):
            print(j + 1)
            pu.parse(wraps, j, f)
    b = datetime.now()
    db.view()
    print(a)
    print(b)
    f.close()
pu = PUParser()
db = Database()
if __name__ == '__main__':
    main()
