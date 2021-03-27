from flask import Flask, request
from flask_cors import CORS
import helper

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    price = request.args['price']
    return {"parts": helper.parts_selector(price)}


if __name__ == '__main__':
    app.run()
