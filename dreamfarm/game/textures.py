import os
import redis
from PIL import Image

class Textures:
    atlas = Image.open(os.path.realpath('./dreamfarm/game/assets/atlas.png'))
    grid = Image.open(os.path.realpath('./dreamfarm/game/assets/grid.png'))
    images = []

    @staticmethod
    def initialize():
        for y in range(16):
            Textures.images.append([])
            for x in range(16):
                Textures.images[y].append(Textures.atlas.copy().crop((x, y, x + 16, y + 16)).convert('RGBA'))

    @staticmethod
    def get(texture_x, texture_y):
        return Textures.images[texture_y][texture_x]
