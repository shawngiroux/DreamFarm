import io
import math
from PIL import Image
from dreamfarm.game.plot import Plot

class Farm:
    def __init__(self):
        self.plots = []

    def generate(self):
        self.plots = []
        for i in range(12):
            self.plots.append(Plot())
            self.plots[i].gen_new()
            yield ((self.plots[i].get_tile_data(), self.plots[i].get_object_data()), i)

    def add_plot(self, plot):
        self.plots.append(plot)

    def render(self):
        # Arrange the plots into the closest thing to a square
        count = len(self.plots)
        height = math.floor(math.sqrt(count))
        while count % height != 0:
            height -= 1
        width = count // height

        img = Image.new('RGB', (340 * width, 272 * height), (255, 255, 255, 255))

        for y in range(height):
            for x in range(width):
                plot_img = self.plots[y * width + x].render()
                img.paste(plot_img, (x * 340, y * 272))

        return img

    def render_file(self):
        img = self.render()
        ret = io.BytesIO()
        img.save(ret, format='PNG')
        ret.seek(0)
        return ret
