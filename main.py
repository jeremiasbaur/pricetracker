from scraper import *
from datastructures import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

engine = create_engine('postgresql://postgres:trackit@localhost:5432/pricetracker_database')
Base.metadata.create_all(engine)

session = sessionmaker(engine)
session = session()

#ap_digitec= Storage(name='Samsung Galaxy S9+', keyword='9017478', company="Digitec", price=float(499), date=datetime.datetime.now())

netgear = session.query(Product).filter(Product.manufacturer_id == '9H.LGLLB.QBE').first()
#net = Product(name = 'UE43NU7092', manufacturer='Samsung', manufacturer_id='UE43NU7092UXXH')

digitec = session.query(Company).filter(Company.name == 'Digitec').first()
microspot = session.query(Company).filter(Company.name == 'Microspot').first()
conrad = session.query(Company).filter(Company.name == 'Conrad').first()

#comp = Company('Conrad', 'https://www.conrad.ch/', 'https://www.conrad.ch/de/')

#pro_comp = session.query(ProductCompany).filter(ProductCompany.company_id == microspot.id)[0]
#net_micro = ProductCompany(tag='0001403223', product=netgear, company=microspot)
#price = Price(price=171.90, date=datetime.datetime.now())
#net_micro.prices.append(price)

digitec_scraper = DigitecScraper(digitec.url, digitec.scrape_url, digitec.id)
microspot_scraper = MicrospotScraper(microspot.url, microspot.scrape_url, microspot.id)
conrad_scraper = ConradScraper(conrad.url, conrad.scrape_url, conrad.id)

#digitec_scraper.scrape_for_day()
#microspot_scraper.scrape_for_day()
#conrad_scraper.scrape_for_day()

#print(digitec_scraper.scrape_manufacturer_id(session.query(ProductCompany).filter(ProductCompany.product_id==netgear.id).first()))

#tinte_digitec = session.query(ProductCompany).filter(ProductCompany.tag == '3230182').first()

#print(digitec_scraper.scrape_price(netgear))
#print(microspot_scraper.scrape_price(netgear))
#print(conrad_scraper.scrape_price(netgear))

#samsung = Product(name='Extreme 128GB', manufacturer='Sandisk', manufacturer_id='SDSQXA1-128G-GN6MA')
#session.add_all([ProductCompany(tag='6304953', product=netgear, company= digitec), ProductCompany(tag='0001485727', product=netgear, company= microspot)])
#session.add(samsung)
#digitec_scraper.scrape_by_manufacturer_tag(samsung)

#digitec_scraper.scrape_tag_category_products(77, 1000, 0)

#print(microspot_scraper.scrape_by_manufacturer_id(netgear, save=True))
#print(microspot_scraper.scrape_price(netgear, save=True))

#for price in session.query(Price).filter(Price.product_company_id == microspot_scraper.scrape_by_manufacturer_id(netgear)).order_by(asc(Price.date)):
#    print(price.price)

#for product in session.query(Product):
#    print(product.manufacturer, product.name)
#    print(microspot_scraper.scrape_by_manufacturer_id(product, save=True))
biggest_changes = []
counter = 0
started = datetime.datetime.now()
for product in session.query(Product):
    if counter > 19:
        pass
        #break
    print(counter)
    counter+=1
    #plt.figure(product.id)
    #plt.suptitle(product.name)
    for product_company in session.query(ProductCompany).filter(ProductCompany.product_id == product.id):
        #prices = session.query(Price).filter(Price.product_company_id == product_company.id).order_by(asc(Price.date))
        prices = product_company.prices
        #prices = session.query(Price).intersect()
        #print(session.query(ProductCompany).get(product_company.id))
        [print(i.date, end='') for i in prices]
        print("\t")
        # prices.count() == 0:
        if len(prices) == 0:
            continue
        last_price = prices[0]
        x = []
        y = []
        #for price in reversed(prices):
        for price in prices:
            print(last_price.date<price.date)
            x.append(mdates.date2num(datetime.date(price.date.year, price.date.month, price.date.day)))
            y.append(price.price)

            if last_price.price != price.price:
                print("Product: %s \tCompany: %s \tID: %s"%(product.name, session.query(Company).get(product_company.company_id).name, product_company.tag))
                print("Price before: %f \tnow: %f \tdate: %s"%(last_price.price, price.price, price.date))
                if len(prices) >= 2 and price == prices[-1] and price.price/last_price.price < 0.8:
                    biggest_changes.append([1-price.price/last_price.price, price.price, last_price.price, product.name, session.query(Company).get(product_company.company_id).name, product_company.tag])
            last_price = price
        #plt.plot(x, y, label=session.query(Company).get(product_company.company_id).name)
         #plt.plot([i for i in range(len(y))], y)
        #plt.gcf().autofmt_xdate()
        #myFmt = mdates.DateFormatter('%D')
        #plt.gca().xaxis.set_major_formatter(myFmt)
        #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        print(prices[-1].price)
print("Took %s seconds to query all prices"%(datetime.datetime.now()-started))
plt.show()

[print(i) for i in biggest_changes]

#session.add(net)
session.commit()
session.close()
