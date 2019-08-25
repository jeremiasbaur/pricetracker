import jsonpickle, json, datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from datastructures import Product, ProductCompany, Price, Company, PriceChanges, AlchemyEncoder

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/prices', methods=['GET'])
def prices():
    started = datetime.datetime.now()
    query = session.query(PriceChanges, ProductCompany, Product, Price)\
        .filter(and_(PriceChanges.date > datetime.datetime.today()-datetime.timedelta(days=1),\
                     PriceChanges.product_company_id == ProductCompany.id,\
                     Product.id == ProductCompany.product_id,\
                     PriceChanges.price_yesterday_id == Price.id))\
        .order_by(PriceChanges.percent_change.desc()).all()
    print(datetime.datetime.now()-started)
    started = datetime.datetime.now()
    #query = session.query(PriceChanges)\
    #    .filter(and_(PriceChanges.date < datetime.datetime.today(), PriceChanges.date > datetime.datetime.today()-datetime.timedelta(days=1)))\
    #    .order_by(PriceChanges.percent_change.desc()).all()
    response_object = {'status': 'success'}
    response_object['prices'] = query

    print(json.dumps(query[1], cls=AlchemyEncoder))
    lol = json.dumps(response_object, cls=AlchemyEncoder)
    print(datetime.datetime.now()-started)
    return lol

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
