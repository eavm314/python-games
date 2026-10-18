import json
import pygame
from config import HEIGHT, LEVEL_CONFIG_PATH, WIDTH
from objects import Ball, Paddle, Wall
from scenes.base import COLOR_BLUE, COLOR_OVERLAY, COLOR_WHITE, COLOR_YELLOW, Scene


def load_level_configs():
    with LEVEL_CONFIG_PATH.open(encoding='utf-8') as config_file:
        config = json.load(config_file)
    return {int(level): values for level, values in config.items()}


LEVEL_CONFIGS = load_level_configs()


class SceneLevel(Scene):
    def __init__(self, context, level):
        Scene.__init__(self)

        self.context = context
        self.level = level
        self.config = LEVEL_CONFIGS[level]
        self.ball = Ball()
        self.player = Paddle()
        self.player.max_speed = self.config['paddle_speed']
        self.wall = Wall(self.config['layout'])

        self.score = context['score']
        self.lives = self.config['lives']
        self.waiting_to_serve = True
        self.paused = False
        self.pause_selection = 0
        self.pause_options = ('Resume', 'Level menu', 'Exit game')

        pygame.key.set_repeat(30)

    def read_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_p:
                self.paused = True
                pygame.key.set_repeat(0)
                continue
            if self.paused:
                self.read_pause_event(event)
                continue
            self.player.update(event)
            if self.waiting_to_serve and event.key == pygame.K_SPACE:
                self.waiting_to_serve = False
                horizontal_speed = self.config['speed'][0]
                vertical_speed = self.config['speed'][1]
                direction = 1 if self.ball.rect.centerx < WIDTH / 2 else -1
                self.ball.speed = [direction * horizontal_speed, -vertical_speed]

    def read_pause_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.paused = False
            pygame.key.set_repeat(30)
            return
        if event.key == pygame.K_UP:
            self.pause_selection = (self.pause_selection - 1) % len(self.pause_options)
        elif event.key == pygame.K_DOWN:
            self.pause_selection = (self.pause_selection + 1) % len(self.pause_options)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            choice = self.pause_options[self.pause_selection]
            if choice == 'Resume':
                self.paused = False
                pygame.key.set_repeat(30)
            elif choice == 'Level menu':
                self.change_scene('LevelsMenu')
            else:
                self.playing = False

    def update(self):
        if self.paused:
            return

        if not self.waiting_to_serve:
            self.ball.update()
        else:
            self.ball.rect.midbottom = self.player.rect.midtop

        if pygame.sprite.collide_rect(self.ball, self.player):
            self.ball.speed[1] = -self.ball.speed[1]

        collided_bricks = pygame.sprite.spritecollide(self.ball, self.wall, False)
        if collided_bricks:
            brick = collided_bricks[0]
            center_x = self.ball.rect.centerx
            if center_x < brick.rect.left or center_x > brick.rect.right:
                self.ball.speed[0] = -self.ball.speed[0]
            else:
                self.ball.speed[1] = -self.ball.speed[1]
            self.wall.remove(brick)
            self.score += 10
            self.context['score'] = self.score

        if not self.wall:
            self.context['completed_levels'].add(self.level)
            self.context['unlocked_level'] = min(10, max(self.context['unlocked_level'], self.level + 1))
            if self.level == 10:
                self.change_scene('GameOver')
            else:
                self.change_scene('LevelsMenu')
            return

        if self.ball.rect.top > HEIGHT:
            self.lives -= 1
            self.waiting_to_serve = True

        if self.lives <= 0:
            self.change_scene('GameOver')

    def draw(self, screen):
        screen.fill(COLOR_BLUE)
        self.show_score(screen)
        self.show_lives(screen)
        screen.blit(self.ball.image, self.ball.rect)
        screen.blit(self.player.image, self.player.rect)
        self.wall.draw(screen)
        if self.paused:
            self.draw_pause_menu(screen)

    def draw_pause_menu(self, screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont('Arial', 48)
        option_font = pygame.font.SysFont('Consolas', 24)
        title = title_font.render('Paused', True, COLOR_WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH / 2, 140)))
        for index, option in enumerate(self.pause_options):
            color = COLOR_YELLOW if index == self.pause_selection else COLOR_WHITE
            text = option_font.render(option, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH / 2, 200 + index * 45)))

    def show_score(self, screen):
        font = pygame.font.SysFont('Consolas', 20)
        text = font.render(str(self.score).zfill(5), True, COLOR_WHITE)
        text_rect = text.get_rect()
        text_rect.topleft = [0, 0]
        screen.blit(text, text_rect)

    def show_lives(self, screen):
        font = pygame.font.SysFont('Consolas', 20)
        label = "Lives: " + str(self.lives).zfill(2)
        text = font.render(label, True, COLOR_WHITE)
        text_rect = text.get_rect()
        text_rect.topright = [WIDTH, 0]
        screen.blit(text, text_rect)
