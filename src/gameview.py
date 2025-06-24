from typing import cast

import arcade
import mido

from game.bpm import BPM
from game.knight import Knight
from game.level import Level
from midi_message import MidiMessage
from ui.fps import draw_fps
from ui.rect_piano_octave import RectPianoOctave


class GameView(arcade.View):
    def __init__(self, midi_input_port: mido.ports.BaseInput):
        super().__init__()
        self.bpm = BPM()
        self.midi_in = midi_input_port

        self.level = Level()

        # Create and position the knight
        self.knight = Knight()
        self.knight.center_x = 200  # Set x position
        self.knight.center_y = 300  # Set y position
        self.knight.start_animation("idle")


        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.piano_octave = RectPianoOctave(rect_width=80, x=380, y=500)

        self.dt = 0.0
        self.logic_fps = 0.0
        # self.background_color = arcade.color.WHITE

        self.text_hello = arcade.Text("Arp Knight", self.window.center_x, 1000, arcade.color.BLACK, font_size=50,
                                      anchor_x="center")
        self.text_bpm = arcade.Text(f"", 5, 70, arcade.color.BLACK, font_size=20, anchor_x="left")
        self.text_err = arcade.Text(f"", 5, 40, arcade.color.BLACK, font_size=20, anchor_x="left")

    def on_update(self, delta_time):
        # return super().on_update(delta_time)
        self.dt = delta_time
        self.logic_fps = 1 / delta_time if delta_time > 0 else 99999

        current_bpm = self.bpm.bpm
        self.bpm.tick(delta_time)
        self.knight.on_update(delta_time)
        self.level.on_update(delta_time)

        # Process MIDI messages
        for msg in self.midi_in.iter_pending():
            msg = cast(MidiMessage, msg)
            # print(f"MIDI: {msg.type} Note: {msg.note}")
            if msg.type == "note_on":
                self.piano_octave.key_on(msg.note)
                new_beat = self.bpm.key_on(msg.note)
                if new_beat and self.knight.current_animation != 'attack':
                    self.knight.oneshot_animation('attack')

            elif msg.type == "note_off":
                self.piano_octave.key_off(msg.note)

        new_bpm = self.bpm.bpm

        if current_bpm is None and new_bpm is not None:
            self.knight.start_animation("run")
        elif current_bpm is not None and new_bpm is None:
            self.knight.start_animation("idle")

        # keep running if it gets out of sync
        if new_bpm is not None and (self.knight.current_animation != "attack" and self.knight.current_animation != "jump"):
            self.knight.current_animation = "run"

        if new_bpm is not None:
            self.level.scroll_speed = new_bpm * 2
        else:
            self.level.scroll_speed = 0

    def on_draw(self):
        self.clear()

        self.level.draw()
        self.knight.draw()
        self.piano_octave.draw()

        self.text_hello.draw()

        self.bpm.draw_debug()

        if self.bpm.bpm is not None:
            # arcade.draw_text(f"BPM: {self.bpm.bpm: .1f}", 50, 200, arcade.color.BLACK, font_size=20, anchor_x="left")
            self.text_bpm.text = f"Tempo: {self.bpm.bpm: .1f}"
        if self.bpm.error is not None:
            error = self.bpm.error * 100
            self.text_err.text = f"Err: {error: .1f}"

        if self.bpm.bpm is None:
            self.text_bpm.text = "Tempo: ???"

        # arcade.
        # self.bpm.

        # arcade.
        # arcade.
        self.text_bpm.draw()
        self.text_err.draw()
        # draw_text = f"FPS: {self.fps:.2f} | Delta Time: {self.dt:.4f}"
        draw_fps(self.logic_fps, self.dt)

        # arcade.start_render()
        # arcade.draw_text("Hello Arp Souls", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  arcade.color.BLACK, font_size=24, anchor_x="center")
