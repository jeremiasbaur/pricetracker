from scraper import *
from datastructures import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

engine = create_engine('postgresql://postgres:trackit@localhost:5432/pricetracker_database')
Base.metadata.create_all(engine)

session = sessionmaker(engine)
session = session()

#ap_digitec= Storage(name='Samsung Galaxy S9+', keyword='9017478', company="Digitec", price=float(499), date=datetime.datetime.now())

netgear = session.query(Product).filter(Product.name == 'Beoplay H4 Black')[0]
#net = Product(name = 'UE43NU7092', manufacturer='Samsung', manufacturer_id='UE43NU7092UXXH')

digitec = session.query(Company).filter(Company.name == 'Digitec')[0]
microspot = session.query(Company).filter(Company.name == 'Microspot')[0]
conrad = session.query(Company).filter(Company.name == 'Conrad')[0]

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

#tinte_digitec = session.query(ProductCompany).filter(ProductCompany.tag == '3230182').first()

#print(digitec_scraper.scrape_price(netgear))
#print(microspot_scraper.scrape_price(netgear))
#print(conrad_scraper.scrape_price(netgear))

#samsung = Product(name='Extreme 128GB', manufacturer='Sandisk', manufacturer_id='SDSQXA1-128G-GN6MA')
#session.add_all([ProductCompany(tag='6304953', product=netgear, company= digitec), ProductCompany(tag='0001485727', product=netgear, company= microspot)])
#session.add(samsung)
#digitec_scraper.scrape_by_manufacturer_tag(samsung)

for product in session.query(Product):
    plt.figure(product.id)
    plt.suptitle(product.name)
    for product_company in session.query(ProductCompany).filter(ProductCompany.product_id == product.id):
        prices = session.query(Price).filter(Price.product_company_id == product_company.id).order_by(asc(Price.date))
        if prices.count() == 0:
            continue
        last_price = prices[0]
        x = []
        y = []
        for price in prices:
            x.append(mdates.date2num(datetime.date(price.date.year, price.date.month, price.date.day)))
            y.append(price.price)

            if last_price.price != price.price:
                print("Product: %s \tCompany: %s \tID: %s"%(product.name, session.query(Company).get(product_company.company_id).name, product_company.tag))
                print("Price before: %f \tnow: %f \tdate: %s"%(last_price.price, price.price, price.date))
            last_price = price
        plt.plot(x, y, label=session.query(Company).get(product_company.company_id).name)
        #plt.plot([i for i in range(len(y))], y)
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%D')
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        #print(prices[-1].price)

plt.show()

#session.add(net)
session.commit()
session.close()
