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
    return {
            "microcenter_build": helper.parts_selector(price=price, site='microcenter'),
            "newegg_build": helper.parts_selector(price=price, site='newegg')}


if __name__ == '__main__':
    app.run()
