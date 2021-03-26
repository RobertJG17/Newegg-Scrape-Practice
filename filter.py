def item_info(tags):
    for tag in tags:
        name = tag.a.img.get("title")
        try:
            dollars = tag.find("li", {"class": "price-current"}).strong.text
            cents = tag.find("li", {"class": "price-current"}).sup.text
        except AttributeError:
            dollars = None
            cents = None

        if dollars is not None and cents is not None:
            info_str = f'{name}, ${dollars}{cents}'
        else:
            info_str = f'{name}, Out Of Stock'

        return info_str
