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
    def __init__(self, layout):
        pygame.sprite.Group.__init__(self)

        sample_brick = Brick((0, 0))
        columns = WIDTH // sample_brick.rect.width
        positions = self.layout_positions(layout, columns)
        for column, row in positions:
            position = (column * sample_brick.rect.width, 20 + row * sample_brick.rect.height)
            self.add(Brick(position))

    @staticmethod
    def layout_positions(layout, columns):
        positions = set()

        def add_row(row, start, end, step=1):
            for column in range(start, end, step):
                if 0 <= column < columns:
                    positions.add((column, row))

        if layout == 'rows':
            for row in range(1):
                add_row(row, 0, columns)
        elif layout == 'pyramid':
            for row in range(6):
                width = 2 + row * 2
                start = (columns - width) // 2
                add_row(row, start, start + width)
        elif layout == 'diamond':
            widths = [4, 6, 8, 10, 8, 6, 4]
            for row, width in enumerate(widths):
                start = (columns - width) // 2
                add_row(row, start, start + width)
        elif layout == 'checkerboard':
            for row in range(7):
                add_row(row, row % 2, columns, 2)
        elif layout == 'tunnel':
            for row in range(6):
                add_row(row, 0, 4)
                add_row(row, columns - 4, columns)
                if row in (0, 5):
                    add_row(row, 4, columns - 4)
        elif layout == 'zigzag':
            for row in range(7):
                start = 1 if row % 2 else columns // 3
                add_row(row, start, start + columns // 2)
        elif layout == 'fortress':
            for row in range(6):
                add_row(row, 0, 2)
                add_row(row, columns - 2, columns)
            add_row(0, 2, columns - 2)
            add_row(5, 2, columns - 2)
        elif layout == 'waves':
            for row in range(7):
                start = (row * 2) % 6
                add_row(row, start, columns - start)
        elif layout == 'cross':
            center = columns // 2
            for row in range(7):
                add_row(row, center - 1, center + 2)
            add_row(2, 2, columns - 2)
            add_row(3, 2, columns - 2)
            add_row(4, 2, columns - 2)
        elif layout == 'dense':
            for row in range(8):
                add_row(row, 0, columns)

        return positions
