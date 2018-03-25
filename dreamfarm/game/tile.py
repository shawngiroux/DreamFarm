tile_ids = [

]

tile_textures = [
    {
        'name': 'corn',
        'tex': (14, 15)
    }
]

class Tile:
    id = 0
    x = 0
    y = 0

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
