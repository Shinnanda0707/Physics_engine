import pymunk

space = pymunk.Space()
space.gravity = (0, -981)

obj = pymunk.Body()
obj.position = (0, 0)

obj_poly = pymunk.Poly.create_box(obj)
obj_poly.mass = 10
space.add(obj, obj_poly)

print_option = pymunk.SpaceDebugDrawOptions()

for _ in range(100):
    space.step(0.02)
    space.debug_draw(print_option)
