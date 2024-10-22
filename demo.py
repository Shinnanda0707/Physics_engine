import math
from random import choice

import pygame
import pymunk
import pymunk.pygame_util
pygame.init()
font = pygame.font.SysFont("Consolas", 20)


# Define object class
class Object():
    def __init__(self, mass: float, radius: float, position: tuple, color: tuple, space) -> None:
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
        space.add(body, shape)


def create_guide_line(window, start_pos: tuple, line_started: bool) -> None:
    if line_started:
        pygame.draw.line(window, (0, 255, 0), start_pos, pygame.mouse.get_pos(), 2)


def visualize_velocity(window, balls, font, scale_factor: float) -> None:
    for ball in balls:
        # Get velocity and position of each ball
        vel_x, vel_y = ball.object_var.velocity
        pos_x, pos_y = ball.object_var.position

        # Write mass and velocity
        mass_info = font.render(f"mass: {ball.mass}", True, (0, 0, 0))
        vel_info = font.render(f"vel: {round(math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)), 2)}", True, (0, 0, 0))
        window.blit(mass_info, (pos_x - 10, pos_y - 70))
        window.blit(vel_info, (pos_x - 10, pos_y - 50))

        # Make guideline pointing ball's moving direction
        pygame.draw.line(window, (225, 0, 0), (pos_x, pos_y), (pos_x + vel_x * scale_factor, pos_y + vel_y * scale_factor))


# Define main loop
def run(win, space, fps: int, balls: list) -> None:
    create_boundaries(space, 700, 700)
    clock = pygame.time.Clock()
    run = True
    mode = "ball"
    line_started = False
    line_start_pos = (0, 0)
    info = font.render("ball(b), line(l)", False, (0, 0, 0))

    while run:
        # Update simulation
        space.step(1 / fps)
        clock.tick(fps)

        # Initialize window
        win.fill((255, 255, 255))
        space.debug_draw(draw_options)

        # Show mode on window
        surface = font.render(f"Mode: {mode}", True, (0, 0, 0))
        win.blit(surface, (10, 10))
        win.blit(info, (10, 30))

        # Create line when the variable mode is "line" and line was started
        create_guide_line(win, line_start_pos, line_started)

        # Show velocity and mass above balls + draw line toward balls' moving direction
        visualize_velocity(win, balls, font, 0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            # Change draw mode
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    mode = "ball"
                    if line_started:
                        line_started = False
                elif event.key == pygame.K_l:
                    mode = "line"
            
            # Draw objects
            if event.type == pygame.MOUSEBUTTONDOWN:
                bt_left, _, bt_right = pygame.mouse.get_pressed()
                if bt_left:
                    # Ball falling mode
                    if mode == "ball":
                        balls.append(Object(10, 20, pygame.mouse.get_pos(), (0, 0, 0, 100), space))
                    
                    # Line drawing mode
                    elif mode == "line":
                        if not line_started:
                            line_started = True
                            line_start_pos = pygame.mouse.get_pos()
                        else:
                            line_started = False
                            body = pymunk.Body(body_type=pymunk.Body.STATIC)
                            shape = pymunk.Segment(body, line_start_pos, tuple(pygame.mouse.get_pos()), 0)
                            shape.friction = 0
                            space.add(body, shape)
                
                # Apply impulse force to the object
                if bt_right:
                    for ball in balls:
                        f_x, f_y = choice([50, -50]), -500
                        v_x, v_y = ball.object_var.velocity
                        time = 7
                        ball.object_var.velocity = v_x + time * f_x / ball.mass, v_y + time * f_y / ball.mass
        
        # Update window
        pygame.display.update()
    pygame.quit()


win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Simulation")

# Set pymunk variables
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(win)

# Declare objects
balls = [Object(10, 20, (250, 250), (0, 0, 0, 100), space)]

# Start main_loop
if __name__ == "__main__":
    run(win, space, 50, balls)
