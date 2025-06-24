import arcade
from arcade import Texture

FRAME_WIDTH = 272
FRAME_HEIGHT = 192


class Knight(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # self.frame_count = 6  # Number of frames in the animation

        # Load the sprite sheet

        self.animations:dict[str, list[Texture]] = dict()

        self.animations['idle'] = arcade.load_spritesheet(':assets:knight/idle/spritesheet_idle_2x.png').get_texture_grid((FRAME_WIDTH, FRAME_HEIGHT), 6, 6)
        self.animations['run'] = arcade.load_spritesheet(':assets:knight/run/spritesheet_run_2x.png').get_texture_grid((FRAME_WIDTH, FRAME_HEIGHT), 1, 8)

        self.texture_list = self.animations['idle']
        self.current_frame = 0

        # Animation settings
        self.time_elapsed = 0
        self.frame_time = 1/15  # 10 frames per second

        # Set the initial texture
        self.texture = self.texture_list[0]
        
        # Set the scale if needed (adjust these values as needed)
        self.scale = 1.0

    def on_update(self, delta_time: float):
        # Update animation time
        self.time_elapsed += delta_time
        
        # Check if it's time to advance to the next frame
        if self.time_elapsed >= self.frame_time:
            self.time_elapsed = 0
            self.current_frame = (self.current_frame + 1) % len(self.texture_list)
            self.texture = self.texture_list[self.current_frame]

    def set_animation(self, animation_name: str):
        self.texture_list = self.animations[animation_name]
        self.current_frame = 0

    def draw(self):
        arcade.draw_sprite(self)
    #     super()