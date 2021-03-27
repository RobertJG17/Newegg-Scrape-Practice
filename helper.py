import pandas as pd


def top_match(tags, price, ratio):
    df = pd.DataFrame()

    for tag in tags:
        price_point = price * ratio
        obj = {}

        tag_name = tag.a.img.get("title")
        tag_href = tag.a.get("href")

        try:
            dollars = tag.find("li", {"class": "price-current"}).strong.text
            cents = tag.find("li", {"class": "price-current"}).sup.text
            tag_rating = tag.find("a", {"class": "item-rating"}).get("title")[-1]
        except AttributeError:
            continue

        obj['name'] = tag_name
        obj['price'] = float(f'{dollars}{cents}'.replace(',', ''))
        obj['href'] = f'{tag_href}'
        obj['rating'] = float(tag_rating)

        if obj['price'] <= price_point:
            df = df.append(obj, ignore_index=True)

    df.sort_values(by="price", ascending=False, inplace=True, ignore_index=True)
    ret = df.iloc[0].to_dict()

    return ret

