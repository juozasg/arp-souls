from random import randint
from typing import Any, cast
import mido
import arcade
import arcade.gui

from gameview import GameView

class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()

        self.nomidi = False  # Flag to indicate if no MIDI inputs are found

        self.input_ports: Any = mido.get_input_names()  # type: ignore
        if not self.input_ports or len(self.input_ports) == 0:
            self.nomidi = True
            return



        # Prepend index to each item in the input_ports list
        portnames = [f"{i+1}: {port}" for i, port in enumerate(self.input_ports)]
        dd = arcade.gui.UIDropdown(height=80, width=400, default=portnames[0] if portnames[0] else "No MIDI Inputs",
                                   options=cast(Any, portnames))

        @dd.event()
        def on_change(event: arcade.gui.UIOnChangeEvent):
            print("CHANGE", event.old_value, event.new_value)
            index = int(event.new_value.split(":")[0]) - 1
            if 0 <= index < len(self.input_ports):
                self.open_midi_input(index)

        self.anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="top",
            align_y=-200,
            child=dd,
        )

        # button = arcade.gui.UIFlatButton(text="Skip", width=250)
        # @button.event("on_click")
        # def on_button_click(event):
            # self.on_midi_ready()

    def on_update(self, delta_time: float) -> bool | None:
        default_port_name = 'KeyLab mkII 61'
        # find the default port index by substring match
        default_port_index = next((i for i, port in enumerate(self.input_ports) if default_port_name in port), -1)

        if default_port_index != -1:
            # If the default port is found, open it immediately
            print(f"Default MIDI Input found: {self.input_ports[default_port_index]}")
            self.open_midi_input(default_port_index)
            return

    def on_draw(self):
        self.clear()
        if self.nomidi:
            arcade.draw_text("No MIDI Inputs Found", self.window.width / 2, self.window.height / 2,
                             arcade.color.WHITE, font_size=50, anchor_x="center")
            return
        arcade.draw_text("Select MIDI Input", self.window.width / 2, self.window.height  - 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press 1 for default", self.window.width / 2, self.window.height  - 150,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        # arcade.draw_text("(Click to DEBUG)", self.window.width / 2, self.window.height / 2-75,
        #                  arcade.color.WHITE, font_size=20, anchor_x="center")

        self.ui.draw()

    def on_show_view(self):
        """This is run once when we switch to this view"""
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.ui.enable()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.ui.disable()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol >= arcade.key.KEY_1 and symbol <= arcade.key.KEY_9:
            # If a number key is pressed, use it to select the MIDI input
            index = symbol - arcade.key.KEY_1
            if 0 <= index < len(self.input_ports):
                self.open_midi_input(index)
            else:
                print("Invalid MIDI Input selection")

    def open_midi_input(self, index: int):
        selected_port = self.input_ports[index]
        print(f"Selected MIDI Input: {selected_port}")
                # Here you would typically open the MIDI port and set up the game
        midi_in = mido.open_input(selected_port) # type: ignore
        if(midi_in):
            print(f"Opened MIDI Input: {selected_port}")
            self.on_midi_ready(midi_in)
        else:
            self.nomidi = True


    def on_midi_ready(self, midi_in: mido.ports.BaseInput):
        print("MIDI is ready!")
        # midi_in = mido.open_input
        game = GameView(midi_in)
        self.window.show_view(game)