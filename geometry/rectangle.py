from geometry.base import Geometry

class RectangleGeometry(Geometry):
    def __init__(self, width=1, height=1) -> None:
        super().__init__()

        p0 = [-width/2, -height/2, 0]
        p1 = [width/2, -height/2, 0]
        p2 = [-width/2, height/2, 0]
        p3 = [width/2, height/2, 0]

        c0 = [1, 1, 1]
        c1 = [1, 0, 0]
        c2 = [0, 1, 0]
        c3 = [0, 0, 1]

        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]

        position_data = [p0, p1, p3,  p0, p3, p2]
        color_data = [c0, c1, c3,  c0, c3, c2]
        uv_data = [t0, t1, t3,  t0, t3, t2]
        normal_data = [[0, 0, 1]] * 6

        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec3", "faceNormal", normal_data)
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.count_vertices()