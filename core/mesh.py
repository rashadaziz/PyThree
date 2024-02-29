from core.Object3D import Object3D
from geometry.base import Geometry
from material.base import Material
from OpenGL.GL import *

class Mesh(Object3D):
    def __init__(self, geometry: Geometry, material: Material) -> None:
        super().__init__()
        
        self.geometry = geometry
        self.material = material

        self.visible = True

        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)

        # bind position and color data to variables
        for var_name, attrib_obj in geometry.attributes.items():
            attrib_obj.associate_variable(material.program_ref, var_name)
        
        glBindVertexArray(0)