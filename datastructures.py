from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

"""class Product(Base):
    __tablename__ = 'product'
    id = Column('id', Integer, primary_key=True)
    company_id = Column('company_id', Integer, ForeignKey('company.id'), nullable=False)
    #company = relationship('Company', backref='company.id')
    #price_id = Column('price_id', Integer, ForeignKey('price_date.id'), nullable=False)
    price = relationship('PriceDate', back_populates='product_id')
    name = Column(String)
    keyword = Column(String)

    def __init__(self, name=None, keyword=None, company=None, price=None):
        self.name = name
        self.keyword = keyword
        self.company = company
        self.price = price

class Company(Base):
    __tablename__ = 'company'
    id = Column('id', Integer, primary_key=True)
    products = relationship(Product)
    name = Column(String)
    scrape_url = Column(String)
    url = Column(String)

    def __init__(self, name=None, scrape_url=None, url=None):
        self.name = name
        self.scrape_url = scrape_url
        self.url = url

class PriceDate(Base):
    __tablename__ = 'price_date'
    id = Column('id', Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    date = Column('date', DateTime)
    price = Column('price', Float)

    def __init__(self, product_id=None, date=None, price=None):
        self.product_id = product_id
        self.date = date
        self.price = price
"""
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

class Company(Base):
    __tablename__ = 'company'
    id = Column('id', Integer, primary_key=True)
    name = Column(String, nullable=False)

class Price(Base):
    __tablename__ = 'price'
    id = Column('id', Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)


class ProductCompany(Base):
    __tablename__ = 'product_of_company'
    id = Column('id', Integer, primary_key=True)


engine = create_engine('postgresql://pricetracker:trackit@localhost:5432/pricetracker_database')
Base.metadata.create_all(engine)

session = sessionmaker(engine)
session = session()

#ap_digitec= Storage(name='Samsung Galaxy S9+', keyword='9017478', company="Digitec", price=float(499), date=datetime.datetime.now())

#session.add(ap_digitec)
session.commit()
