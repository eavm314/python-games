import pygame
from config import HEIGHT, WIDTH
from scenes.base import COLOR_BLUE, COLOR_WHITE, COLOR_YELLOW, Scene


class SceneLevelsMenu(Scene):
    def __init__(self, context):
        Scene.__init__(self)
        self.context = context
        self.selected_level = min(context['unlocked_level'], 10)

    def read_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_UP:
                self.selected_level = max(1, self.selected_level - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_level = min(self.context['unlocked_level'], self.selected_level + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.change_scene(('Level', self.selected_level))

    def draw(self, screen):
        screen.fill(COLOR_BLUE)
        title_font = pygame.font.SysFont('Arial', 36)
        level_font = pygame.font.SysFont('Consolas', 24)
        title = title_font.render('Select a level', True, COLOR_WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH / 2, 60)))

        for level in range(1, 11):
            unlocked = level <= self.context['unlocked_level']
            completed = level in self.context['completed_levels']
            color = COLOR_YELLOW if level == self.selected_level and unlocked else COLOR_WHITE
            label = f'{level:02d}  '
            if not unlocked:
                label += 'Locked'
            elif completed:
                label += 'Complete'
            else:
                label += 'Ready'
            text = level_font.render(label, True, color)
            text_rect = text.get_rect(center=(WIDTH / 2, 80 + level * 30))
            screen.blit(text, text_rect)

        score = level_font.render(f"Score: {self.context['score']}", True, COLOR_WHITE)
        screen.blit(score, score.get_rect(center=(WIDTH / 2, HEIGHT - 35)))
