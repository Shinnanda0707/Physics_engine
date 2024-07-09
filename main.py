import math

import pygame
import pymunk
import pymunk.pygame_util

from initial_env import objs, create_env
pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont("Consolas", 15)
sound = pygame.mixer.Sound("stomp.mp3")


def visualize_velocity(window, objs, font, scale_factor: float) -> None:
    for obj in objs:
        # Get velocity and position of each obj
        vel_x, vel_y = obj.object_var.velocity
        pos_x, pos_y = obj.object_var.position

        # Write mass and velocity
        mass_info = font.render(f"m={str(obj.mass)}", True, (0, 0, 0))
        vel_info = font.render(
            f"v={round(math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)))}",
            True, (0, 0, 0)
        )
        window.blit(mass_info, (pos_x - 17, pos_y + 5))
        window.blit(vel_info, (pos_x - 17, pos_y - 20))

        # Make guideline pointing obj's moving direction
        pygame.draw.line(window, (225, 0, 0), (pos_x, pos_y), (pos_x + vel_x * scale_factor, pos_y + vel_y * scale_factor))


def create_boundaries(space, width: float, height: float) -> None:
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
        shape.color = (255, 255, 255, 0)
        space.add(body, shape)


# Define main loop
def run(win, space, draw_options, fps=50, font=font):
    # Set variables for loop
    clock = pygame.time.Clock()
    run = True
    pause = False

    # Set boundaries
    create_boundaries(space, win.get_width(), win.get_height())

    # Set environment
    create_env(space)

    # Main loop
    while run:
        # Tick
        space.step(1 / fps)
        clock.tick(fps)

        # Reset window
        win.fill((0, 0, 0))
        space.debug_draw(draw_options)
        
        # Show mass & velocity above each object
        visualize_velocity(win, objs, font, 0.1)

        # Update window
        if not pause:
            pygame.display.update()

        # Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pause:
                        pause = True
                        vel = []
                        for obj in objs:
                            vel.append(obj.object_var.velocity)
                            obj.object_var.body_type = pymunk.Body.STATIC
                    else:
                        pause = False
                        for i in range(len(objs)):
                            objs[i].object_var.body_type = pymunk.Body.DYNAMIC
                            objs[i].object_var.velocity = vel[i]
    pygame.quit()


# Set pygame variables
win = pygame.display.set_mode((1300, 200))
pygame.display.set_caption("Simulation")

# Set pymunk variables
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(win)

# Start main loop
if __name__ == "__main__":
    run(win, space, draw_options)
