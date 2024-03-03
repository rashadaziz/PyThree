from geometry.base import Geometry
from core.utils import OBJECT_PATH
import numpy as np
import pywavefront


class ObjectGeometry(Geometry):
    def __init__(self, file_name: str, scale=1) -> None:
        super().__init__()

        scene = pywavefront.Wavefront(OBJECT_PATH + file_name, collect_faces=True, create_materials=True)

        position_data = []
        color_data = []
        
        # source: https://stackoverflow.com/questions/59923419/pyopengl-how-do-i-import-an-obj-file
        scene_box = (scene.vertices[0], scene.vertices[0])
        for vertex in scene.vertices:
            min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
            max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
            scene_box = (min_v, max_v)

        scene_translate = np.multiply(scale, [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)])
        
        for mesh in scene.mesh_list:
            for face in mesh.faces:
                for i in face:
                    position_data.append(np.multiply(scene.vertices[i], scale))
        ############################################################################################

        position_data = np.add(position_data, [scene_translate])

        colors = [[1,  0.5, 0.5], [0.5,  0,  0],
                  [0.5,  1, 0.5], [0,  0.5,  0],
                  [0.5,  0.5, 1], [0,  0,  0.5]]
        

        for i in range(len(position_data)):
            color_data.append(colors[i % len(colors)])

        self.add_attribute('vec3', "vertexPosition", position_data)
        self.add_attribute('vec3', "vertexColor", color_data)
        self.count_vertices()