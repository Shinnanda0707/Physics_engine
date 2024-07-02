def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption("text")
    Font = pygame.font.SysFont("arial", 20, True, False)

    balls = []
    line = []
    mode = 1

    space = pymunk.Space()
    space.gravity = (0,1000)

    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    first_pos = None
    
    while run:
        Text = Font.render("asdf", True, (34,139,34))
        window.blit(Text, (width/2,height/2))
        pygame.display.update()
