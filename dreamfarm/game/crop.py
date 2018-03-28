from dreamfarm.game.textures import Textures

class Crop:
    lookup_by_id = []
    lookup_by_name = {}

    @staticmethod
    def create_lookups(data):
        for i in range(len(data)):
            Crop.lookup_by_id.append(data[i])
            Crop.lookup_by_name[data[i]] = i

    def __init__(self, name, x, y):
        self.id = Crop.lookup_by_name[name]
        self.x = x
        self.y = y
