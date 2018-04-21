import json
import os

class Shop:
    items = json.load(open(os.path.realpath('./dreamfarm/game/data/items.json')))

    def getShopItems(self):
        item_types = []
        for names in self.items:
            item_types.append(names)
        return item_types

    def getItemsArray(self, item_name):
        return self.items[item_name]['data']['levels']

# shop = Shop()
# shop.getAxes()
# shop = Shop()
# response = "**Item Types**:\n"
# item_types = shop.getShopItems()
# for i, item_name in enumerate(item_types):
#     response += "**{0}**) {1}\n".format(i+1, item_name)