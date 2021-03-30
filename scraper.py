import pandas as pd


def set_structure(site,
                  tag_name, tag_img, tag_href, tag_num_of_ratings,
                  tag_dollars, tag_cents, tag_rating, tag_price):

    # APPENDING ALL SCRAPED ATTRIBUTES TO A DICTIONARY
    obj = {"name": tag_name}

    if site == 'newegg':
        obj["price"] = float(f'{tag_dollars}{tag_cents}'.replace(',', ''))
        obj["href"] = f'{tag_href}'
    elif site == 'microcenter':
        obj["price"] = float(tag_price)
        obj["href"] = f'https://www.microcenter.com{tag_href}'

    try:
        obj["num_ratings"] = int(tag_num_of_ratings.replace('reviews', '').lstrip(' ').rstrip(' '))
    except ValueError:
        obj["num_ratings"] = int(tag_num_of_ratings.replace('review', '').lstrip(' ').rstrip(' '))

    obj["rating"] = float(tag_rating[0])
    obj["image"] = tag_img

    return obj


def scrape(tags, site, price, ratio):

    df = pd.DataFrame()

    # LOOPING THROUGH TAGS AND EXTRACTING PERTINENT INFORMATION
    for tag in tags:
        # USING RATIO AND TOTAL PRICE TO CALCULATE ALLOTMENT FOR PC PART
        price_point = price * ratio

        # CREATING KEY-VALUE PAIRING TO HOLD ATTRIBUTES OF PARTS

        (tag_name, tag_img, tag_href, tag_num_of_ratings, tag_dollars, tag_cents, tag_rating, tag_price) = \
            (None, None, None, None, None, None, None, None)

        if site == 'newegg':
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

        elif site == 'microcenter':
            try:
                tag_name = tag.find("a", {"class": "image"}).get("data-name")
                tag_img = tag.find("img", {"class": "SearchResultProductImage"}).get("src")
                tag_href = tag.find("a", {"class": "image"}).get("href")
                tag_num_of_ratings = tag.find("div", {"class": "ratingstars"}).div.span.text.replace('(', '').replace(')', '').replace(',', '')
                tag_price = tag.find("a", {"class": "image"}).get("data-price")
                tag_rating = tag.find("img", {"class": "imgReviews"}).get("alt")
            except AttributeError:
                continue

        obj = set_structure(site,
                  tag_name, tag_img, tag_href, tag_num_of_ratings,
                  tag_dollars, tag_cents, tag_rating, tag_price)

        # APPEND ONLY THOSE PC PARTS THAT FALL UNDER OUR ALLOTTED AMOUNT
        if obj["price"] <= price_point:
            df = df.append(obj, ignore_index=True)

    return df
