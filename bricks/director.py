import time
import pygame
from config import HEIGHT, TITLE, WIDTH
from scenes import SceneLevel, SceneGameOver

class Director:
    def __init__(self):
        pygame.init()
        self.current_scene = None
        # Initialize the screen.
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # Set the window title.
        pygame.display.set_caption(TITLE)
        # Create the clock.
        self.clock = pygame.time.Clock()
        self.scenes = {
            'Level1': SceneLevel,
            'GameOver': SceneGameOver,
        }

    def run(self, initial_scene, fps=60):
        self.choose_scene(initial_scene)
        playing = True
        while playing:
            self.clock.tick(fps)
            events = pygame.event.get()
            # Check all events.
            for event in events:
                # If the close button on the title bar is pressed,
                if event.type == pygame.QUIT:
                    # close the game.
                    playing = False

            scene = self.current_scene
            scene.read_events(events)
            scene.update()
            scene.draw(self.screen)

            self.choose_scene(scene.next_scene)

            if playing:
                playing = scene.playing

            pygame.display.flip()

        time.sleep(3)

    def choose_scene(self, next_scene):
        if next_scene:
            if next_scene not in self.scenes:
                raise ValueError(f"Scene '{next_scene}' not found.")
            self.current_scene = self.scenes[next_scene]()
