import json
import os

class Shop:
    items = json.load(open(os.path.realpath('./dreamfarm/game/data/items.json')))

    def getShopItems(self):
        item_types = []
        for names in self.items:
            item_types.append(names)
        return item_types