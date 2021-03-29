from flask import Flask, request
from flask_cors import CORS
import helper
import os
import parts_info

app = Flask(__name__)
CORS(app)

os.environ['newegg_parts'] = parts_info.newegg_parts
os.environ['microcenter_parts'] = parts_info.microcenter_parts


@app.route('/')
def index():
    return 'up n at em'


@app.route('/parts')
def build():
    price = request.args['price']
    return {"newegg_build": helper.parts_selector(price=price, site='newegg'),
            "microcenter_build": helper.parts_selector(price=price, site='microcenter')
            }


if __name__ == '__main__':
    app.run()
