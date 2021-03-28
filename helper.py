import requests
import bs4

import pandas as pd
from scraper import scrape
from parts_info import newegg_parts, microcenter_parts


def item_parse(parts_url, part, pc_parts, site):
    # CPU-MOBO COMPATIBILITY CHECK
    if part == 'mobo' and site is 'newegg':
        if 'LGA' in pc_parts[1]["name"]:
            parts_url = 'https://www.newegg.com/p/pl?d=motherboards&N=100007627&isdeptsrh=1'
        else:
            parts_url = 'https://www.newegg.com/p/pl?d=motherboards&N=100007625&isdeptsrh=1'

    elif part == 'mobo' and site is 'microcenter':
        if 'LGA' in pc_parts[1]["name"]:
            parts_url = 'https://www.microcenter.com/category/4294966996,4294818573/intel-based-motherboards'
        else:
            parts_url = 'https://www.microcenter.com/search/search_results.aspx?N=4294966996+4294818892&NTK=all&sortby=match&rpp=96'

    # STORING URL FOR SCRAPE
    result = requests.get(parts_url)

    # SOUP OBJECT INSTANCE, PARSING WITH LXML
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    # CREATING ARRAY OF TAGS THAT CORRESPOND TO SPECIFIED TAG
    if site is 'newegg':
        soup_tags = soup.findAll("div", {"class": "item-container"})
    elif site is 'microcenter':
        soup_tags = soup.findAll("li", {"class": "product_wrapper"})
    else:
        soup_tags = ''

    return soup_tags


def top_match(tags, price, ratio, site):

    df = scrape(tags, site, price, ratio)

    # SORTING THE VALID PARTS BY PRICE IN DESCENDING ORDER
    df.sort_values(by=["price", "num_ratings", "rating"], ascending=False, inplace=True, ignore_index=True)

    # RETURNING THE FIRST ROW OF OUR DATAFRAME (this is the most expensive product that doesn't exceed our price point)
    ret = df.iloc[0].to_dict()

    return ret


def parts_selector(price):
    # CPU, MOBO, RAM, GPU, SSD, CASE, PSU
    pc_parts = []
    price = float(price)

    # LINKS FROM NEWEGG

    # for part in sorted(newegg_parts.keys()):
    #     tags = item_parse(parts_url=newegg_parts[f'{part}']['link'], part=part, pc_parts=pc_parts, site='newegg')
    #     top_part = top_match(tags=tags, price=price, ratio=newegg_parts[f'{part}']['ratio']['gaming'], site='newegg')
    #     pc_parts.append(top_part)

    for part in sorted(microcenter_parts.keys()):
        tags = item_parse(parts_url=microcenter_parts[f'{part}']['link'], part=part, pc_parts=pc_parts, site='microcenter')
        top_part = top_match(tags=tags, price=price, ratio=microcenter_parts[f'{part}']['ratio']['gaming'], site='microcenter')
        pc_parts.append(top_part)

    for part in pc_parts:
        print(part["name"], '\n')

    # pcpartpicker: https://pcpartpicker.com/list/, price: 1014.92 comment
    return pc_parts
