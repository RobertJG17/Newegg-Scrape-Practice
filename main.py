import bs4
import requests
import helper

from flask import Flask, current_app, request


app = Flask(__name__)


def item_parse(url):
    result = requests.get(url)

    # HTML PARSER
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    soup_tags = soup.findAll("div", {"class": "item-container"})
    return soup_tags


@app.route('/')
def index():
    price = request.args['price']
    price = float(price)
    # CPU, MOBO, RAM, GPU, SSD, CASES, PSU
    pc_parts = []

    # LINKS FROM NEWEGG
    parts = {'gpu': {'link': 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709', 'ratio': .38},
             'cpu': {'link': 'https://www.newegg.com/CPUs-Processors/Category/ID-34', 'ratio': .20},
             'ram': {'link': 'https://www.newegg.com/Desktop-Memory/SubCategory/ID-147?Tid=7611', 'ratio': .06},
             'ssd': {'link': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=119&Depa=1', 'ratio': .10},
             'psu': {'link': 'https://www.newegg.com/Power-Supplies/Category/ID-32?Tid=6656', 'ratio': .07},
             'mobo': {'link': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=20&Depa=1', 'ratio': .09},
             'cases': {'link': 'https://www.newegg.com/Computer-Cases/Category/ID-9?Tid=6644', 'ratio': .08}}

    for part in parts.keys():
        tags = item_parse(url=parts[f'{part}']['link'])
        top_part = helper.top_match(tags, price=price, ratio=parts[f'{part}']['ratio'])
        pc_parts.append(top_part)

    # for part in pc_parts:
        # print(part['name'], '\n')

    # pcpartpicker: https://pcpartpicker.com/list/, price: 1014.92

    return f'{pc_parts}'


if __name__ == '__main__':
    app.run()
