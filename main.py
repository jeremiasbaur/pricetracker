from scraper import *
from datastructures import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
            #for price in reversed(prices):
            for price in prices:
                #print(last_price.date<price.date)
                #x.append(mdates.date2num(datetime.date(price.date.year, price.date.month, price.date.day)))
                x.append(mdates.date2num(price.date))
                y.append(price.price)

                if last_price.price != price.price:
                    print("Product: %s \tCompany: %s \tID: %s"%(product.name, session.query(Company).get(product_company.company_id).name, product_company.tag))
                    print("Price before: %f \tnow: %f \tdate: %s"%(last_price.price, price.price, price.date))
                    if len(prices) >= 2 and price == prices[-1]:
                        biggest_changes.append([1-price.price/last_price.price, price.price, last_price.price, product.name, session.query(Company).get(product_company.company_id).name, product_company.tag, product])
                last_price = price
            if show_graph: plt.plot(x, y, label=session.query(Company).get(product_company.company_id).name)
             #plt.plot([i for i in range(len(y))], y)
            if show_graph: plt.gcf().autofmt_xdate()
            if show_graph: myFmt = mdates.DateFormatter('%D')
            if show_graph: plt.gca().xaxis.set_major_formatter(myFmt)
            if show_graph: plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            print(prices[-1].price)
    if show_graph: plt.show()
    biggest_changes.sort(key=lambda x:x[0])
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

try:
    engine = create_engine('postgresql://postgres:trackit@localhost:5432/pricetracker_database')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)
    session = session()

    #ap_digitec= Storage(name='Samsung Galaxy S9+', keyword='9017478', company="Digitec", price=float(499), date=datetime.datetime.now())

    netgear = session.query(Product).filter(Product.manufacturer_id == 'C2P43AE').first()
    #net = Product(name = 'UE43NU7092', manufacturer='Samsung', manufacturer_id='UE43NU7092UXXH')

    digitec = session.query(Company).filter(Company.name == 'Digitec').first()
    microspot = session.query(Company).filter(Company.name == 'Microspot').first()
    conrad = session.query(Company).filter(Company.name == 'Conrad').first()

    #pro_comp = session.query(ProductCompany).filter(ProductCompany.company_id == microspot.id)[0]
    #net_micro = ProductCompany(tag='1650635', product=netgear, company=conrad)

    digitec_scraper = DigitecScraper(digitec.url, digitec.scrape_url, digitec.id)
    microspot_scraper = MicrospotScraper(microspot.url, microspot.scrape_url, microspot.id)
    conrad_scraper = ConradScraper(conrad.url, conrad.scrape_url, conrad.id)

    if False:
        digitec_scraper.scrape_for_day()
        microspot_scraper.scrape_for_day()
        conrad_scraper.scrape_for_day()
        pass

    res = session.query(Product).filter(Product.manufacturer_id == '1066253').first()

    result = price_analyser_biggest_change(False)
    #result = price_analyser_biggest_change_overall(0) # 0 sort for absolute change, 1 sort for percent change
    #get_pricegraph(res)

    counter = 0
    for i in reversed(result):
        if counter > 20: break
        counter+=1
        get_pricegraph(i[-1])

finally:
    session.commit()
    session.close()
    Scraper.driver.quit()
