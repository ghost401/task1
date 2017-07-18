import requests
from bs4 import BeautifulSoup
import sqlite3

class Database():

    def __init__(self):
        con=sqlite3.connect("parse.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS npdb (NAME INT, PHOTO TEXT, LINK TEXT, PRICE INT, DETAILS INT)")
        con.commit()
        con.close()

    def todb(self, name, image, link, price, details):
        con=sqlite3.connect("parse.db")
        cur=con.cursor()
        cur.execute("INSERT INTO npdb (?, ?, ?, ?, ?)",(name, image, link, price, details))
        con.commit()
        con.close()

    def view(self):
        con=sqlite3.connect("parse.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM npdb)
        rows = cur.fetchall()
        con.close()
        for row in rows:
            print row
class PUParser():
	
    def conn(self, link):
        try:
            cont = requests.get(link)
        except HTTPError:
            print("Can not access server!")
        soup = BeautifulSoup(cont.content, "html.parser")
        return soup
		
    def cr_links(self, i):
        base = 'http://price.ua/catc839t14/page'
        ad = '.html'
        link = base + str(i) + ad
        return link

    def get_amount(self):
        try:
            s_data = requests.get("http://price.ua/catc839t14.html")
        except HTTPError:
            print("Can not access server!")
        soup = BeautifulSoup(s_data.content, "html.parser")
        soup = soup.find("span",  id = "top-paginator-max")
        amount = int(soup.get_text())
        return amount
	
    def get_b(self, html):
        new_b = html.find_all("div",  class_ = 'product-item')
        return new_b
    
    def parse(self, b, i):
        name = b[i].find("a",  class_ = 'model-name')
        name = name.get('title')
        name = name.replace('Цены на ', '')
        name = name.replace(' в Ивано-Франковске', '')
        price = b[i].find("span",  class_ = "price")
        price = price.get_text()
        price = price.replace('\xa0', '')
        price = price.replace('грн.', '')
        price = price.replace(' ', '')
        price = int(price)
        det = b[i].find_all("div",  class_ = 'item')
        details = ""
        for i in range(len(det)):
            details += str(det[i].get_text())
        link = b[i].find("a",  class_ = 'model-name')
        link = link.get('href')
        image = b[i].find('img')
        image = image.get('src')
        if price > 10000 and price < 20000:
            db.todb(name, image, link, price, details)
pp = PUParser()
db = Database()

def main():
    for i in range(pp.get_amount()):
        link = pp.cr_links(i)
        html = pp.conn(link)
        for j in range(len(pp.get_b(html))):
            b = pp.get_b(html)
            pp.parse(b, i)

main()
