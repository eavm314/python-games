import time
import pygame
import random
import sys
import threading

# Set up the display window
WIDTH = 800
HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Snake class
class Snake:
  def __init__(self):    
    self.position = [100, 50]
    self.body = [[100, 50], [90, 50], [80, 50]]
    self.direction = "RIGHT"
    # self.change_to = self.direction
    
  def change_direction(self, direction):
    if direction == "RIGHT" and not self.direction == "LEFT":
      self.direction = "RIGHT"
    if direction == "LEFT" and not self.direction == "RIGHT":
      self.direction = "LEFT"
    if direction == "UP" and not self.direction == "DOWN":
      self.direction = "UP"
    if direction == "DOWN" and not self.direction == "UP":
      self.direction = "DOWN"
      
  def move(self, food_pos):
    if self.direction == "RIGHT":
      self.position[0] += 10
    if self.direction == "LEFT":
      self.position[0] -= 10
    if self.direction == "UP":
      self.position[1] -= 10
    if self.direction == "DOWN":
      self.position[1] += 10
    self.body.insert(0, self.position.copy())
    if self.position == food_pos:
      return 1
    else:
      self.body.pop()
      return 0
      
  def check_collision(self):
    if self.position[0] > WIDTH - 10 or self.position[0] < 0:
      return 1
    elif self.position[1] > HEIGHT - 10 or self.position[1] < 0:
      return 1
    for body_part in self.body[1:]:
      if self.position == body_part:
        return 1
    return 0
      
  def get_body(self):
    return self.body
    
# Food class
class Food:
  def __init__(self):
    self.position = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    self.is_food_on_screen = True
    
  def draw_food(self, color, snake):
    pygame.draw.rect(window, color, pygame.Rect(self.position[0], self.position[1], 10, 10))
    if self.position in snake.get_body():
      self.is_food_on_screen = False
      
  def food_on_screen(self):
    return self.is_food_on_screen
    
  def update_food_position(self):
    if not self.is_food_on_screen:
      self.position = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
      self.is_food_on_screen = True

snake = Snake()
food = Food()
score = 0
game_over = False
fps = pygame.time.Clock()

def check_events():
  for event in pygame.event.get():
    # Quit the game if the user closes the window
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
      
    # Handle user input
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        snake.change_direction("UP")
      if event.key == pygame.K_s:
        snake.change_direction("DOWN")
      if event.key == pygame.K_a:
        snake.change_direction("LEFT")
      if event.key == pygame.K_d:
        snake.change_direction("RIGHT")

def update_game():
  if snake.move(food.position) == 1:
    global score, game_over
    score += 1
    food.is_food_on_screen = False
  if snake.check_collision() == 1:
    game_over = True
    return
    
  # Update the food's position and check if it has been eaten
  if not food.food_on_screen():
    food.update_food_position()
    
  # Clear the window
  window.fill(BLACK)
  
  # Draw the snake and food
  for pos in snake.get_body():
    pygame.draw.rect(window, WHITE, pygame.Rect(pos[0], pos[1], 10, 10))
  food.draw_food(WHITE, snake)
  
  # Update the display
  pygame.display.update()

# Run the game loop
while True:    

  check_events()
  # Update the snake's position and check for collisions
  if not game_over:
    update_game()
  
  fps.tick(30)

# Display the game over screen
if game_over:
  font = pygame.font.SysFont('Times New Roman', 32)
  text = font.render("Game Over! Your score: " + str(score), True, WHITE)
  window.blit(text, (WIDTH/3, HEIGHT/2))
  pygame.display.update()
  # time.sleep(10)
  # pygame.quit()
  # sys.exit()
