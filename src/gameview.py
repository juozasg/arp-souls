import arcade

from constants import TILE_SCALING
from ui.fps import draw_fps

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_texture = arcade.load_texture(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # self.background_color = arcade.color.WHITE


    def on_update(self, delta_time):
        # return super().on_update(delta_time)
        self.dt = delta_time
        self.logic_fps = 1 / delta_time if delta_time > 0 else 99999

    def on_draw(self):
        self.clear()
        # Code to draw other things will go here
        arcade.draw_sprite(self.player_sprite)
        self.wall_list.draw()

        arcade.draw_text("Hello Arp Souls Default", 500, 800, arcade.color.BLACK, font_size=50)


        # draw_text = f"FPS: {self.fps:.2f} | Delta Time: {self.dt:.4f}"
        # draw_fps(self.logic_fps, self.dt)

        # arcade.start_render()
        # arcade.draw_text("Hello Arp Souls", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  arcade.color.BLACK, font_size=24, anchor_x="center")