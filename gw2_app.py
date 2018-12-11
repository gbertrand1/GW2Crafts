import sys
import os
import requests
import gw2_app_support

url_base = "https://api.guildwars2.com/v2/"
url_item = "https://api.guildwars2.com/v2/items/"
mc_venom = {}


# def get_material_stocks():
#     r.get = requests(url_base.format(""))

def get_item_name(item_id):
    url = "{}{}".format(url_item, item_id)
    r = requests.get(url)
    print(r.url)
    name = r.json()
    return name["name"]


def get_mystic_curios(base):
    url = "{}recipes/{}".format(base, gw2_app_support.mystic_curio_list[0])
    r = requests.get(url)
    recipe = r.json()
    name = get_item_name(recipe["output_item_id"])
    print(name)
    components = recipe["ingredients"]
    name = get_item_name(components[0]["item_id"])
    print(name)
    print(components)


get_mystic_curios(url_base)
