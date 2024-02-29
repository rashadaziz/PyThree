from geometry.base import Geometry
from math import sin, cos, pi

class Polygon(Geometry):
    def __init__(self, sides=3, radius=1) -> None:
        super().__init__()

        base_angle = 2*pi/sides

        position_data = []
        color_data = []

        for n in range(sides):
            position_data.append([0, 0, 0])
            position_data.append([radius*cos(n*base_angle), radius*sin(n*base_angle), 0])
            position_data.append([radius*cos((n+1)*base_angle), radius*sin((n+1)*base_angle), 0])

            color_data.append([1, 1, 1])
            color_data.append([1, 0, 0])
            color_data.append([0, 0, 1])

        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.count_vertices()