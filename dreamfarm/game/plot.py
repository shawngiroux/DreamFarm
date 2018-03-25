from dreamfarm.game.tile import Tile

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
                self.tiles[y].append([Tile(0, x, y)])

    def set_tile(self, coords, id):
        return 0

    # def render(self):
