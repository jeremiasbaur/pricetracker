from scraper import *
from datastructures import Product, ProductCompany, Price, Company, PriceChanges

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from preispirat import Preispirat

from dateutil import parser

#print(digitec_scraper.scrape_price(netgear, True))

#print(digitec_scraper.scrape_manufacturer_id(session.query(ProductCompany).filter(ProductCompany.product_id==netgear.id).first()))

#tinte_digitec = session.query(ProductCompany).filter(ProductCompany.tag == '3230182').first()

#samsung = Product(name='Extreme 128GB', manufacturer='Sandisk', manufacturer_id='SDSQXA1-128G-GN6MA')
#session.add_all([ProductCompany(tag='6304953', product=netgear, company= digitec), ProductCompany(tag='0001485727', product=netgear, company= microspot)])
#session.add(samsung)
#digitec_scraper.scrape_by_manufacturer_tag(samsung)



#print(microspot_scraper.scrape_by_manufacturer_id(netgear, save=True))
#print(microspot_scraper.scrape_price(netgear, save=True))

def binary_search(prices, value):
    """
    :param prices: list of prices
    :param value: value to retrieve range
    :return: index range of value
    """
    l_leftmost = 0
    r = len(prices)
    while l_leftmost < r:
        mid = int((l_leftmost + r) / 2)
        if prices[mid].product_company_id < value:
            l_leftmost = mid+1
        else:
            r = mid

    l_rightmost = 0
    r = len(prices)
    while l_rightmost < r:
        mid = int((l_rightmost + r) / 2)
        if prices[mid].product_company_id > value:
            r = mid
        else:
            l_rightmost = mid+1
    return l_leftmost, l_rightmost - 1

def price_analyser_biggest_change():
    biggest_changes = []
    counter = 0
    started = datetime.datetime.now()
    prices = session.query(Price).order_by(Price.product_company_id.asc()).order_by(Price.date.asc()).all()
    for product in session.query(Product):
        print(datetime.datetime.now()-started)
        counter += 1
        for product_company in product.product_offered:
            l, r = binary_search(prices, product_company.id)
            print(l, r)
            if r-l <= 0:
                continue

            if prices[r].price != prices[r-1].price:
                biggest_changes.append({"percent_change": 1-prices[r].price/prices[r-1].price, "price": prices[r].price, "last_price": prices[r-1].price, "product_name": product.name, "company": session.query(Company).get(product_company.company_id).name, "id": product_company.tag, "date": prices[r].date,"product": product, "product_company": product_company, "price_today": prices[r].id, "price_yesterday": prices[r-1].id})
                print("Found price change")
    biggest_changes.sort(key=lambda x: x["percent_change"])
    [print(i) for i in biggest_changes]
    print("Took %s seconds to query all prices" % (datetime.datetime.now()-started))
    return biggest_changes

def price_analyser_biggest_change_overall(mode = 1, show_graph = False):
    biggest_changes = []
    counter = 0
    started = datetime.datetime.now()
    for product in session.query(Product):
        print(counter)
        counter+=1
        for product_company in product.product_offered:
            biggest_changes.append([0, 0, product.name, session.query(Company).get(product_company.company_id).name, product_company.tag, product])
            prices = product_company.prices

            if len(prices) == 0:
                continue
            last_price = prices[0]
            for price in prices:
                if last_price.price != price.price:
                    print("Product: %s \tCompany: %s \tID: %s"%(product.name, session.query(Company).get(product_company.company_id).name, product_company.tag))
                    print("Price before: %f \tnow: %f \tdate: %s"%(last_price.price, price.price, price.date))
                    biggest_changes[-1][0] += abs(price.price-last_price.price)
                    biggest_changes[-1][1] += abs(1-price.price/last_price.price)
                last_price = price
    biggest_changes.sort(key=lambda x:x[mode])
    [print(i) for i in biggest_changes]

    for i in range(20):
        if not show_graph: break
        product = session.query(Product).get(biggest_changes[-1-i][-1])
        plt.figure(product.id)
        plt.suptitle(product.name)
        for product_company in product.product_offered:
            prices = product_company.prices
            if len(prices) == 0:
                continue
            x = []
            y = []
            for price in prices:
                #x.append(mdates.date2num(datetime.date(price.date.year, price.date.month, price.date.day)))
                x.append(mdates.date2num(price.date))
                y.append(price.price)
            plt.plot(x, y, label=session.query(Company).get(product_company.company_id).name)
            plt.gcf().autofmt_xdate()
            myFmt = mdates.DateFormatter('%D')
            plt.gca().xaxis.set_major_formatter(myFmt)
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
    print("Took %s seconds to query all prices"%(datetime.datetime.now()-started))
    return biggest_changes

def scrape_images():
    for product in session.query(Product).all():
        product.url_image = digitec_scraper.scrape_image_product(product)
        print(product.url_image)

def get_pricegraph(product):
    plt.figure(product.id)
    plt.suptitle(product.name)
    for product_company in product.product_offered:
        prices = product_company.prices

        if len(prices) == 0:
            continue
        x = []
        y = []
        for price in prices:
            x.append(mdates.date2num(price.date))
            y.append(price.price)
        plt.plot(x, y, label=session.query(Company).get(product_company.company_id).name)

        plt.gcf().autofmt_xdate()
        my_fmt = mdates.DateFormatter('%D')
        plt.gca().xaxis.set_major_formatter(my_fmt)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

