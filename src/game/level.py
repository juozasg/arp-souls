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
        note2.center_x = 300
        note2.center_y = 380
        self.notes.append(note2)

    def notes_in_hit_zone(self):
        # find all the notes around x = 300
        notes_in_hit_zone = []
        for note in self.notes:
            if 290 < note.center_x < 310:
                notes_in_hit_zone.append(note)
        return notes_in_hit_zone


    def note_hit(self, note_name: str):
        hit_notes = self.notes_in_hit_zone()
        for note in hit_notes:
            if note.letter == note_name:
                note.was_hit()
                return True
        return False

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