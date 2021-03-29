import requests
import bs4

from scraper import scrape
from parts_info import newegg_parts, microcenter_parts


def compatibility_check(parts_url, part, pc_parts, site):
    # CPU-MOBO COMPATIBILITY CHECK
    if part == 'mobo' and site == 'newegg':
        if 'LGA' in pc_parts[1]["name"]:
            parts_url = 'https://www.newegg.com/Intel-Motherboards/SubCategory/ID-280?Tid=7627&PageSize=96'
        else:
            parts_url = 'https://www.newegg.com/AMD-Motherboards/SubCategory/ID-22?Tid=7625&PageSize=96'

    elif part == 'mobo' and site == 'microcenter':
        if 'LGA' in pc_parts[1]["name"]:
            parts_url = 'https://www.microcenter.com/category/4294966996,4294818573/intel-based-motherboards'
        else:
            parts_url = 'https://www.microcenter.com/search/search_results.aspx?N=4294966996+4294818892&NTK=all&sortby=match&rpp=96'
    return parts_url


def item_parse(parts_url, part, pc_parts, site):

    parts_url = compatibility_check(parts_url, part, pc_parts, site)

    # STORING URL FOR SCRAPE
    result = requests.get(parts_url)

    # SOUP OBJECT INSTANCE, PARSING WITH LXML
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    # CREATING ARRAY OF TAGS THAT CORRESPOND TO SPECIFIED TAG
    if site == 'newegg':
        soup_tags = soup.findAll("div", {"class": "item-container"})
    elif site == 'microcenter':
        soup_tags = soup.findAll("li", {"class": "product_wrapper"})
    else:
        soup_tags = ''

    return soup_tags


def top_match(tags, price, ratio, site):

    df = scrape(tags, site, price, ratio)

    # SORTING THE VALID PARTS BY PRICE IN DESCENDING ORDER
    print(df["name"])
    df.sort_values(by=["price", "num_ratings", "rating"], ascending=False, inplace=True, ignore_index=True)

    # RETURNING THE FIRST ROW OF OUR DATAFRAME (this is the most expensive product that doesn't exceed our price point)
    ret = df.iloc[0].to_dict()

    return ret


def parts_selector(price, site):
    # CPU, MOBO, RAM, GPU, SSD, CASE, PSU
    pc_parts = []
    price = float(price)

    # LINKS FROM NEWEGG
    if site == 'newegg':
        for part in sorted(newegg_parts.keys()):
            tags = item_parse(parts_url=newegg_parts[part]['link'], part=part, pc_parts=pc_parts, site=site)
            top_part = top_match(tags=tags, price=price, ratio=newegg_parts[part]['ratio']['gaming'], site=site)
            pc_parts.append(top_part)
        print("NEWEGG BUILD:")
        for part in pc_parts:
            print(part["name"], '\n')

    if site == 'microcenter':
        for part in sorted(microcenter_parts.keys()):
            tags = item_parse(parts_url=microcenter_parts[part]['link'], part=part, pc_parts=pc_parts, site=site)
            top_part = top_match(tags=tags, price=price, ratio=microcenter_parts[part]['ratio']['gaming'], site=site)
            pc_parts.append(top_part)
        print("MICROCENTER BUILD:")
        for part in pc_parts:
            print(part["name"], '\n')

    # pcpartpicker: https://pcpartpicker.com/list/, price: 1014.92 comment
    return pc_parts
