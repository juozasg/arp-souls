import arcade

from game.note import Note


class Level:
    def __init__(self):
        # spikes = ":resources:/images/tiles/spikes.png"
        window = arcade.get_window()

        self.platforms = arcade.SpriteList()
        self.notes = []

        self.scroll_speed = 0.0  # pixels per second

        platform = ":assets:piano-tile.png"
        platform_texture = arcade.load_texture(platform)
        count = (window.width // platform_texture.width) + 3
        for i in range(count):
            sprite = arcade.Sprite(platform_texture, 1.0, i * platform_texture.width, 180)
            self.platforms.append(sprite)

        note1 = Note('C')
        note1.center_x = 300
        note1.center_y = 320
        self.notes.append(note1)

        note2 = Note('G')
        note2.center_x = 500
        note2.center_y = 320
        self.notes.append(note2)

    def on_update(self, delta_time: float):
        self.move_platforms(delta_time)
        self.move_notes(delta_time)

    def move_notes(self, delta_time):
        for note in self.notes:
            note.center_x -= self.scroll_speed * delta_time
            if note.center_x < -50:
                self.notes.remove(note)
                # note.center_x = note.width
                # note.was_hit()

    def move_platforms(self, delta_time):
        for p in self.platforms:
            p.center_x -= self.scroll_speed * delta_time
        self.platforms.sort(key=lambda x: x.center_x)
        leftmost = self.platforms[0]
        # wrap around
        if leftmost.center_x < -leftmost.width:
            rightmost = max(plat.center_x for plat in self.platforms)
            leftmost.center_x = rightmost + leftmost.width

    def draw(self):
        self.platforms.draw()
        for note in self.notes:
            note.draw()