import pygame
import pymunk
import pymunk.pygame_util
pygame.init()


# Define object class
class Object():
    def __init__(self, mass, radius: float, position: tuple, color: tuple, space) -> None:
        self.mass = mass
        self.radius = radius
        self.x, self.y = position
        self.color = color

        self.object_var = pymunk.Body()
        self.object_var.position = (self.x, self.y)
        
        self.poly = pymunk.Circle(self.object_var, self.radius)
        self.poly.mass = self.mass
        self.poly.color = self.color

        space.add(self.object_var, self.poly)


def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 2.5), (width, 5)],
        [(width / 2, 2.5), (width, 5)],
        [(2.5, height / 2), (5, height)],
        [(width - 2.5, height / 2), (5, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        space.add(body, shape)


# Define main loop
def run(win, space, fps):
    create_boundaries(space, 700, 700)
    clock = pygame.time.Clock()
    run = True

    while run:
        # Update simulation
        space.step(1 / fps)
        clock.tick(fps)

        # Initialize window
        win.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()


win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Simulation")

# Set pymunk variables
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(win)

# Declare objects
objs = [Object(10, 20, (250, 250), (0, 0, 0, 100), space)]

# Start main_loop
if __name__ == "__main__":
    run(win, space, 50)
