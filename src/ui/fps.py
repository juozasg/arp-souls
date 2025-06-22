import arcade

def draw_fps(logicfps, dt):
    arcade.draw_text(
        f"Logic FPS: {logicfps:.2f} | Delta Time: {dt:.4f} | Render FPS: {arcade.get_fps():.2f}",
        10, 10, arcade.color.BLACK, font_size=20)