def zero_sum(timeframe = [0,0]):
    #parser.parse('', dayfirst=True)
    for company in session.query(Company):
        sum = 0
        for product_company in session.query(ProductCompany).filter(ProductCompany.company == company):
            last_price = None
            for price in session.query(Price).filter(Price.product_company_id == product_company.id):
                if last_price == None: last_price = price.price
                if price.price / last_price != 1:
                    sum += price.price - last_price
                    last_price = price.price
        print("Sum of company %s : %f"%(company.name, sum))

def delete_prices_of_day():
    print(datetime.date.today())
    for price in session.query(Price):
        if (price.date.date() == datetime.date.today()):
            print(price.id, price.date, price.date.date() == datetime.date.today())
            session.delete(price)

def preispiratTest(testProduct):
    lol = datetime.datetime.now()
    #testProduct = session.query(ProductCompany).join(Product).join(Company).filter(and_(Product.manufacturer_id == 'DELL-U2718Q', Company.name == 'Digitec')).first()
    #print(digitec_scraper.get_latest_price(testProduct))
    #testProduct.url = 'https://www.digitec.ch/de/s1/product/dell-ultrasharp-u2718q-27-3840-x-2160-pixels-monitor-6412351'
    test = Preispirat()
    test.uploadProduct(testProduct)

def url_to_product():
    for product_company in digitec.stock:
        product_company.url = digitec_scraper.url_product(product_company)
    for product_company in microspot.stock:
        product_company.url = 'https://www.microspot.ch/msp/products/' + product_company.tag
    for product_company in conrad.stock:
        product_company.url = conrad_scraper.url_product(product_company)

try:
    engine = create_engine('postgresql://postgres:admin@localhost:5432/pricetracker_database')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)
    session = session()

    digitec = session.query(Company).filter(Company.name == 'Digitec').first()
    microspot = session.query(Company).filter(Company.name == 'Microspot').first()
    conrad = session.query(Company).filter(Company.name == 'Conrad').first()

    digitec_scraper = DigitecScraper(digitec.url, digitec.scrape_url, digitec.id)
    microspot_scraper = MicrospotScraper(microspot.url, microspot.scrape_url, microspot.id)
    conrad_scraper = ConradScraper(conrad.url, conrad.scrape_url, conrad.id)

    if True:
        failed = []
        failed.extend(digitec_scraper.scrape_for_day())
        print(failed)
        failed.extend(microspot_scraper.scrape_for_day())
        print(failed)
        failed.extend(conrad_scraper.scrape_for_day())
        pass

    #delete_prices_of_day()

    #preispiratTest()

    #digitec_scraper.scrape_tag_category_products(591, 1000, 0)

    #scrape_images()

    result = price_analyser_biggest_change()

    #result = price_analyser_biggest_change_overall(0) # 0 sort for absolute change, 1 sort for percent change
    #get_pricegraph(res)
    #zero_sum()
    #print(digitec_scraper.get_toppreise(session.query(Product).filter(Product.manufacturer_id=='DELL-U2718Q').first()))

    #url_to_product()

    counter = 0
    for i in reversed(result):
        if counter > 100: break
        if i['date'].date() != datetime.date.today():
            continue
        counter += 1
        if(True and len(session.query(Price).filter(Price.id == i['price_today']).all()) == 1 and len(session.query(Price).filter(Price.id == i['price_yesterday']).all())==1):
            test = PriceChanges(date=datetime.datetime.today(), price_today_id=i['price_today'], price_yesterday_id=i['price_yesterday'], percent_change=i['percent_change']+1, product_company_id= i['product_company'].id)
            session.add(test)
            session.commit()
        #get_pricegraph(i['product'])
        print(i)
        #preispiratTest(i['product_company'])

    #zero_sum()

finally:
    session.commit()
    session.close()
    Scraper.driver.quit()

"""
error products:
LX50 (Over-Ear, Schwarz) Microspot
G12IG 19V1 (Intel Core i7-8700, 16GB, SSD, HDD) Microspot
G9IG 19V1 (Intel Core i5-8400, 8GB, SSD, HDD) Microspot
G12AR 19V1 (AMD Ryzen 7 2700X, 16GB, SSD, HDD) Microspot
M9 (2GB, Schwarz) Microspot
0001345833 Microspot
0001713855 Microspot
0001703185 Microspot
0001054911 Microspot
0001725909 Microspot

6843426 digitec
6191539 digitec
10133029 digitec
8218823 digitec
8985094 digitec
7033103 digitec
9632782 digitec
5627781 digitec
6333008 digitec
6982815 digitec
9623754 digitec
6190303 digitec
8810945 digitec
2452586 digitec
10369198 digitec
10450681 digitec
8182687 digitec
8218823 digitec
8985094 digitec
10125597 digitec
6427502 digitec
6972334 digitec
3229667 digitec
5341475 digitec
6399709 digitec
235363 digitec

"""
