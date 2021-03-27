from flask import Flask, request

import helper

app = Flask(__name__)


@app.route('/')
def index():
    price = request.args['price']
    return f'{helper.parts_selector(price)}'


if __name__ == '__main__':
    app.run()
