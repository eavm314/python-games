import time
import pygame

from config import HEIGHT, WIDTH
from scenes.base import COLOR_WHITE, Scene


class SceneGameOver(Scene):
    def __init__(self, context):
        Scene.__init__(self)
        self.context = context

    def update(self):
        self.playing = False

    def draw(self, screen):
        font = pygame.font.SysFont('Arial', 72)
        message = 'You cleared every level!' if len(self.context['completed_levels']) == 10 else 'Game over :('
        text = font.render(message, True, COLOR_WHITE)
        text_rect = text.get_rect()
        text_rect.center = [WIDTH / 2, HEIGHT / 2]
        screen.blit(text, text_rect)
        time.sleep(3)
