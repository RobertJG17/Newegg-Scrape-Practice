import requests
import bs4

import pandas as pd


def item_parse(parts_url, part, pc_parts):
    # CPU-MOBO COMPATIBILITY CHECK
    if part == 'mobo':
        if 'LGA' in pc_parts[1]["name"]:
            parts_url = 'https://www.newegg.com/p/pl?d=motherboards&N=100007627&isdeptsrh=1'
        else:
            parts_url = 'https://www.newegg.com/p/pl?d=motherboards&N=100007625&isdeptsrh=1'

    # STORING URL FOR SCRAPE
    result = requests.get(parts_url)

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
            tag_img = tag.a.img.get("src")
            tag_href = tag.a.get("href")
            tag_num_of_ratings = \
                tag.find("span", {"class": "item-rating-num"}).text.replace('(', '').replace(')', '').replace(',', '')
            tag_dollars = tag.find("li", {"class": "price-current"}).strong.text
            tag_cents = tag.find("li", {"class": "price-current"}).sup.text
            tag_rating = tag.find("a", {"class": "item-rating"}).get("title")[-1]
        except AttributeError:
            continue

        # APPENDING ALL SCRAPED ATTRIBUTES TO A DICTIONARY
        obj["name"] = tag_name
        obj["price"] = float(f'{tag_dollars}{tag_cents}'.replace(',', ''))
        obj["href"] = f'{tag_href}'
        obj["rating"] = float(tag_rating)
        obj["image"] = tag_img
        obj["num_ratings"] = int(tag_num_of_ratings)

        # APPEND ONLY THOSE PC PARTS THAT FALL UNDER OUR ALLOTTED AMOUNT
        if obj["price"] <= price_point:
            df = df.append(obj, ignore_index=True)

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
    newegg_parts = {
        'gpu': {'link': 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7709',
                'ratio': {'gaming': .34, 'productivity': .38}},
        'cpu': {'link': 'https://www.newegg.com/CPUs-Processors/Category/ID-34',
                'ratio': {'gaming': .17, 'productivity': .20}},
        'ram': {'link': 'https://www.newegg.com/Desktop-Memory/SubCategory/ID-147?Tid=7611',
                'ratio': {'gaming': .06, 'productivity': .06}},
        'ssd': {'link': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=119&Depa=1',
                'ratio': {'gaming': .1, 'productivity': .10}},
        'hdd': {'link': 'https://www.newegg.com/p/pl?Submit=StoreIM&Category=15&Order=1',
                'ratio': {'gaming': .07, 'productivity': .07}},
        'psu': {'link': 'https://www.newegg.com/Power-Supplies/Category/ID-32?Tid=6656',
                'ratio': {'gaming': .07, 'productivity': .07}},
        'mobo': {'link': None,
                'ratio': {'gaming': .11, 'productivity': .09}},
        'cases': {'link': 'https://www.newegg.com/Computer-Cases/Category/ID-9?Tid=6644',
                'ratio': {'gaming': .08, 'productivity': .08}}}

    for part in sorted(newegg_parts.keys()):
        tags = item_parse(parts_url=newegg_parts[f'{part}']['link'], part=part, pc_parts=pc_parts)
        top_part = top_match(tags=tags, price=price, ratio=newegg_parts[f'{part}']['ratio']['gaming'])
        pc_parts.append(top_part)

    for part in pc_parts:
        print(part["name"], '\n')

    # pcpartpicker: https://pcpartpicker.com/list/, price: 1014.92
    return pc_parts
