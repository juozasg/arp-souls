import arcade
from arcade import Texture

FRAME_WIDTH = 272
FRAME_HEIGHT = 192


class Knight(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.is_running = False

        self.animations: dict[str, list[Texture]] = dict()

        self.animations['idle'] = arcade.load_spritesheet(
            ':assets:knight/idle/spritesheet_idle_2x.png').get_texture_grid((FRAME_WIDTH, FRAME_HEIGHT), 6, 6)
        self.animations['run'] = arcade.load_spritesheet(':assets:knight/run/spritesheet_run_2x.png').get_texture_grid(
            (FRAME_WIDTH, FRAME_HEIGHT), 1, 8)
        # part of the attack combo
        attack_sheet = arcade.load_spritesheet(':assets:knight/attack/spritesheet_attack_2x.png').get_texture_grid(
            (FRAME_WIDTH, FRAME_HEIGHT), 7, 14)
        self.animations['attack'] = attack_sheet[1:4]
        # attack_sheet = arcade.load_spritesheet(':assets:knight/attack/spritesheet_attack_2x.png').get_texture_grid((FRAME_WIDTH, FRAME_HEIGHT), 7, 14)
        self.animations['attack2'] = attack_sheet[9:14]

        self.current_animation = 'idle'
        self.current_frame = 0

        # Animation settings
        self.time_elapsed = 0
        self.frame_time = 1 / 15  # 10 frames per second

        self.speed_multiplier = 1.0
        # self.frame_time = 0.5  # 1 frames per second

        # Set the initial texture
        self.texture = self.animations['idle'][0]

    def on_update(self, delta_time: float):
        # Update animation time
        self.time_elapsed += delta_time

        # Check if it's time to advance to the next frame
        speed_mult = 1.0
        if self.current_animation == 'run':
            speed_mult = self.speed_multiplier
        if self.time_elapsed >= self.frame_time * speed_mult:
            self.time_elapsed = 0
            self.current_frame = (self.current_frame + 1)
            if self.current_frame >= len(self.animations[self.current_animation]):
                self.current_frame = 0
                if self.is_running:
                    self.current_animation = 'run'
                else:
                    self.current_animation = 'idle'

            texture_list = self.animations[self.current_animation]
            self.texture = texture_list[self.current_frame]

    # def start_animation(self, animation_name: str):
    #     print(f"Start animation: {animation_name}")
    #     self.current_animation = animation_name
    #     self.current_frame = 0
    #     # self.time_elapsed = 0

    def oneshot_animation(self, animation_name: str):
        if self.current_animation != animation_name:
            self.current_frame = 0
        self.current_animation = animation_name

        # self.time_elapsed = 0

    def draw(self):
        arcade.draw_sprite(self)
    #     super()
