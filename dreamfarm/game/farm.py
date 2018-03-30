import pickle
import bz2
import io
import os
import numpy as np
from PIL import Image
from dreamfarm.game.tile import Tile
from dreamfarm.game.crop import Crop
from dreamfarm.game.obj import Obj
from dreamfarm.game.textures import Textures

# Convert grid notation (A1, D12, etc.) to tile indices
def coords_to_indices(coords):
    return (0, 0)

class Farm:
    def __init__(self):
        self.tiles = []
        self.crops = []
        self.objects = []

    def gen_new(self):
        # Initialize a 2D array of Tiles with dimensions 16x20
        self.tiles = []
        for y in range(16):
            self.tiles.append([])
            for x in range(20):
                self.tiles[y].append(Tile(2, x, y))

        # Generate some debris
        self.objects = []
        obj_points = np.random.randint(0, 10, (20, 16))
        for (x, y), value in np.ndenumerate(obj_points):
            if value == 7:
                self.objects.append(Obj('tree', x, y))
            elif value == 6:
                self.objects.append(Obj('brown_leaves', x, y))
            elif value == 5:
                self.objects.append(Obj('weeds', x, y))

        return (self.get_tile_data(), self.get_object_data())

    def get_tile_data(self):
        return bz2.compress(pickle.dumps(self.tiles))

    def set_tile_data(self, data):
        self.tiles = pickle.loads(bz2.decompress(data))

    def get_object_data(self):
        return bz2.compress(pickle.dumps(self.objects))

    def set_object_data(self, data):
        self.objects = pickle.loads(bz2.decompress(data))

    def set_tile(self, coords, id):
        return 0

    def add_crop(self, crop):
        self.crops.append(crop)

    def render_file(self):
        img = self.render()
        ret = io.BytesIO()
        img.save(ret, format='PNG')
        ret.seek(0)
        return ret

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

        # Render objects
        for obj in self.objects:
            tex = Textures.get_image(Obj.lookup_by_id[obj.id])
            x = obj.x * 17
            y = obj.y * 17
            img.paste(tex, (x, y), tex)

        return img
