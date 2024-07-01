import time

import pygame
import pymunk
pygame.init()


# Define object class
class Object():
    def __init__(self, mass, size: tuple, position: tuple, color: tuple, space) -> None:
        self.mass = mass
        self.size_x, self.size_y = size
        self.x, self.y = position
        self.color = color

        self.object_var = pymunk.Body(self.mass)
        self.object_var.position = (self.x, self.y)
        
        self.poly = pymunk.Poly.create_box(self.object_var)
        self.poly.mass = self.mass

        space.add(self.object_var, self.poly)

    def update(self):
        self.x, self.y = self.object_var.position
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size_x, self.size_y))


# Set pymunk variables
space = pymunk.Space()
space.gravity = (0, 10000)

# Set pygame variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Simulation")

# Declare objects
objs = [Object(10, (20, 20), (250, 0), BLUE, space)]

# Main loop
for _ in range(100):
    space.step(0.01)

    # Initialize window
    win.fill(WHITE)

    # Update object position and draw
    for o in objs:
        o.update()
        o.draw(win)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    time.sleep(0.1)
