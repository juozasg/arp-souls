from typing import cast
import arcade
import mido

from constants import TILE_SCALING
from midi_message import MidiMessage
from ui.fps import draw_fps

class GameView(arcade.View):
    def __init__(self, midi_input_port: mido.ports.BaseInput):
        super().__init__()
        self.midi_in = midi_input_port

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # self.background_color = arcade.color.WHITE


    def on_update(self, delta_time):
        # return super().on_update(delta_time)
        self.dt = delta_time
        self.logic_fps = 1 / delta_time if delta_time > 0 else 99999

        # Process MIDI messages
        for msg in self.midi_in.iter_pending():
            msg = cast(MidiMessage, msg)
            print(f"MIDI: {msg.type} Note: {msg.note}")

    def on_draw(self):
        self.clear()

        arcade.draw_text("Hello Arp Souls Default", 500, 800, arcade.color.BLACK, font_size=50)

        # draw_text = f"FPS: {self.fps:.2f} | Delta Time: {self.dt:.4f}"
        draw_fps(self.logic_fps, self.dt)

        # arcade.start_render()
        # arcade.draw_text("Hello Arp Souls", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  arcade.color.BLACK, font_size=24, anchor_x="center")