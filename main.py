import os, tempfile
from pathlib import Path
import pyglet
import arcade

from constants import WINDOW_HEIGHT, WINDOW_WIDTH

from views.intro import IntroView
from piano_sampler import load_soundfound

asset_dir = os.path.join(Path(__file__).parent.resolve(), "assets")
arcade.resources.add_resource_handle("assets", asset_dir)

arcade.resources.load_liberation_fonts()

load_soundfound()

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Arp Knight", update_rate=1.0/1000)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()

    def center_on_screen(self):
        viewport = pyglet.display.get_display().get_default_screen()
        left = (viewport.width - WINDOW_WIDTH) // 4
        top = (viewport.height - WINDOW_HEIGHT) // 4
        self.set_location(left, top)


def remove_splash_screen():
    if "NUITKA_ONEFILE_PARENT" in os.environ:
        splash_filename = os.path.join(
            tempfile.gettempdir(),
            "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
        )

        if os.path.exists(splash_filename):
            os.unlink(splash_filename)


def main():
    window = GameWindow()
    # window.set_vsync(True)
    game = IntroView()
    window.show_view(game)
    window.center_on_screen()

    arcade.enable_timings()
    arcade.run()

    remove_splash_screen()

if __name__ == '__main__':
    main()