import os
from PIL import Image

class Textures:
    atlas = Image.open(os.path.realpath('./dreamfarm/game/textures/atlas.png'))

    @staticmethod
    def get_image(id):
        tx, ty = Textures.by_id[id]['tex'];
        x1 = 16 * tx
        x2 = x1 + 16
        y1 = 16 * ty
        y2 = y1 + 16
        return Textures.atlas.copy().crop((x1, y1, x2, y2))

    by_id = [
        {
            'tex': (14, 15)
        },
        {
            'tex': (14, 15)
        }
    ]

    by_name = {
        'grass': by_id[0],
        'corn': by_id[1]
    }
