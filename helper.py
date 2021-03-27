import requests
import bs4

import pandas as pd


def item_parse(url, part, pc_parts):

    # CPU-MOBO COMPATIBILITY CHECK
    if part == 'mobo':
        if 'LGA' in pc_parts[1]['name']:
            url = 'https://www.newegg.com/p/pl?d=motherboards&N=100007627&isdeptsrh=1'
        else:
            url = 'https://www.newegg.com/p/pl?d=motherboards&N=100007625&isdeptsrh=1'

    # STORING URL FOR SCRAPE
    result = requests.get(url)

    # SOUP OBJECT INSTANCE, PARSING WITH LXML
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    # CREATING ARRAY OF TAGS THAT CORRESPOND TO DIV TYPE WITH CLASS ITEM CONTAINER
    soup_tags = soup.findAll("div", {"class": "item-container"})
    return soup_tags


def top_match(tags, price, ratio):
    df = pd.DataFrame()

    # LOOPING THROUGH TAGS AND EXTRACTING PERTINENT INFORMATION
    for tag in tags:
        # USING RATIO AND TOTAL PRICE TO CALCULATE ALLOTMENT FOR PC PART
        price_point = price * ratio

        # CREATING KEY-VALUE PAIRING TO HOLD ATTRIBUTES OF PARTS
        obj = {}

        # ENSURING THAT THE INFORMATION WE ARE TRYING TO ACCESS EXISTS, IF NOT, IGNORE ITEM AND CONTINUE
        try:
            tag_name = tag.a.img.get("title")
            tag_href = tag.a.get("href")
            dollars = tag.find("li", {"class": "price-current"}).strong.text
            cents = tag.find("li", {"class": "price-current"}).sup.text
            tag_rating = tag.find("a", {"class": "item-rating"}).get("title")[-1]
        except AttributeError:
            continue

        obj['name'] = tag_name
        obj['price'] = float(f'{dollars}{cents}'.replace(',', ''))
        obj['href'] = f'{tag_href}'
        obj['rating'] = float(tag_rating)

        # APPEND ONLY THOSE PC PARTS THAT FALL UNDER OUR ALLOTTED AMOUNT
        if obj['price'] <= price_point:
            df = df.append(obj, ignore_index=True)

        

    df.sort_values(by="price", ascending=False, inplace=True, ignore_index=True)

    ret = df.iloc[0].to_dict()

    return ret


def parts_selector(price):
    # CPU, MOBO, RAM, GPU, SSD, CASE, PSU
    pc_parts = []
    price = float(price)

    # LINKS FROM NEWEGG
    newegg_parts = {
        'gpu': {'link': 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709', 'ratio': .38},
        'cpu': {'link': 'https://www.newegg.com/CPUs-Processors/Category/ID-34', 'ratio': .20},
        'ram': {'link': 'https://www.newegg.com/Desktop-Memory/SubCategory/ID-147?Tid=7611', 'ratio': .06},
        'ssd': {'link': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=119&Depa=1', 'ratio': .10},
        'psu': {'link': 'https://www.newegg.com/Power-Supplies/Category/ID-32?Tid=6656', 'ratio': .07},
        'mobo': {'link': None, 'ratio': .09},
        'cases': {'link': 'https://www.newegg.com/Computer-Cases/Category/ID-9?Tid=6644', 'ratio': .08}}

    for part in newegg_parts.keys():
        tags = item_parse(url=newegg_parts[f'{part}']['link'], part=part, pc_parts=pc_parts)
        top_part = top_match(tags=tags, price=price, ratio=newegg_parts[f'{part}']['ratio'])
        pc_parts.append(top_part)

    for part in pc_parts:
        print(part['name'], '\n')

    # pcpartpicker: https://pcpartpicker.com/list/, price: 1014.92
    return pc_parts

