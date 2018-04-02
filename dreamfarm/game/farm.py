from sqlalchemy import *
import numpy as np
from PIL import Image
import io
from sqlalchemy.orm import relationship
from dreamfarm.db import DB
from dreamfarm.game.obj import Obj
from dreamfarm.game.objinfo import ObjInfo
from dreamfarm.game.tile import Tile
from dreamfarm.game.tileinfo import TileInfo
from dreamfarm.game.textures import Textures

class Farm(DB.Base):
    __tablename__ = 'farms'

    id = Column(Integer, primary_key=True)
    duid = Column(BigInteger, ForeignKey('users.duid'))

    tiles = relationship('Tile')
    crops = relationship('Crop')
    objects = relationship('Obj')

    def __init__(self, tiles=None, crops=[], objects=[]):
        self.crops = crops
        self.objects = objects
        if tiles is None:
            untilled = TileInfo.get_by_name('untilled')
            self.tiles = []
            for y in range(16):
                for x in range(20):
                    self.tiles.append(Tile(x, y, untilled))

            # Generate some debris
            debris = [
                ObjInfo.get_by_name('tree'),
                ObjInfo.get_by_name('weeds'),
                ObjInfo.get_by_name('brown_leaves')
            ]

            self.objects = []
            obj_points = np.random.randint(0, 10, (20, 16))
            for (x, y), value in np.ndenumerate(obj_points):
                if value == 7:
                    self.objects.append(Obj(debris[0]))
                elif value == 6:
                    self.objects.append(Obj(debris[1]))
                elif value == 5:
                    self.objects.append(Obj(debris[2]))
        else:
            self.tiles = tiles

    def render(self):
        img = Image.new('RGB', (340, 272), (255, 255, 255, 255))

        # Render tiles
        for tile in self.tiles:
            tex = Textures.get(tile.tile_info.texture_x, tile.tile_info.texture_y).resize((17, 17))
            x1 = tile.x * 17
            y1 = tile.y * 17
            img.paste(tex, (x1, y1))

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
