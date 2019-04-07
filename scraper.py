from bs4 import BeautifulSoup as bs
import requests as r
from datastructures import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import json

class Scraper():
    engine = create_engine('postgresql://postgres:trackit@localhost:5432/pricetracker_database')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)
    session = session()

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def __init__(self, website_url, scrape_base_url, id):
        self.info = [website_url, scrape_base_url, id]

    def get_product_company(self, product): # here query to database to this specific company and it's related product
        return self.session.query(ProductCompany).filter(and_(ProductCompany.product_id == product.id, ProductCompany.company_id == self.info[2])).first()

    def scrape_price(self, product, save=False):
        if isinstance(product, Product):
            product = self.get_product_company(product)
        return product

    def get_product_id(self, product):
        return session.query(Product).get(Product)

    def url_product(self, product):
        pass

    def scrape_for_day(self):
        counter = 0
        for product in self.session.query(ProductCompany).filter(ProductCompany.company_id == self.info[2]):
            self.scrape_price(product, save=True)
            counter+=1
        print('Updated %d products for company %s'%(counter, self.session.query(Company).get(self.info[2]).name))
        self.session.commit()

    def scrape_by_manufacturer_tag(self, product):
        pass

    def insert_new_product(self, product, with_price=False):
        if isinstance(product, Product):
            results = scrape_by_manufacturer_tag(product)
            new_product = ProductCompany(tag=results[0], product=product, company=self.session.query(Company).get(self.info[2]))
            if with_price:
                self.scrape_price(product = new_product, save = True)
            self.session.commit()

class DigitecScraper(Scraper):
    def scrape_price(self, product, save=False):
        product = super().scrape_price(product)
        soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
        price = soup.find('div', {'class': 'product-price'}).text.split('.')[0].split(' ')[1]

        if save!= None and save:
            new_product_price = Price(price, datetime.datetime.now())
            product.prices.append(new_product_price)

        return price

    def url_product(self, product):
        return self.info[1] + product.tag

    def scrape_by_manufacturer_tag(self, product):
        soup = bs(r.get('https://www.digitec.ch/de/search?q=SM-G965FZKDAUT', headers=self.header).content, 'html.parser')
        print(soup)
        print(soup.find('div', {'class': 'panel--i3JJH productList'}))
        #if no 'enterSearchWrapper--3Vu4d' rip

class MicrospotScraper(Scraper):
    def scrape_price(self, product, save=False):
        product = super().scrape_price(product)
        data = r.get(self.url_product(product), headers = self.header).json()
        price = data['price']['value']

        if save!= None and save:
            new_product_price = Price(price, datetime.datetime.now())
            product.prices.append(new_product_price)

        return price

    def url_product(self, product):
        return self.info[1] + product.tag + '?fieldSet=FULL&lang=de'

class ConradScraper(Scraper):
    def scrape_price(self, product, save=False):
        product = super().scrape_price(product)
        soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
        price = soup.find(itemprop='price').get('content')

        if save:
            new_product_price = Price(price, datetime.datetime.now())
            product.prices.append(new_product_price)

        return price

    def url_product(self, product):
        return self.info[1] + product.tag

if __name__ == '__main__':
    """if response.history:
        print("Request was redirected")
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    else:
        print("Request was not redirected")"""
    digitec = DigitecScraper('https://www.digitec.ch/', 'https://www.digitec.ch/de/s1/product/')
    print(digitec.scrape_price(1))
    conrad = ConradScraper('https://www.conrad.ch/', 'https://www.conrad.ch/de/')
    print(conrad.scrape_price(1))
    microspot = MicrospotScraper('https://www.microspot.ch/', 'https://www.microspot.ch/mspocc/occ/msp/products/')
    print(microspot.scrape_price(1))
