import sys    # to use exit()
import time   # to use sleep()
import pygame

WIDTH = 640   # Screen width.
HEIGHT = 480  # Screen height.
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


class Director:
    def __init__(self, title="", resolution=(WIDTH, HEIGHT)):
        pygame.init()
        # Initialize the screen.
        self.screen = pygame.display.set_mode(resolution)
        # Set the window title.
        pygame.display.set_caption(title)
        # Create the clock.
        self.clock = pygame.time.Clock()
        self.scene = None
        self.scenes = {}

    def run(self, initial_scene, fps=60):
        self.scene = self.scenes[initial_scene]
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

            self.scene.read_events(events)
            self.scene.update()
            self.scene.draw(self.screen)

            self.choose_scene(self.scene.next_scene)

            if playing:
                playing = self.scene.playing

            pygame.display.flip()

        time.sleep(3)

    def choose_scene(self, next_scene):
        if next_scene:
            if next_scene not in self.scenes:
                self.add_scene(next_scene)
            self.scene = self.scenes[next_scene]

    def add_scene(self, scene):
        scene_class_name = 'Scene' + scene
        scene_class = globals()[scene_class_name]
        self.scenes[scene] = scene_class()


class SceneLevel1(Scene):
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
        self.speed = [3, 3]

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
            self.speed = [-5, 0]
        # Check whether the right arrow was pressed.
        elif event.key == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.speed = [5, 0]
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


director = Director('Brick Game', (WIDTH, HEIGHT))
director.add_scene('Level1')
director.run('Level1')