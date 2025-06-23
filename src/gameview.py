from typing import cast
import arcade
import mido

from constants import TILE_SCALING
from game.bpm import BPM
from midi_message import MidiMessage
from ui.fps import draw_fps
from ui.rect_piano_octave import RectPianoOctave

class GameView(arcade.View):
    def __init__(self, midi_input_port: mido.ports.BaseInput):
        super().__init__()
        self.midi_in = midi_input_port

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.piano_octave = RectPianoOctave(rect_width=80, x=380, y=500)

        self.dt = 0.0
        self.logic_fps = 0.0
        self.bpm = BPM()
        self.beattime: float | None = None
        # self.background_color = arcade.color.WHITE


    def on_update(self, delta_time):
        # return super().on_update(delta_time)
        self.dt = delta_time
        self.logic_fps = 1 / delta_time if delta_time > 0 else 99999

        if self.beattime is not None:
            self.beattime += delta_time
        # Process MIDI messages
        for msg in self.midi_in.iter_pending():
            msg = cast(MidiMessage, msg)
            # print(f"MIDI: {msg.type} Note: {msg.note}")
            if msg.type == "note_on":
                self.piano_octave.key_on(msg.note)
                if self.beattime is None:
                    self.beattime = 0.0
                else:
                    self.bpm.update_beat(self.beattime)
                    self.beattime = 0.0  # Reset for next beat
            elif msg.type == "note_off":
                self.piano_octave.key_off(msg.note)

    def on_draw(self):
        self.clear()

        self.piano_octave.draw()

        arcade.draw_text("Hello Arp Souls", self.window.center_x, 1000, arcade.color.BLACK, font_size=50, anchor_x="center")


        if self.bpm.bpm is not None:
            arcade.draw_text(f"BPM: {self.bpm.bpm: .1f}", 50, 200, arcade.color.BLACK, font_size=20, anchor_x="left")
        if self.bpm.error is not None:
            error = self.bpm.error * 100
            arcade.draw_text(f"Err: {error: .1f}", 50, 150, arcade.color.BLACK, font_size=20, anchor_x="left")

        if self.bpm.bpm is None:
            arcade.draw_text("BPM: ???", 50, 200, arcade.color.BLACK, font_size=20, anchor_x="left")
            # arcade.draw_text("Err: N/A", 50, 150, arcade.color.BLACK, font_size=20, anchor_x="left")

        # draw_text = f"FPS: {self.fps:.2f} | Delta Time: {self.dt:.4f}"
        draw_fps(self.logic_fps, self.dt)

        # arcade.start_render()
        # arcade.draw_text("Hello Arp Souls", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  arcade.color.BLACK, font_size=24, anchor_x="center")