import arcade

class Level:
    def __init__(self):
        spikes = ":resources:/images/tiles/spikes.png"

        self.platforms = arcade.SpriteList()
        self.window = arcade.get_window()

        self.scroll_speed = 0.0  # pixels per second

        platform = ":assets:piano-tile.png"
        platform_texture = arcade.load_texture(platform)
        count = (self.window.width // platform_texture.width) + 3
        for i in range(count):
            sprite = arcade.Sprite(platform_texture, 1.0, i * platform_texture.width, 180)
            self.platforms.append(sprite)

    def on_update(self, delta_time: float):
        for p in self.platforms:
            p.center_x -= self.scroll_speed * delta_time
            # wrap around
            if p.center_x < -p.width:
                rightmost = max(plat.center_x for plat in self.platforms)
                p.center_x = rightmost + p.width

    def draw(self):
        self.platforms.draw()