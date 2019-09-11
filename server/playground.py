import jsonpickle, json, datetime

from datastructures import Product, ProductCompany, Price, Company, PriceChanges, AlchemyEncoder

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, aliased
from sqlalchemy import and_, create_engine



engine = create_engine('postgresql://postgres:admin@localhost:5432/pricetracker_database')

session = sessionmaker(engine)
session = session()

Base = declarative_base()
Base.metadata.create_all(engine)

p_alias = aliased(Price)

lol = session.query(PriceChanges, ProductCompany, Product, Price, p_alias).\
            filter(PriceChanges.date > datetime.datetime.today()-datetime.timedelta(days=1)).\
            join(ProductCompany, PriceChanges.product_company_id == ProductCompany.id).\
            join(Product, ProductCompany.product_id == Product.id).\
            join(Price, PriceChanges.price_yesterday_id == Price.id).\
            join(p_alias, PriceChanges.price_today_id == p_alias.id).order_by(PriceChanges.percent_change.desc()).all()

print(lol)

print(json.dumps(lol, cls=AlchemyEncoder))
