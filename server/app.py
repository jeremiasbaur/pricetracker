import json, datetime, random

from flask import Flask, jsonify, request
from flask_cors import CORS
from datastructures import Product, ProductCompany, Price, Company, PriceChanges, PriceChangesSimple, BaseSimple, AlchemyEncoder, Base

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

engine = create_engine('postgres://hdlubjhvpibagw:68fde9cba5c79eeca8eba0c52528f095ca1ffb912c12095104ce03809b8f2939@ec2-54-247-178-166.eu-west-1.compute.amazonaws.com:5432/d3p7ql5olgpc0j')
big_engine = create_engine('postgresql://postgres:admin@localhost:5432/pricetracker_database')
BaseSimple.metadata.create_all(engine)
Base.metadata.create_all(big_engine)

Session = sessionmaker()
session = Session(bind=engine)
bigsession = Session(bind=big_engine)

@app.route('/prices', methods=['GET'])
def prices():
    last_price_change = session.query(PriceChangesSimple).order_by(PriceChangesSimple.date.desc()).first()

    today = datetime.datetime(last_price_change.date.year, last_price_change.date.month, last_price_change.date.day)

    query = session.query(PriceChangesSimple).\
                filter(PriceChangesSimple.date >= today).order_by(PriceChangesSimple.percent_change.desc()).all()

    response_object = {'status': 'success'}
    response_object['prices'] = query

    return json.dumps(response_object, cls=AlchemyEncoder)

@app.route('/api/v1/prices/<string:shop>/<string:product_id>/<int:id_type>', methods=['GET'])
def get_product(shop, product_id, id_type):
    """
    Return top price and its shop of requested product
    via either shop id (id_type 0) or manufacturer id (id_type 1)
    :param shop: current shop
    :param product_id: shop id or manufacturer id set per id_type
    :param id_type: shop id (id_type 0) or manufacturer id (id_type 1)
    :return: Return top price and its shop of requested product
    """
    shops = {'digitec':1, 'microspot':2, 'conrad':3, 'pcostschweiz':4}
    try:
        if shop in shops:
            if id_type == 0:
                og_pc = bigsession.query(ProductCompany).filter(and_(ProductCompany.tag == product_id, ProductCompany.company_id == shops[shop])).first()

                if og_pc is None:
                    return json.dumps({'error': 404, 'message': 'Product not found in DB'})

                pcs = bigsession.query(ProductCompany)\
                        .filter(ProductCompany.product_id == og_pc.product_id).all()

                best_price = -1

                for pc in pcs:
                    pc_price = bigsession.query(Price) \
                        .filter(Price.product_company_id == pc.id) \
                        .order_by(Price.date.desc()) \
                        .first()

                    if isinstance(best_price, int) or pc_price.price < best_price.price:
                        best_price = pc_price

                pc_best = bigsession.query(ProductCompany).filter(ProductCompany.id == best_price.product_company_id).first()

            response_object = {'status': 'success'}
            response_object['shop'] = pc_best.company.name
            response_object['product_id'] = product_id
            response_object['top_price'] = best_price.price
            response_object['url'] = pc_best.url

            return json.dumps(response_object, cls=AlchemyEncoder)
        else:
            return json.dumps({'error': 404, 'message': 'Shop not found'})
    except Exception as e:
        print("Error:", e)
        return json.dumps({'error': 404, 'message': 'An unknown error occurred'})


"""def prices_adv():
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

    return json.dumps(response_object, cls=AlchemyEncoder)"""

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        session.close()
        bigsession.close()
