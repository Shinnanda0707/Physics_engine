import time

import pygame
import pymunk
pygame.init()


# Define object class
class Object():
    def __init__(self, size: tuple, position: tuple, color: tuple) -> None:
        self.size_x, self.size_y = size
        self.x, self.y = position
        self.color = color
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size_x, self.size_y))


# Set pymunk variables
space = pymunk.Space()
space.gravity = (0, 10000)

obj = pymunk.Body()
obj.position = (50, 0)

obj_poly = pymunk.Poly.create_box(obj)
obj_poly.mass = 10
space.add(obj, obj_poly)

# Set pygame variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Simulation")

# Declare objects
obj1 = Object((10, 10), tuple(obj.position), BLUE)

# Main loop
for _ in range(100):
    space.step(0.01)

    # Initialize window
    win.fill(WHITE)

    # Update object position
    obj1.x, obj1.y = obj.position
    
    # Draw object
    obj1.draw(win)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    time.sleep(0.1)
