from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Float, asc
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import relationship, sessionmaker
import datetime, json

# after pull:
# psql -U postgres -c "drop database pricetracker_database;"
# psql -U postgres -c "create database pricetracker_database with owner postgres encoding = 'UNICODE';"
# psql -U postgres -d pricetracker_database -f pricetracker_database.sql

#before commit:
# pg_dump -U postgres -O pricetracker_database > pricetracker_database.sql

# https://wiki-bsse.ethz.ch/display/ITDOC/Copy+PostgreSQL+database+between+computers

Base = declarative_base()
BaseSimple = declarative_base()

class Storage(Base):
    __tablename__ = 'storage'
    id = Column('id', Integer, primary_key=True)
    company = Column('company', String, nullable=False)
    name = Column('name', String)
    keyword = Column('keyword', String)
    date = Column('date', DateTime)
    price = Column('price', Float)

    def __init__(self, name=None, keyword=None, company=None, price=None, date=None):
        self.name = name
        self.keyword = keyword
        self.company = company
        self.price = price
        self.date = date

class Product(Base):
    __tablename__ = 'product'
    id = Column('id', Integer, primary_key=True)

    name = Column(String, nullable=False)
    manufacturer = Column(String)
    manufacturer_id = Column(String)

    url_image = Column(String)
    product_offered = relationship('ProductCompany', back_populates='product') # One to many with ProductCompany with backlinking

    def __int__(self, name=None, manufacturer=None, manufacturer_id=None):
        self.name = name
        self.manufacturer = manufacturer
        self.manufacturer_id = manufacturer_id

class Company(Base):
    __tablename__ = 'company'
    id = Column('id', Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String)
    scrape_url = Column(String, nullable=False)

    stock = relationship('ProductCompany', back_populates='company') # One to many with ProductCompany with backlinking

    def __init__(self, name=None, url=None, scrape_url=None):
        self.name = name
        self.url = url
        self.scrape_url = scrape_url

class ProductCompany(Base):
    __tablename__ = 'product_company'
    id = Column('id', Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship(Product, back_populates='product_offered')

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship(Company, back_populates='stock') # backlinking

    tag = Column(String, nullable=False)
    url = Column(String)

    prices = relationship("Price") # One to many with prices

    def __int__(self, tag=None, product=None, company=None):
        self.tag = tag
        self.product = product
        self.company = company

class Price(Base):
    __tablename__ = 'price'
    id = Column('id', Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    product_company_id = Column(Integer, ForeignKey('product_company.id'))

    #price_changes = relationship("PriceChanges")

    def __init__(self, price=None, date=None):
        self.price = price
        self.date = date

class PriceChanges(Base):
    __tablename__ = 'price_changes'
    id = Column('id', Integer, primary_key=True)

    date = Column(DateTime, nullable=False)
    percent_change = Column(Float, nullable=False)

    product_company_id = Column(Integer, ForeignKey('product_company.id'))
    #product_company = relationship(Price, back_populates='product_company')

    price_today_id = Column(Integer, ForeignKey('price.id'))
    #price_today = relationship(Price, foreign_keys=[price_today_id]) # backlinking

    price_yesterday_id = Column(Integer, ForeignKey('price.id'))
    #price_yesterday = relationship(Price, foreign_keys=[price_yesterday_id]) # backlinking

    def __init__(self,  date = None, product_company_id = None, price_today_id = None, price_yesterday_id = None, percent_change = None):
        #self.percent_change = price_today.price/price_yesterday.price
        self.price_today_id = price_today_id
        self.price_yesterday_id = price_yesterday_id
        self.product_company_id = product_company_id
        self.percent_change = percent_change

        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = date


class PriceChangesSimple(BaseSimple):
    __tablename__ = 'price_changes'
    id = Column('id', Integer, primary_key=True)

    date = Column(DateTime, nullable=False)
    percent_change = Column(Float, nullable=False)

    product_company_url = Column(String)
    product_manufacturer = Column(String)
    product_name = Column(String)
    product_tag = Column(String)
    product_url_image = Column(String)

    price_today = Column(Float)
    price_yesterday = Column(Float)

    def __init__(self,  date = None, product_company = None, product = None, price_today = None, price_yesterday = None):
        #self.percent_change = price_today.price/price_yesterday.price
        self.price_today = price_today.price
        self.price_yesterday = price_yesterday.price
        self.product_company_url = product_company.url
        self.percent_change = 2 - self.price_today / self.price_yesterday

        self.product_name = product.name
        self.product_manufacturer = product.manufacturer
        self.product_tag = product.manufacturer_id
        self.product_url_image = product.url_image

        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = date

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, datetime.date):
                        json.dumps(data.isoformat())
                        fields[field] = data.isoformat()
                    else:
                        json.dumps(data) # this will fail on non-encodable values, like other classes
                        fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
