import pickle
import bz2
import io
import os
from PIL import Image
from dreamfarm.game.tile import Tile
from dreamfarm.game.textures import Textures

# Convert grid notation (A1, D12, etc.) to tile indices
def coords_to_indices(coords):
    return (0, 0)

class Plot:
    tiles = []

    def __init__(self):
        # Initialize a 2D array of Tiles with dimensions 16x20
        self.tiles = []
        for y in range(16):
            self.tiles.append([])
            for x in range(20):
                self.tiles[y].append(Tile(0, x, y))

    def get_tile_data(self):
        return bz2.compress(pickle.dumps(self.tiles))

    def set_tile_data(self, data):
        self.tiles = pickle.loads(bz2.decompress(data))

    def set_tile(self, coords, id):
        return 0

    def render(self):
        img = Image.new('RGBA', (16 * 20, 16 * 16))
        for y in range(16):
            for x in range(20):
                id = self.tiles[y][x].id
                tex = Textures.get_image(id)
                x1 = x * 16
                x2 = x1 + 16
                y1 = y * 16
                y2 = y1 + 16
                img.paste(tex, (x1, y1, x2, y2))
        ret = io.BytesIO()
        img.save(ret, format='PNG')
        ret.seek(0)
        return ret
