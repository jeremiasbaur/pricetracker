import json, datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from datastructures import Product, ProductCompany, Price, Company, PriceChanges, AlchemyEncoder

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, aliased
from sqlalchemy import and_, create_engine

# configuration
DEBUG = False

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

Base = declarative_base()
engine = create_engine('postgres://hdlubjhvpibagw:68fde9cba5c79eeca8eba0c52528f095ca1ffb912c12095104ce03809b8f2939@ec2-54-247-178-166.eu-west-1.compute.amazonaws.com:5432/d3p7ql5olgpc0j')
Base.metadata.create_all(engine)

session = sessionmaker(engine)
session = session()

@app.route('/prices', methods=['GET'])
def prices():
    last_price_change = session.query(PriceChanges).order_by(PriceChanges.date.desc()).first()

    p_alias = aliased(Price)
    delta = datetime.timedelta(days=1)
    today = datetime.datetime(last_price_change.date.year, last_price_change.date.month, last_price_change.date.day)

    if(last_price_change.date < datetime.datetime.today()-delta):
        delta = datetime.timedelta(days=2)

    query = session.query(PriceChanges, ProductCompany, Product, Price, p_alias).\
                filter(PriceChanges.date >= today).\
                join(ProductCompany, PriceChanges.product_company_id == ProductCompany.id).\
                join(Product, ProductCompany.product_id == Product.id).\
                join(Price, PriceChanges.price_yesterday_id == Price.id).\
                join(p_alias, PriceChanges.price_today_id == p_alias.id).order_by(PriceChanges.percent_change.desc()).all()

    response_object = {'status': 'success'}
    response_object['prices'] = query

    return json.dumps(response_object, cls=AlchemyEncoder)


if __name__ == '__main__':
    try:
        app.run()
    finally:
        session.close()
