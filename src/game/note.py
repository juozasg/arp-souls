import arcade
from arcade.gl.types import PyGLenum, OpenGlFilter, BlendFunction


class Note:
    def __init__(self, letter='C'):
        super().__init__()

        self.letter = letter

        self.center_x = 0
        self.center_y = 0

        self.circle = arcade.SpriteCircle(30, arcade.color.BLUE_GREEN, True)
        self.letter_text = arcade.Text(letter, 0, 0, arcade.color.WHITE, 24, anchor_x="center", anchor_y="center", bold=True, font_name="Kenney Future")

    def was_hit(self):
        self.circle.color = arcade.color.YELLOW_GREEN

    def draw(self):
        self.circle.position = self.center_x, self.center_y
        self.letter_text.position = self.center_x + 2, self.center_y

        arcade.draw_sprite(self.circle)
        self.letter_text.draw()