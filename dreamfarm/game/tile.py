class Tile:
    lookup_by_id = []
    lookup_by_name = {}

    @staticmethod
    def create_lookups(data):
        for i in range(len(data)):
            Tile.lookup_by_id.append(data[i])
            Tile.lookup_by_name[data[i]] = i

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
