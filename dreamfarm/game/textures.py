import os

from PIL import Image

import redis


class Textures:
    atlas = Image.open(os.path.realpath('./dreamfarm/game/assets/atlas.png'))
    grid = Image.open(os.path.realpath('./dreamfarm/game/assets/grid.png'))
    images = []

    @staticmethod
    def initialize():
        for y in range(16):
            Textures.images.append([])
            for x in range(16):
                x1 = x * 16
                y1 = y * 16
                Textures.images[y].append(Textures.atlas.copy().crop((x1, y1, x1 + 16, y1 + 16)).convert('RGBA'))

    @staticmethod
    def get(texture_x, texture_y):
        return Textures.images[texture_y][texture_x]
