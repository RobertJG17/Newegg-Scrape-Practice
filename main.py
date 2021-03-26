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
    url = 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709'
    tags = item_parse(url=url)

    lst = filter.item_info(tags)

    return f'{lst}'


@app.route('/cpu')
def cpu_index():
    url = 'https://www.newegg.com/CPUs-Processors/Category/ID-34'
    tags = item_parse(url=url)

    price, link, rating = filter.item_info(tags)

    df = pd.DataFrame(data=[price, link, rating], index=['Price', 'Link', 'Rating'])
    cpu_json = df.to_json()

    return cpu_json


if __name__ == '__main__':
    app.run()
