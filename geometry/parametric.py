from geometry.base import Geometry
from abc import ABC, abstractmethod

class ParametricGeometry(Geometry, ABC):
    @abstractmethod
    def __init__(self, u_start, u_end, u_resolution, v_start, v_end, v_resolution, surface_function) -> None:
        super().__init__()

        d_u = (u_end - u_start) / u_resolution
        d_v = (v_end - v_end) / v_resolution
        positions = []

        for u_idx in range(u_resolution + 1):
            v_array = []
            for v_idx in range(v_resolution + 1):
                u = u_start + u_idx * d_u
                v = v_start + v_idx * d_v
                v_array.append(surface_function(u, v))
            positions.append(v_array)

        position_data = []
        color_data = []

        c1, c2, c3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        c4, c5, c6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        for x in range(u_resolution):
            for y in range(v_resolution):
                pA = positions[x][y]
                pB = positions[x+1][y]
                pC = positions[x+1][y+1]
                pD = positions[x][y+1]

                position_data += [
                    pA.copy(), pB.copy(), pC.copy(),
                    pA.copy(), pC.copy(), pD.copy()
                ]

                color_data += [c1, c2, c3, c4, c5, c6]

        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.count_vertices()