def price_seperator(price):
    if type(price) is not float:
        price = round(float(price), 10)
    mines = False

    if "e" in str(price).lower():
        price = format(price, '.10f')
        return price

    if (price * -1) > 1:
        price *= -1
        mines = True
    if price > 0:
        price = round(price, 3)

    result = f'{price:,}'
    if mines:
        result = "-" + result
    return result