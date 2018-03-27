from dreamfarm.game.plot import Plot

class Farm:
    def generate(self):
        self.plots = []
        for i in range(4):
            self.plots.append(Plot())
            yield (self.plots[i].get_tile_data(), i)
