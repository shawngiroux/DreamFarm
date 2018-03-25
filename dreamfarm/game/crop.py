from dreamfarm.game.textures import Textures

class Crop:
    by_name = {
        'corn': 0
    }

    def __init__(self, name, x, y):
        self.id = Crop.by_name[name]
        self.x = x
        self.y = y
        self.tex = Textures.by_name[name]

    def draw(self):
        return 0
