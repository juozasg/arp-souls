import pyglet
import arcade

from constants import WINDOW_HEIGHT, WINDOW_WIDTH


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Hello Arp Souls")
        self.background_color = arcade.color.WHITE

    def setup(self):
        pass

    def center_on_screen(self):
        viewport = pyglet.display.get_display().get_default_screen()
        left = (viewport.width - WINDOW_WIDTH) // 4
        top = (viewport.height - WINDOW_HEIGHT) // 4
        self.set_location(left, top)

    def on_draw(self):
        self.clear()
        # arcade.start_render()
        # arcade.draw_text("Hello Arp Souls", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  arcade.color.BLACK, font_size=24, anchor_x="center")

def main():
    window = GameView()
    window.setup()
    window.center_on_screen()
    arcade.run()


if __name__ == '__main__':
    main()