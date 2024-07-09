import pymunk
import pymunk.pygame_util
import pygame
import math

fps = 100
dt = 1/fps

pygame.init()

WIDTH, HEIGHT = 1500, 750
window = pygame.display.set_mode((WIDTH, HEIGHT))

#마우스가 그리는 선 길이
def calculate_distance(p1,p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

#그 길이 앵글
def calculate_angle(p1,p2):
    return math.atan2(p2[1] - p1[1] , p2[0] - p1[0])

def visualize_velocity(window, balls, font, scale_factor: float, is_pause) -> None:
    for ball in balls:
        # Get velocity and position of each ball
        vel_x, vel_y = ball[0].body.velocity
        pos_x, pos_y = ball[0].body.position

        # Write mass and velocity
        mass_info = font.render(f"mass: {ball[0].mass}", True, (0, 0, 0))
        if is_pause:
            vel_info = font.render(f"vel: {round(math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)), 2)}", True, (0, 0, 0))
            window.blit(vel_info, (pos_x - 10, pos_y - 50))
        else:
            if ball[1]:
                vel_x, vel_y = ball[1]
                vel_info = font.render(f"vel: {round(math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)), 2)}", True, (0, 0, 0))
                window.blit(vel_info, (pos_x - 10, pos_y - 50))
        window.blit(mass_info, (pos_x - 10, pos_y - 70))
        

        # Make guideline pointing ball's moving direction
        pygame.draw.line(window, (225, 0, 0), (pos_x, pos_y), (pos_x + vel_x * scale_factor, pos_y + vel_y * scale_factor))


#배경 그리기
def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)

def create_segment(space, first_pos, line):
    if line:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        #body.position = pos
        shape = pymunk.Segment(body, line[0], line[1], 3)#3은 두께
        shape.elasticity = 0
        shape.friction = 0
        space.add(body, shape)
    if first_pos:
        pygame.draw.line(window, "black", first_pos, pygame.mouse.get_pos(), 3)#3은 두께
        

#배경 벽
def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 2.5), (width, 5)],
        [(width / 2, 2.5), (width, 5)],
        [(2.5, height / 2), (5, height)],
        [(width - 2.5, height / 2), (5, height)] 
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.1
        shape.friction = 0
        space.add(body, shape)

#볼1 만들기
def create_Ball(space, radius, mass, pos, balls, is_pause):
    if is_pause:
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC) #is_pause가 True이면 DYNAMIC
    else:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0
    shape.color = (199, 199 , 199, 100)
    space.add(body, shape)
    balls.append([shape, None])
    return shape, balls

def shoot_balls():
    pass

#main
def run(window, width, height):
    run = True
    clock = pygame.time.Clock()

    line = None
    first_pos = None
    pressed_pos = None
    is_pause = False
    mode = 1

    balls = []

    pygame.display.set_caption("Sootk")
    Font = pygame.font.SysFont("Consolas", 20, True, False)

    space = pymunk.Space()
    space.gravity = (0,2000)

    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)
    
    while run:

        if mode % 3 == 1:
            Text = Font.render("Mode : Create_Ball", True, (34,139,34))
        elif mode % 3 == 2:
            Text = Font.render("Mode : Draw_Lines", True, (34,139,34))
        elif mode % 3 == 0:
            Text = Font.render("Mode : Shoot_Ball", True, (34,139,34))
        
        if is_pause:
            Text_1 = Font.render("STATUS : MOVE", True, (34,139,34))
        else:
            Text_1 = Font.render("STATUS : STOP", True, (34,139,34))
        
        window.blit(Text, (10,10))
        window.blit(Text_1, (10,30))
        visualize_velocity(window, balls, Font, 0.1, is_pause)
        
        pygame.display.update()

        #Ball 감지
        mouse_pos = pymunk.pygame_util.get_mouse_pos(window)
        near_shape = space.point_query_nearest(
            mouse_pos, float("inf"), pymunk.ShapeFilter()
        ).shape
        print(near_shape)
        if near_shape is not None and isinstance(near_shape, pymunk.Circle):
            r = near_shape.radius + 4
            pygame.draw.circle(window, pygame.Color("red"), near_shape.body.position, int(r), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode % 3 == 1:
                    create_Ball(space,30,10,pygame.mouse.get_pos(),balls, is_pause)

                elif mode % 3 == 2:
                    if not first_pos:
                        first_pos = pygame.mouse.get_pos()
                    else:
                        line = [first_pos, pygame.mouse.get_pos()]
                        first_pos = None
                
                elif mode % 3 == 0:
                    pass
                

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if is_pause:
                        for ball in balls:
                            ball[1] = ball[0].body.velocity
                            ball[0].body.body_type = pymunk.Body.STATIC
                        is_pause = False
                    else:
                        for ball in balls:
                            ball[0].body.body_type = pymunk.Body.DYNAMIC
                            if ball[1]:
                                ball[0].body.velocity = ball[1]
                        is_pause = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mode += 1
                line = None
                first_pos = None


        draw(space, window, draw_options)
        create_segment(space, first_pos, line)

        space.step(dt)
        clock.tick(fps)

#인터프리터에서 직접 실행시 실행
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
