import arcade
from arcade import Texture

FRAME_WIDTH = 272
FRAME_HEIGHT = 192


class Knight(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.animations:dict[str, list[Texture]] = dict()

        self.animations['idle'] = arcade.load_spritesheet(':assets:knight/idle/spritesheet_idle_2x.png').get_texture_grid((FRAME_WIDTH, FRAME_HEIGHT), 6, 6)
        self.animations['run'] = arcade.load_spritesheet(':assets:knight/run/spritesheet_run_2x.png').get_texture_grid((FRAME_WIDTH, FRAME_HEIGHT), 1, 8)
        # part of the attack combo
        self.animations['attack'] = arcade.load_spritesheet(':assets:knight/attack/spritesheet_attack_2x.png').get_texture_grid((FRAME_WIDTH, FRAME_HEIGHT), 7, 14)
        self.animations['attack'] = self.animations['attack'][1:4]

        self.current_animation = 'idle'
        self.previous_animation = None
        self.current_frame = 0

        # Animation settings
        self.time_elapsed = 0
        self.frame_time = 1/15  # 10 frames per second

        # Set the initial texture
        self.texture = self.animations['idle'][0]


    def on_update(self, delta_time: float):
        # Update animation time
        self.time_elapsed += delta_time

        # Check if it's time to advance to the next frame
        if self.time_elapsed >= self.frame_time:
            self.time_elapsed = 0
            self.current_frame = (self.current_frame + 1)
            if self.current_frame >= len(self.animations[self.current_animation]):
                self.current_frame = 0
                if self.previous_animation:
                    self.start_animation(self.previous_animation)
                    self.previous_animation = None

            texture_list = self.animations[self.current_animation]
            self.texture = texture_list[self.current_frame]

    def start_animation(self, animation_name: str):
        self.current_animation = animation_name
        self.current_frame = 0
        # self.time_elapsed = 0

    def oneshot_animation(self, animation_name: str):
        self.previous_animation = self.current_animation
        self.start_animation(animation_name)
        # self.time_elapsed = 0

    def draw(self):
        arcade.draw_sprite(self)
    #     super()