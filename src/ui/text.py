import pygame


text_font = None


def init_text():
    global text_font
    text_font = pygame.font.SysFont('Arial', 37)

def draw_text(surface, text, color, x, y):
    text_surface = text_font.render(text, True, color)
    surface.blit(text_surface, (x, y))