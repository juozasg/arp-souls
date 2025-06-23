import arcade

from constants import BLACK_KEYS


class RectPianoOctave:
    def __init__(self, rect_width: int = 80, x: int = 0, y: int = 0):
        self.rect_width = rect_width
        self.keys_on: list[int] = []
        self.x = x
        self.y = y

    def key_on(self, key: int):
        key = key % 12
        if key not in self.keys_on:
            self.keys_on.append(key)
            self.keys_on.sort()
            # print(f"Key {key} turned on.")

    def key_off(self, key: int):
        key = key % 12
        if key in self.keys_on:
            self.keys_on.remove(key)
            # print(f"Key {key} turned off.")

    def draw(self):
        for i in range(12):
            black = i in BLACK_KEYS
            color = arcade.color.BLACK if black else arcade.color.WHITE
            if i in self.keys_on:
                color = arcade.color.YELLOW

            x = i * (self.rect_width * 1.2) + self.x
            offset_y = (self.rect_width * 1.5)  if black else 0
            y = self.y + offset_y

            rect = arcade.rect.LBWH(x, y, self.rect_width, self.rect_width)
            arcade.draw_rect_filled(rect, color)
            # arcade.draw_text(str(i), x + self.rect_width / 2, 20, arcade.color.BLACK, font_size=16,
            #                  anchor_x="center", anchor_y="center")
