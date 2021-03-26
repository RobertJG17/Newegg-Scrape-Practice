import bs4
import requests
import pandas as pd
from flask import Flask, current_app
import filter

app = Flask(__name__)


def item_parse(url):
    # FROM NEWEGG
    result = requests.get(url)

    # HTML PARSER
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    soup_tags = soup.findAll("div", {"class": "item-container"})
    return soup_tags


@app.route('/')
def index():
    url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38'
    tags = item_parse(url=url)
    print(filter.item_info(tags))

    return 'yellow'


# @app.route('/cpu')
# def cpu_index():
#     tags = graphics_card_parse()
#     for tag in tags:
#         print(f'{tag.a.img.get("title")}, ${tag.find("li", {"class": "price-current"}).strong.text}'
#               f'{tag.find("li", {"class": "price-current"}).sup.text}')
#
#     return 'yellow'


if __name__ == '__main__':
    app.run()
