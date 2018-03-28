import pickle
import bz2
import io
import os
from PIL import Image
from dreamfarm.game.tile import Tile
from dreamfarm.game.crop import Crop
from dreamfarm.game.textures import Textures

# Convert grid notation (A1, D12, etc.) to tile indices
def coords_to_indices(coords):
    return (0, 0)

class Plot:
    def __init__(self):
        self.tiles = []
        self.crops = []
        for y in range(5):
            for x in range(5):
                if x > 0 and y > 0:
                    self.crops.append(Crop('watermelon', x, y))

    def gen_new(self):
        # Initialize a 2D array of Tiles with dimensions 16x20
        self.tiles = []
        for y in range(16):
            self.tiles.append([])
            for x in range(20):
                if (x > 0 and x < 5 and y > 0 and y < 5) or (x > 0 and x < 5 and y > 5 and y < 10):
                    self.tiles[y].append(Tile(1, x, y))
                else:
                    self.tiles[y].append(Tile(0, x, y))

    def get_tile_data(self):
        return bz2.compress(pickle.dumps(self.tiles))

    def set_tile_data(self, data):
        self.tiles = pickle.loads(bz2.decompress(data))

    def set_tile(self, coords, id):
        return 0

    def add_crop(self, crop):
        self.crops.append(crop)

    def render(self):
        img = Image.new('RGB', (340, 272), (255, 255, 255, 255))

        # Render tiles
        for y in range(16):
            for x in range(20):
                id = self.tiles[y][x].id
                tex = Textures.get_image(Tile.lookup_by_id[id])
                x1 = x * 17
                y1 = y * 17
                img.paste(tex, (x1, y1))

        # Render grid
        grid = Textures.get_image('grid')
        img.paste(grid, (0, 0), mask=grid)

        # Render crops
        for crop in self.crops:
            tex = Textures.get_image(Crop.lookup_by_id[crop.id])
            x = crop.x * 17
            y = crop.y * 17
            img.paste(tex, (x, y), tex)

        ret = io.BytesIO()
        img.save(ret, format='PNG')
        ret.seek(0)
        return ret
