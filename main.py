from flask import Flask

import helper

app = Flask(__name__)


@app.route('/')
def index():
    return f'{helper.parts_selector()}'


if __name__ == '__main__':
    app.run()
