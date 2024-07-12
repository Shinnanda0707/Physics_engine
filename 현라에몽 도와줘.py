import pymunk
import pymunk.pygame_util
import pygame
import math

fps = 100
dt = 1/fps

#init
pygame.init()

WIDTH, HEIGHT = 1500, 750
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Calculate distance
def calculate_distance(p1,p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

# Calculate tan value
def calculate_angle(p1,p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

#visualize velocity and mass
def visualize_velocity(window, balls, font, scale_factor: float, is_pause) -> None:
    for ball in balls:

        vel_x, vel_y = ball[0].body.velocity
        pos_x, pos_y = ball[0].body.position

        mass_info = font.render(f"{int(ball[0].mass)}kg", True, (0, 0, 0))
        if is_pause:
            vel_info = font.render(f"{int(round(math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)), 0))}m/s", True, (0, 0, 0))
            window.blit(vel_info, (pos_x - 20, pos_y - 50))
        else:
            if ball[1]:
                vel_x, vel_y = ball[1]
                vel_info = font.render(f"{int(round(math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)), 2))}m/s", True, (0, 0, 0))
                window.blit(vel_info, (pos_x - 20, pos_y - 50))
        window.blit(mass_info, (pos_x - 20, pos_y - 70))
        
        pygame.draw.line(window, (225, 0, 0), (pos_x, pos_y), (pos_x + vel_x * scale_factor, pos_y + vel_y * scale_factor))

# Draw Background
def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)

# Create Segment(실체 있음)
def create_segment(space, first_pos, line):
    if line:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, line[0], line[1], 3)  # 3은 두께
        shape.elasticity = 0
        shape.friction = 0
        space.add(body, shape)
    if first_pos:
        pygame.draw.line(window, "black", first_pos, pygame.mouse.get_pos(), 3)  # 3은 두께

# Create Walls
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

# Create Ball
def create_Ball(space, radius, mass, pos, balls, is_pause):
    if is_pause:
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)  # is_pause가 True이면 DYNAMIC
    else:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0
    shape.color = (199, 199, 199, 100)
    space.add(body, shape)
    shape.collision_type = 1
    balls.append([shape, None])
    return shape, balls

#Draw line(실체 없음)
def draw_line(window, first_pos):
    pygame.draw.line(window, "black", first_pos, pygame.mouse.get_pos(), 3)

#sound / detect collision
def post_solve(arbiter, space, data):
    impulse = abs(arbiter.total_impulse)
    if impulse != 0:
        print(impulse)
        #volume = impulse  # 최대 볼륨은 1.0으로 제한
        pygame.mixer.init()
        collision_sound = pygame.mixer.Sound("collision_sound.mp3")
        #collision_sound.set_volume(volume)
        collision_sound.play()
        return True  # 충돌 계속 처리

# main
def run(window, width, height):
    run = True
    clock = pygame.time.Clock()

    line = None
    first_pos = None
    is_pause = False
    mode = 1

    selected_shape = None

    balls = []
    Font = pygame.font.SysFont("Consolas", 20, True, False)

    space = pymunk.Space()
    space.gravity = (0, 2000)

    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    #충돌 핸들러
    handler = space.add_collision_handler(1, 1)
    handler.post_solve = post_solve
    print(handler.post_solve)

    while run:
        draw(space, window, draw_options)
        pygame.display.set_caption(f"Sootk / fps : {clock.get_fps()}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode % 3 == 1:
                    selected_shape = None
                    create_Ball(space, 30, 10, pygame.mouse.get_pos(), balls, is_pause)

                elif mode % 3 == 2:
                    selected_shape = None
                    if not first_pos:
                        first_pos = pygame.mouse.get_pos()
                    else:
                        line = [first_pos, pygame.mouse.get_pos()]
                        first_pos = None
                
                elif mode % 3 == 0:
                    if near_shape and selected_shape is None and isinstance(near_shape, pymunk.Circle):
                        selected_shape = near_shape
                    elif selected_shape:
                        angle = calculate_angle(selected_shape.body.position, pygame.mouse.get_pos())
                        force = calculate_distance(selected_shape.body.position, pygame.mouse.get_pos()) * 50
                        fx = math.cos(angle) * force
                        fy = math.sin(angle) * force
                        selected_shape.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                        selected_shape = None

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

        if mode % 3 == 1:
            Text = Font.render("Mode : Create_Ball", True, (34, 139, 34))
        elif mode % 3 == 2:
            Text = Font.render("Mode : Draw_Lines", True, (34, 139, 34))
        elif mode % 3 == 0:
            Text = Font.render("Mode : Shoot_Ball", True, (34, 139, 34))

        if is_pause:
            Text_1 = Font.render("STATUS : MOVE", True, (34, 139, 34))
        else:
            Text_1 = Font.render("STATUS : STOP", True, (34, 139, 34))

        window.blit(Text, (10, 10))
        window.blit(Text_1, (10, 30))
        visualize_velocity(window, balls, Font, 0.1, is_pause)

        if mode % 3 == 0 and selected_shape is None:
            # Ball 감지
            mouse_pos = pymunk.pygame_util.get_mouse_pos(window)
            near_shape = space.point_query_nearest(
                mouse_pos, float("inf"), pymunk.ShapeFilter()
            ).shape
            if near_shape is not None and isinstance(near_shape, pymunk.Circle):
                r = near_shape.radius + 4
                pygame.draw.circle(window, pygame.Color("blue"), near_shape.body.position, int(r), 2)

        elif mode % 3 == 0 and selected_shape:
            r = selected_shape.radius + 4
            pygame.draw.circle(window, pygame.Color("red"), selected_shape.body.position, int(r), 2)

        if selected_shape:
            draw_line(window, selected_shape.body.position)

        create_segment(space, first_pos, line)
        space.step(dt)
        clock.tick(fps)
        pygame.display.update()

# 인터프리터에서 직접 실행시 실행
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
