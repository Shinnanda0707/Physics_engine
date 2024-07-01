import pygame
import pymunk
import pymunk.pygame_util
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


# Set pygame variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

fps = 50
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()
run = True

# Set pymunk variables
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(win)

# Declare objects
objs = [Object(10, (20, 20), (250, 0), BLUE, space)]

# Main loop
while run:
    # Update simulation
    space.step(1 / fps)
    clock.tick(fps)

    # Initialize window
    win.fill(WHITE)
    space.debug_draw(draw_options)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
