import pygame
from config import HEIGHT, TITLE, WIDTH, UNLOCKED_LEVELS
from scenes import SceneGameOver, SceneLevel, SceneLevelsMenu

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
        self.context = {
            'unlocked_level': 10 if UNLOCKED_LEVELS else 1,
            'completed_levels': set(),
            'score': 0,
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

        pygame.quit()

    def choose_scene(self, next_scene):
        if next_scene:
            scene_name = next_scene[0] if isinstance(next_scene, tuple) else next_scene
            level = next_scene[1] if isinstance(next_scene, tuple) else None
            if scene_name == 'LevelsMenu':
                self.current_scene = SceneLevelsMenu(self.context)
            elif scene_name == 'Level':
                self.current_scene = SceneLevel(self.context, level)
            elif scene_name == 'GameOver':
                self.current_scene = SceneGameOver(self.context)
            else:
                raise ValueError(f"Scene '{scene_name}' not found.")
