import math

import pygame
import pymunk
import pymunk.pygame_util
pygame.init()


def draw(win, space, draw_options):
    win.fill("white")
    space.debug_draw(draw_options)


def create_ball(space, radius, mass, x=250, y=250):
    body = pymunk.Body()
    body.position = (x, y)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)

    return shape


def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        space.add(body, shape)


def run(win):
    run = True
    clock = pygame.time.Clock()
    fps = 50

    space = pymunk.Space()
    space.gravity = (0, 982)

    ball = create_ball(space, 30, 10)
    create_boundaries(space, 500, 500)

    draw_options = pymunk.pygame_util.DrawOptions(win)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(win, space, draw_options)
        space.step(1 / fps)
        clock.tick(fps)
        pygame.display.update()
    pygame.quit()


win = pygame.display.set_mode((500, 500))

if __name__ == "__main__":
    run(win)
