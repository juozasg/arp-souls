import arcade

from gameview import GameView

class IntroView(arcade.View):
    # super().__init__()

    def on_draw(self):
        self.clear()
        arcade.draw_text("Select MIDI Input", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("(Click to DEBUG)", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # DEBUG: Simulate MIDI ready
        self.on_midi_ready()

    def on_midi_ready(self):
        print("MIDI is ready!")
        game = GameView()
        self.window.show_view(game)