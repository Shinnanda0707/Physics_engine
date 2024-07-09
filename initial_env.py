import pymunk

objs = []
 
# Define object class
class Object():
    def __init__(
            self, space,
            name: str,
            mass: float,
            size: tuple[float, float],
            position: tuple[float, float],
            initial_velocity: tuple[float, float]
        ) -> None:
        self.mass = mass
        self.size = size
        self.name = name
        self.initial_velocity = initial_velocity

        self.object_var = pymunk.Body()
        self.object_var.position = position
        self.object_var.velocity = initial_velocity

        self.poly = pymunk.Poly.create_box(self.object_var, self.size)
        self.poly.mass = self.mass
        self.poly.color = (255, 255, 255, 1)

        space.add(self.object_var, self.poly)
        objs.append(self)
    
    def apply_force(self, mag: tuple[float, float], time: int) -> None:
        vel_x, vel_y = self.object_var.velocity
        self.object_var.velocity = (vel_x + mag[0] / self.mass), (vel_y + mag[1] / self.mass)


class StaticTrack():
    def __init__(
            self, space,
            start_pos: tuple[float, float],
            end_pos: tuple[float, float]
        ) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos

        self.object_var = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.poly = pymunk.Segment(self.object_var, self.start_pos, self.end_pos)
        self.poly.color = (255, 255, 255, 1)

        space.add(self.object_var, self.poly)


# Code here for initial environment
def create_env(space) -> None:
    # obj1 = Object(space, "A", 10, (50, 50), (80, 100), (120, 0))
    obj1 = Object(space, "A", 10, (50, 50), (80, 100), (300, 0))
    obj2 = Object(space, "B", 20, (50, 50), (700, 100), (0, 0))
