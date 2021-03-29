from flask import Flask, request
from flask_cors import CORS
import helper

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'up n at em'


@app.route('/parts')
def build():
    price = request.args['price']
    return {"newegg_build": helper.parts_selector(price=price, site='newegg'),
            # "microcenter_build": helper.parts_selector(price=price, site='microcenter')
            }


if __name__ == '__main__':
    app.run()
