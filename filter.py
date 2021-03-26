def item_info(tags):
    corys_list = []
    index = 0
    for tag in tags:
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

        corys_list.append(obj)

    return corys_list
