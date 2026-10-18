import pygame
from config import HEIGHT, WIDTH
from objects import Ball, Paddle, Wall

COLOR_BLUE = (0, 0, 64)         # Blue color for the background.
COLOR_WHITE = (255, 255, 255)   # White color, for text.

class Scene:
    """Skeleton for each of the game's scenes."""

    def __init__(self):
        self.next_scene = False
        self.playing = True

    def read_events(self, events):
        """Read events to interact with the objects."""
        pass

    def update(self):
        """Update the objects on the screen."""
        pass

    def draw(self, screen):
        """Draw the objects on the screen."""
        pass

    def change_scene(self, scene):
        """Change the game scene."""
        self.next_scene = scene

class SceneLevel(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.ball = Ball()
        self.player = Paddle()
        self.wall = Wall(50)

        self.score = 0
        self.lives = 3
        self.waiting_to_serve = True

        # Set key repeat delay for held-down keys.
        pygame.key.set_repeat(30)

    def read_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.player.update(event)
                if self.waiting_to_serve and event.key == pygame.K_SPACE:
                    self.waiting_to_serve = False
                    if self.ball.rect.centerx < WIDTH / 2:
                        self.ball.speed = [3, -3]
                    else:
                        self.ball.speed = [-3, -3]

    def update(self):
        # Update the ball's position.
        if not self.waiting_to_serve:
            self.ball.update()
        else:
            self.ball.rect.midbottom = self.player.rect.midtop

        # Collision between ball and player.
        if pygame.sprite.collide_rect(self.ball, self.player):
            self.ball.speed[1] = -self.ball.speed[1]

        # Collision between ball and wall.
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

        # Check whether the ball left the screen.
        if self.ball.rect.top > HEIGHT:
            self.lives -= 1
            self.waiting_to_serve = True

        if self.lives <= 0:
            self.change_scene('GameOver')

    def draw(self, screen):
        # Fill the screen.
        screen.fill(COLOR_BLUE)
        # Show the score.
        self.show_score(screen)
        # Show the lives.
        self.show_lives(screen)
        # Draw the ball on the screen.
        screen.blit(self.ball.image, self.ball.rect)
        # Draw the player on the screen.
        screen.blit(self.player.image, self.player.rect)
        # Draw the bricks.
        self.wall.draw(screen)

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


class SceneGameOver(Scene):
    def update(self):
        self.playing = False

    def draw(self, screen):
        font = pygame.font.SysFont('Arial', 72)
        text = font.render('Game over :(', True, COLOR_WHITE)
        text_rect = text.get_rect()
        text_rect.center = [WIDTH / 2, HEIGHT / 2]
        screen.blit(text, text_rect)
