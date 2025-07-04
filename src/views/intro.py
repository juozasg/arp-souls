from random import randint
from typing import Any, cast
import mido
import arcade
import arcade.gui
from views.game_main import GameMain


class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()

        self.no_midi = False  # Flag to indicate if no MIDI inputs are found

        self.input_ports: Any = mido.get_input_names()  # type: ignore
        if not self.input_ports or len(self.input_ports) == 0:
            self.no_midi = True
            return



        # Prepend index to each item in the input_ports list
        port_names = [f"{i + 1}: {port}" for i, port in enumerate(self.input_ports)]
        dd = arcade.gui.UIDropdown(height=80, width=400, default=port_names[0] if port_names[0] else "No MIDI Inputs",
                                   options=cast(Any, port_names))

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



        self.instructions_text = arcade.gui.UITextArea(
            text="""HOW TO PLAY:
            
Play green arpeggio notes to turn them yellow
Play yellow notes together as a chord to make them red and temporarily unlock the next chord
Start playing the next chord arpeggio to jump to the higher level
Steady rhythm restores HP. Faster tempo scores more points.
Game ends when you run out of HP.""",
            width=900,
            height=300,
            font_size=16,
            # font_name="Arial",
            text_color=arcade.color.WHITE,
            background_color=arcade.color.BLACK,
        )
        self.anchor.add(self.instructions_text)

    def on_update(self, delta_time: float) -> bool | None:
        self.select_default_midi()
        # pass

    def select_default_midi(self):
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
        if self.no_midi:
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
        if arcade.key.KEY_1 <= symbol <= arcade.key.KEY_9:
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
        if midi_in:
            print(f"Opened MIDI Input: {selected_port}")
            self.on_midi_ready(midi_in)
        else:
            self.no_midi = True


    def on_midi_ready(self, midi_in: mido.ports.BaseInput):
        print("MIDI is ready!")
        # midi_in = mido.open_input
        game = GameMain(midi_in)
        self.window.show_view(game)