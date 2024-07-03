import pymunk
import pymunk.pygame_util
import pygame
import math
import sys

fps = 60
dt = 1/fps

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

#마우스가 그리는 선 길이
def calculate_distance(p1,p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

#그 길이 앵글
def calculate_angle(p1,p2):
    return math.atan2(p2[1] - p1[1] , p2[0] - p1[0])

#배경 그리기
def draw(space, window, draw_options, line):
    window.fill("white")

    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)#3은 두께


    space.debug_draw(draw_options)
    pygame.display.update()

#배경 벽
def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)] 
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 1
        shape.friction = 0.5
        space.add(body, shape)

#볼1 만들기
def create_Ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 0 ,0, 100)
    space.add(body, shape)
    return shape

#main
def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption("text")
    Font = pygame.font.SysFont("arial", 20, True, False)
    Text = Font.render("asdf", True, (34,139,34))

    balls = []
    line = None
    first_pos = None
    mode = 1

    space = pymunk.Space()
    space.gravity = (0,1000)

    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)
    
    while run:
        window.blit(Text, (width/2,height/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode % 3 == 1:
                    pressed_pos = pygame.mouse.get_pos()
                    for _ in range(5):
                        ball = create_Ball(space, 30, 100, pressed_pos)
                        ball.body.body_type = pymunk.Body.DYNAMIC
                        balls.append(ball)

                elif mode % 3 == 2:
                    if balls:
                        for i in range(5):
                            space.remove(balls[i], balls[i].body)
                        for _ in range(5):
                            del balls[0]
                    else:
                        balls.remove
            
                elif mode % 3 == 0:
                    if not first_pos:
                        first_pos = pygame.mouse.get_pos()
                    else:
                        line = [first_pos, pygame.mouse.get_pos()]

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mode += 1


        draw(space, window, draw_options, line)
        if line:
            line = None

        space.step(dt)
        clock.tick(fps)

#인터프리터에서 직접 실행시 실행
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
