import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 480))

background = pygame.Surface(screen.get_size())
background.fill((255, 255, 255))
screen.blit(background, (0, 0))

player = pygame.Rect(100, 100, 50, 50)

pygame.draw.rect(screen, (0, 0, 255), player)

# Define los obstáculos.
obstacles = []
for i in range(10):
    obstacles.append(pygame.Rect(random.randint(0, screen.get_width()),
                                random.randint(0, screen.get_height()),
                                50, 50))
def update_obstacles(dt):
    # Mueve los obstáculos hacia abajo.
    for obstacle in obstacles:
        obstacle.y += 5 * dt
    # Elimina los obstáculos que se salgan de la pantalla.
    for obstacle in obstacles:
        if obstacle.y > screen.get_height():
            obstacles.remove(obstacle)

def draw_background(screen):
    screen.blit(background, (0, 0))

def draw_player(screen):
    pygame.draw.rect(screen, (0, 0, 255), player)

def draw_obstacles(screen):
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obstacle)

def die():
    print("You died!")
    pygame.quit()

def win():
    print("You won!")
    pygame.quit()

def lose():
    print("You lost!")
    pygame.quit()


def update_player(dt):
    # Mueve el jugador hacia la izquierda o hacia la derecha.
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        player.x -= 5* dt
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        player.x += 5* dt
    # Verifica si el jugador ha salido de la pantalla.
    if player.x < 0:
        player.x = 0
    elif player.x > screen.get_width():
        player.x = screen.get_width()
    # Verifica si el jugador ha chocado con un obstáculo.
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            # El jugador ha chocado con un obstáculo, así que muere.
            die()

# Define el reloj del juego.
clock = pygame.time.Clock()

# Define el ciclo de juego.
while True:
    # Actualiza el juego.
    dt = clock.tick(60)
    update_player(dt)
    update_obstacles(dt)
    # Dibuja el juego en la pantalla.
    screen.fill((0, 0, 0))
    draw_background(screen)
    draw_player(screen)
    draw_obstacles(screen)
    pygame.display.flip()
    # Verifica si el jugador ha ganado o perdido.
    if player.y > screen.get_height():
        win()
    elif player.y < 0:
        lose()
