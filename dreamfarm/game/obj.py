from dreamfarm.game.textures import Textures

class Obj:
    lookup_by_id = []
    lookup_by_name = {}

    @staticmethod
    def create_lookups(data):
        for i in range(len(data)):
            Obj.lookup_by_id.append(data[i])
            Obj.lookup_by_name[data[i]] = i

    def __init__(self, name, x, y):
        self.id = Obj.lookup_by_name[name]
        self.x = x
        self.y = y
