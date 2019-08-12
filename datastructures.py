from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, create_engine, Float, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

# after pull:
# psql -U postgres -c "drop database pricetracker_database;"
# psql -U postgres -c "create database pricetracker_database with owner postgres encoding = 'UNICODE';"
# psql -U postgres -d pricetracker_database -f pricetracker_database.sql

#before commit:
# pg_dump -U postgres -O pricetracker_database > pricetracker_database.sql

# https://wiki-bsse.ethz.ch/display/ITDOC/Copy+PostgreSQL+database+between+computers

Base = declarative_base()

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

    def __init__(self, price=None, date=None):
        self.price = price
        self.date = date
