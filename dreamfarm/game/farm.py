import io
from PIL import Image
from dreamfarm.game.plot import Plot

class Farm:
    def __init__(self):
        self.plots = []

    def generate(self):
        self.plots = []
        for i in range(4):
            self.plots.append(Plot())
            self.plots[i].gen_new()
            yield ((self.plots[i].get_tile_data(), self.plots[i].get_object_data()), i)

    def add_plot(self, plot):
        self.plots.append(plot)

    def render(self):
        img = Image.new('RGB', (680, 544), (255, 255, 255, 255))

        for i, plot in enumerate(self.plots):
            plot_img = plot.render()
            x = i % 2
            y = i // 2
            img.paste(plot_img, (x * 340, y * 272))

        return img

    def render_file(self):
        img = self.render()
        ret = io.BytesIO()
        img.save(ret, format='PNG')
        ret.seek(0)
        return ret
