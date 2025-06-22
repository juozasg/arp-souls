import os
from pathlib import Path
import pyglet
import arcade

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
# from gameview import GameView
from introview import IntroView

asset_dir = os.path.join(Path(__file__).parent.resolve(), "assets")
arcade.resources.add_resource_handle("assets", asset_dir)

arcade.resources.load_liberation_fonts()
arcade.resources.load_kenney_fonts()



def center_window(window):
    viewport = pyglet.display.get_display().get_default_screen()
    left = (viewport.width - WINDOW_WIDTH) // 4
    top = (viewport.height - WINDOW_HEIGHT) // 4
    window.set_location(left, top)

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Hello Arp Souls", update_rate=1.0/200)
    # window.set_vsync(True)
    game = IntroView()
    window.show_view(game)
    center_window(window)

    arcade.enable_timings()
    arcade.run()


if __name__ == '__main__':
    main()