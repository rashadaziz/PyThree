from geometry.base import Geometry
from math import sin, cos, pi

class PolygonGeometry(Geometry):
    def __init__(self, sides=3, radius=1) -> None:
        super().__init__()

        base_angle = 2*pi/sides

        position_data = []
        color_data = []
        uv_data = []
        uv_center = [.5, .5]
        normal_data = []
        normal_vector = [0, 0, 1]

        for n in range(sides):
            position_data.append([0, 0, 0])
            position_data.append([radius*cos(n*base_angle), radius*sin(n*base_angle), 0])
            position_data.append([radius*cos((n+1)*base_angle), radius*sin((n+1)*base_angle), 0])

            color_data.append([1, 1, 1])
            color_data.append([1, 0, 0])
            color_data.append([0, 0, 1])

            uv_data.append(uv_center)
            uv_data.append([cos(n*base_angle)*.5 + .5, sin(n*base_angle)*.5 + .5])
            uv_data.append([cos((n+1)*base_angle)*.5 + .5, sin((n+1)*base_angle)*.5 + .5])

            normal_data.append(normal_vector)
            normal_data.append(normal_vector)
            normal_data.append(normal_vector)

        self.add_attribute('vec3', "vertexNormal", normal_data)
        self.add_attribute('vec3', "faceNormal", normal_data)
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.count_vertices()