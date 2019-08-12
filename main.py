from scraper import *
from datastructures import *

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

#digitec_scraper.scrape_tag_category_products(1123, 1000, 0)

#print(microspot_scraper.scrape_by_manufacturer_id(netgear, save=True))
#print(microspot_scraper.scrape_price(netgear, save=True))

def price_analyser_biggest_change(show_graph = False):
    biggest_changes = []
    counter = 0
    started = datetime.datetime.now()
    for product in session.query(Product):
        if show_graph and counter > 19:
            break
            pass

        print(counter)
        counter+=1
        if show_graph: plt.figure(product.id)
        if show_graph: plt.suptitle(product.name)
        for product_company in product.product_offered:
            prices = product_company.prices

            #[print(i.date, end='') for i in prices]

            if len(prices) == 0:
                continue
            last_price = prices[0]
            x = []
            y = []

            if len(prices)>=2 and prices[-1].price != prices[-2].price:
                biggest_changes.append({"percent_change": 1-prices[-1].price/prices[-2].price, "price": prices[-1].price, "last_price": prices[-2].price, "product_name": product.name, "company": session.query(Company).get(product_company.company_id).name, "id": product_company.tag, "date": prices[-1].date,"product": product})
                print("Found price change")

            """for price in prices:
                #print(last_price.date<price.date)
                #x.append(mdates.date2num(datetime.date(price.date.year, price.date.month, price.date.day)))
                x.append(mdates.date2num(price.date))
                y.append(price.price)

                if last_price.price != price.price:
                    print("Product: %s \tCompany: %s \tID: %s"%(product.name, session.query(Company).get(product_company.company_id).name, product_company.tag))
                    print("Price before: %f \tnow: %f \tdate: %s"%(last_price.price, price.price, price.date))
                    if len(prices) >= 2 and price == prices[-1]:
                        biggest_changes.append({"percent_change": 1-price.price/last_price.price, "price": price.price, "last_price": last_price.price, "product_name": product.name, "company": session.query(Company).get(product_company.company_id).name, "id": product_company.tag, "date": price.date,"product": product})
                last_price = price
            if show_graph: plt.plot(x, y, label=session.query(Company).get(product_company.company_id).name)
             #plt.plot([i for i in range(len(y))], y)
            if show_graph: plt.gcf().autofmt_xdate()
            if show_graph: myFmt = mdates.DateFormatter('%D')
            if show_graph: plt.gca().xaxis.set_major_formatter(myFmt)
            if show_graph: plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            print(prices[-1].price)
    if show_graph: plt.show()"""
    biggest_changes.sort(key=lambda x:x["percent_change"])
    [print(i) for i in biggest_changes]
    print("Took %s seconds to query all prices"%(datetime.datetime.now()-started))
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
            #x.append(mdates.date2num(datetime.date(price.date.year, price.date.month, price.date.day)))
            x.append(mdates.date2num(price.date))
            y.append(price.price)
        plt.plot(x, y, label=session.query(Company).get(product_company.company_id).name)
         #plt.plot([i for i in range(len(y))], y)
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%D')
        plt.gca().xaxis.set_major_formatter(myFmt)
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

def preispiratTest():
    lol = datetime.datetime.now()
    print(lol)
    testProduct = session.query(ProductCompany).join(Product).join(Company).filter(and_(Product.manufacturer_id == 'DELL-U2718Q', Company.name == 'Digitec')).first()
    #print(digitec_scraper.get_latest_price(testProduct))
    print(testProduct.product.name, testProduct.company.name)
    print(datetime.datetime.now()-lol)
    testProduct.url = 'https://www.digitec.ch/de/s1/product/dell-ultrasharp-u2718q-27-3840-x-2160-pixels-monitor-6412351'
    test = Preispirat()
    test.uploadProduct(testProduct)

try:
    engine = create_engine('postgresql://postgres:trackit@localhost:5432/pricetracker_database')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)
    session = session()

    #netgear = session.query(Product).filter(Product.manufacturer_id == 'C2P43AE').first()
    #net = Product(name = 'UE43NU7092', manufacturer='Samsung', manufacturer_id='UE43NU7092UXXH')

    digitec = session.query(Company).filter(Company.name == 'Digitec').first()
    microspot = session.query(Company).filter(Company.name == 'Microspot').first()
    conrad = session.query(Company).filter(Company.name == 'Conrad').first()

    #pro_comp = session.query(ProductCompany).filter(ProductCompany.company_id == microspot.id)[0]
    #net_micro = ProductCompany(tag='1650635', product=netgear, company=conrad)

    digitec_scraper = DigitecScraper(digitec.url, digitec.scrape_url, digitec.id)
    microspot_scraper = MicrospotScraper(microspot.url, microspot.scrape_url, microspot.id)
    conrad_scraper = ConradScraper(conrad.url, conrad.scrape_url, conrad.id)

    #print(digitec_scraper.scrape_price(session.query(ProductCompany).filter(ProductCompany.tag == "10034506").first(), False))

    if False:
        failed = []
        failed.extend(digitec_scraper.scrape_for_day())
        print(failed)
        failed.extend(microspot_scraper.scrape_for_day())
        print(failed)
        failed.extend(conrad_scraper.scrape_for_day())
        pass

    #delete_prices_of_day()

    preispiratTest()
    # res = session.query(Product).filter(Product.manufacturer_id == '1066253').first()
    #
    # result = price_analyser_biggest_change(False)
    # #result = price_analyser_biggest_change_overall(0) # 0 sort for absolute change, 1 sort for percent change
    # #get_pricegraph(res)
    # #zero_sum()
    # #print(digitec_scraper.get_toppreise(session.query(Product).filter(Product.manufacturer_id=='DELL-U2718Q').first()))
    #
    # counter = 0
    # for i in reversed(result):
    #     if counter > 20: break
    #     if i['date'].date() != datetime.date.today():
    #         print("adsfasdf")
    #         continue
    #     counter+=1
    #     get_pricegraph(i['product'])

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
