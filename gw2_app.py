import sys
import os
import requests
import gw2_app_support

url_base = "https://api.guildwars2.com/v2/"
url_item = "https://api.guildwars2.com/v2/items/"
url_tp = "https://api.guildwars2.com/v2/commerce/prices/"
mc_venom = {}


# def get_material_stocks():
#     r.get = requests(url_base.format(""))

def format_currency(val):
    value = str(val)

    if val < 100:
        price = "{}c".format(value[-2:])
    elif val in range(100, 10000):
        price = "{}s{}c".format(value[-4:-2:1], value[-2:])
    else:
        price = "{}g{}s{}c".format(value[:-4], value[-4:-2:1], value[-2:])

    return price


def get_item_name(item_id):
    url = "{}{}".format(url_item, item_id)
    r = requests.get(url)
    name = r.json()
    return name["name"]


def get_price_buy(item_id):
    url = "{}{}".format(url_tp, item_id)
    r = requests.get(url)
    listing = r.json()
    return listing["buys"]["unit_price"]


def get_price_sell(item_id):
    url = "{}{}".format(url_tp, item_id)
    r = requests.get(url)
    listing = r.json()
    return listing["sells"]["unit_price"]


def get_mystic_curios(base, index):
    indices = ["name", "price", "ingredient1", "qty1", "price1", "ingredient2", "qty2", "price2", "ingredient3", "qty3", "price3"]
    data = []
    url = "{}recipes/{}".format(base, index)
    r = requests.get(url)
    recipe = r.json()
    item_name = get_item_name(recipe["output_item_id"])
    components = recipe["ingredients"]
    data.append("{} ({})".format(item_name, get_item_name(components[0]["item_id"])))
    data.append(format_currency(get_price_sell(recipe["output_item_id"])))
    total_crafting_cost = 0

    for object in components:
        data.append(get_item_name(object["item_id"]))
        data.append(object["count"])
        data.append(format_currency(get_price_buy(object["item_id"])))
        total_crafting_cost = total_crafting_cost + ((int(object["count"])) * int(get_price_buy(object["item_id"])))

    item = dict(zip(indices, data))
    print(indices)
    print(data)
    profit = (get_price_sell(recipe["output_item_id"]) - total_crafting_cost)
    print("Total crafting cost: {}".format(format_currency(total_crafting_cost)))
    print("Item price: {}".format(item["price"]))
    print("Profit: {}".format(format_currency(profit)))


mystic_curio = {}


for x in range(len(gw2_app_support.mystic_curio_list)):
    get_mystic_curios(url_base, gw2_app_support.mystic_curio_list[x])
