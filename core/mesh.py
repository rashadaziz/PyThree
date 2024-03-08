from core.Object3D import Object3D
from core.camera import Camera
from core.light import Light
from geometry.base import Geometry
from material.base import Material
from typing import List
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

    def render(self, camera: Camera, lights: List[Light], manual_settings=False):
        glUseProgram(self.material.program_ref)
        glBindVertexArray(self.vao_ref)

        self.material.uniforms["modelMatrix"].data = self.get_world_matrix()
        self.material.uniforms["viewMatrix"].data = camera.view_matrix
        self.material.uniforms["projectionMatrix"].data = camera.projection_matrix

        if "light0" in self.material.uniforms.keys():
            for i in range(4):
                var_name = "light" + str(i)
                light_obj = lights[i]
                self.material.uniforms[var_name].data = light_obj
        
        if "viewPosition" in self.material.uniforms.keys():
            self.material.uniforms["viewPosition"].data = camera.get_world_position()

        for uniform_obj in self.material.uniforms.values():
            uniform_obj.upload_data()

        if not manual_settings:
            self.material.update_render_settings()

        glDrawArrays(
            self.material.settings['drawStyle'], 0, self.geometry.vertex_count)

        # reset
        glUseProgram(0)
        glBindVertexArray(0)
