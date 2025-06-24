import arcade

def draw_fps(logic_fps, dt):
    arcade.draw_text(
        f"Logic FPS: {logic_fps:.2f} | Delta Time: {dt:.4f} | Render FPS: {arcade.get_fps():.2f}",
        arcade.get_window().width - 10, 10, arcade.color.BLACK, font_size=12, anchor_x='right')
