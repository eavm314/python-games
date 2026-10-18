import pygame
from config import HEIGHT, WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load the image.
        self.image = pygame.image.load('./assets/ball.png')
        # Get the image's rectangle.
        self.rect = self.image.get_rect()
        # Initial position centered on the screen.
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        # Set the initial speed.
        self.speed = [8, 10]

    def update(self):
        # Bounce off the top edge.
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Bounce off the left and right edges.
        elif self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Move based on current position and speed.
        self.rect.move_ip(self.speed)


class Paddle(pygame.sprite.Sprite):
    max_speed = 10  # Maximum speed of the paddle.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Load the image.
        self.image = pygame.image.load('./assets/player.png')
        # Get the image's rectangle.
        self.rect = self.image.get_rect()
        # Initial position, horizontally centered on the screen.
        self.rect.midbottom = (WIDTH / 2, HEIGHT - 20)
        # Set the initial speed.
        self.speed = [0, 0]

    def update(self, event):
        # Check whether the left arrow was pressed.
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-self.max_speed, 0]
        # Check whether the right arrow was pressed.
        elif event.key == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.speed = [self.max_speed, 0]
        else:
            self.speed = [0, 0]
        # Move based on current position and speed.
        self.rect.move_ip(self.speed)


class Brick(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # Load the image.
        self.image = pygame.image.load('./assets/brick.png')
        # Get the image's rectangle.
        self.rect = self.image.get_rect()
        # Initial position, provided externally.
        self.rect.topleft = position


class Wall(pygame.sprite.Group):
    def __init__(self, brick_count):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for _ in range(brick_count):
            brick = Brick((pos_x, pos_y))
            self.add(brick)

            pos_x += brick.rect.width
            if pos_x >= WIDTH:
                pos_x = 0
                pos_y += brick.rect.height
