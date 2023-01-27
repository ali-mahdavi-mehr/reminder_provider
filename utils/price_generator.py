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


def number_generator(price):
    route = f"price init is ({price}) changed to string\n"
    price = str(price).lower()
    if price == "none":
        route += f"price is none({price})\n"
        return "--"

    if "e" in price:
        route += f"price has e({price})\n"
        price = "{:.10f}".format(float(price))
        route += f"price changed e({price})\n"
        return price

    route += f"price ({price}) changed to string\n"
    sahih, kasr = price.split(".") if "." in price else (str(price), str(0))
    route += f"get sahih({sahih}) and kasr({kasr})\n"
    n = sahih.replace("-", "")
    route += f"remove - {n}\n"

    nums = len(n)
    route += f"nums length ({nums})\n"

    if int(sahih) == 0:
        price = round(float(price), 5)
        route += f"price lower than 0 ({price})\n"
        return price
    elif nums < 4:
        price = round(float(price), 3)

    elif nums in [4, 5, 6]:
        price = f"{sahih[0:-3]}.{sahih[-3:]}K"


    elif nums in [7, 8, 9]:
        price = f"{sahih[0:-6]}.{sahih[-6:-3]}M"

    elif nums in [10, 11, 12]:
        price = f"{sahih[0:-9]}.{sahih[-9:-6]}B"

    elif nums in [13, 14, 15]:
        price = f"{sahih[0:-12]}.{sahih[-12:-9]}T"
    return price
