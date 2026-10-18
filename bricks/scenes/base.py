import pygame

COLOR_BLUE = (0, 0, 64)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 220, 80)
COLOR_OVERLAY = (0, 0, 0, 190)


class Scene:
    """Skeleton for each of the game's scenes."""

    def __init__(self):
        self.next_scene = False
        self.playing = True

    def read_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def change_scene(self, scene):
        self.next_scene = scene
