from sqlalchemy import *
import numpy as np
from PIL import Image
import io
from sqlalchemy.orm import relationship
from dreamfarm.db import DB
from dreamfarm.game.obj import Obj
from dreamfarm.game.tile import Tile
from dreamfarm.game.textures import Textures

# A farm belonging to a player, containing many tiles
class Farm(DB.Base):
    __tablename__ = 'farms'

    id = Column(Integer, primary_key=True)
    duid = Column(BigInteger, ForeignKey('users.duid'), index=True)

    tiles = relationship('Tile', backref='farms')

    def __init__(self, tiles=None):
        if tiles is None:
            # Generate a new farm with some debris
            obj_points = np.random.randint(0, 10, (20, 16))
            for (x, y), value in np.ndenumerate(obj_points):
                tile = Tile(x, y, 'untilled')
                if value == 7:
                    tile.obj = Obj('tree')
                elif value == 6:
                    tile.obj = Obj('weeds')
                elif value == 5:
                    tile.obj = Obj('brown_leaves')
                self.tiles.append(tile)
        else:
            self.tiles = tiles

    def render(self):
        img = Image.new('RGB', (340, 272), (255, 255, 255, 255))

        # Render tiles
        for tile in self.tiles:
            tile_img = tile.render()
            img.paste(tile_img, (tile.x * 17, tile.y * 17))

        # Render grid
        grid = Textures.grid
        img.paste(grid, (0, 0), mask=grid)

        return img

    def render_file(self):
        img = self.render()
        ret = io.BytesIO()
        img.save(ret, format='PNG')
        ret.seek(0)
        return ret
