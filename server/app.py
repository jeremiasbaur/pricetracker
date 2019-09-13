import json, datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from datastructures import Product, ProductCompany, Price, Company, PriceChanges, AlchemyEncoder

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, aliased
from sqlalchemy import and_, create_engine

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

Base = declarative_base()
engine = create_engine('postgresql://postgres:admin@localhost:5432/pricetracker_database')
Base.metadata.create_all(engine)

session = sessionmaker(engine)
session = session()

@app.route('/prices', methods=['GET'])
def prices():
    last_price_change = session.query(PriceChanges).order_by(PriceChanges.date.desc()).first()

    p_alias = aliased(Price)
    delta = datetime.timedelta(days=1)
    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)

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

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()
    session.close()
