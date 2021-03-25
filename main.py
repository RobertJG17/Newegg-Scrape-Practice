import bs4
import requests
import pandas as pd
from flask import Flask, current_app

app = Flask(__name__)


def graphics_card_parse():
    # FROM NEWEGG
    result_ngc = requests.get('https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38')

    # HTML PARSER
    soup = bs4.BeautifulSoup(result_ngc.text, 'lxml')
    print(soup.prettify())

    return soup.findAll("div", {"class": "item-container"})


@app.route('/')
def index():
    containers = graphics_card_parse()
    container_info = []

    #for container in containers:
    #   print(container.a.img.get('title'))

    return 'yellow'


if __name__ == '__main__':
    app.run()


