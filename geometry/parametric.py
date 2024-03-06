from geometry.base import Geometry
from abc import ABC, abstractmethod
import numpy as np

class ParametricGeometry(Geometry, ABC):
    @abstractmethod
    def __init__(self, u_start, u_end, u_resolution, v_start, v_end, v_resolution, surface_function) -> None:
        super().__init__()

        def calculate_normal(p0, p1, p2):
            v1 = np.array(p1) - np.array(p0)
            v2 = np.array(p2) - np.array(p0)
            orthogonal_vector = np.cross(v1, v2)
            norm = np.linalg.norm(orthogonal_vector)
            normal_vector = orthogonal_vector / norm if norm > 1e-6 \
                else np.array(p0) / np.linalg.norm(p0)
            return normal_vector

        d_u = (u_end - u_start) / u_resolution
        d_v = (v_end - v_start) / v_resolution
        positions = []
        for u_idx in range(u_resolution + 1):
            v_array = []
            for v_idx in range(v_resolution + 1):
                u = u_start + u_idx * d_u
                v = v_start + v_idx * d_v
                v_array.append(surface_function(u, v))
            positions.append(v_array)
        
        uvs = []
        for u_idx in range(u_resolution + 1):
            v_array = []
            for v_idx in range(v_resolution + 1):
                u = u_idx / u_resolution
                v = v_idx / v_resolution
                v_array.append([u, v])
            uvs.append(v_array)

        vertex_normals = []
        for u_idx in range(u_resolution + 1):
            v_array = []
            for v_idx in range(v_resolution + 1):
                u = u_idx / u_resolution
                v = v_idx / v_resolution
                h = 1e-5
                p0 = surface_function(u, v)
                p1 = surface_function(u+h, v)
                p2 = surface_function(u, v+h)
                normal = calculate_normal(p0, p1, p2)
                v_array.append(normal)
            vertex_normals.append(v_array)

        position_data = []
        color_data = []
        uv_data = []
        vertex_normal_data = []
        face_normal_data = []

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

                uvA = uvs[x][y]
                uvB = uvs[x+1][y]
                uvC = uvs[x+1][y+1]
                uvD = uvs[x][y+1]

                uv_data += [uvA, uvB, uvC, uvA, uvC, uvD]

                nA = vertex_normals[x][y] 
                nB = vertex_normals[x+1][y] 
                nC = vertex_normals[x+1][y+1] 
                nD = vertex_normals[x][y+1] 
                vertex_normal_data += [nA,nB,nC, nA,nC,nD]

                fn0 = calculate_normal(pA, pB, pC)
                fn1 = calculate_normal(pA, pC, pD)
                face_normal_data += [fn0, fn0, fn0, fn1, fn1, fn1]

        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexNormal", position_data)
        self.add_attribute("vec3", "faceNormal", face_normal_data)
        self.count_vertices()