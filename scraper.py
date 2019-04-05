from bs4 import BeautifulSoup as bs
import requests as r
import json

class Scraper():
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    def __init__(self, website_url, scrape_base_url):
        self.info = [website_url, scrape_base_url]

    def scrape_price(self, product):
        pass

    def get_product_id(self, product):
        pass

    def url_product(self, product):
        pass

class DigitecScraper(Scraper):
    def scrape_price(self, product):
        soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
        return soup.find('div', {'class': 'product-price'}).text.split('.')[0].split(' ')[1]

    def get_product_id(self, product):
        return str(6569196) # here query to database to this specific company and it's related product

    def url_product(self, product):
        #return 'https://www.digitec.ch/de/s1/product/netgear-nighthawk-x6s-mesh-extender-access-point-repeater-6569196'
        return self.info[1] + self.get_product_id(product)

class ConradScraper(Scraper):
    def scrape_price(self, product):
        soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
        return soup.find(itemprop='price').get('content')

    def get_product_id(self, product):
        return 'netgear-ex8000-wlan-repeater-24-ghz-5-ghz-5-ghz-1604352.html'

    def url_product(self, product):
        return self.info[1] + self.get_product_id(product)

class MicrospotScraper(Scraper):
    def scrape_price(self, product):
        data = r.get(self.url_product(product), headers = self.header).json()
        return str(data['price']['value'])

    def get_product_id(self, product):
        return '0001403223'

    def url_product(self, product):
        return self.info[1] + self.get_product_id(product) + '?fieldSet=FULL&lang=de'

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
