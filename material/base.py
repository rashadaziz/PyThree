from core.utils import OpenGLUtils
from core.uniform import Uniform
from OpenGL.GL import *
from typing import Dict

class Material:
    def __init__(self, vertex_shader_source, fragment_shader_source) -> None:
        self.program_ref = OpenGLUtils.init_program(vertex_shader_source, fragment_shader_source)

        self.uniforms: Dict[str, Uniform] = {}
        self.uniforms["modelMatrix"] = Uniform("mat4", None)
        self.uniforms["viewMatrix"] = Uniform("mat4", None)
        self.uniforms["projectionMatrix"] = Uniform("mat4", None)

        self.settings = {}
        self.settings["drawStyle"] = GL_TRIANGLES

    def add_uniform(self, data_type, var_name, data):
        self.uniforms[var_name] = Uniform(data_type, data)

    def locate_uniforms(self):
        for var_name, uniform_obj in self.uniforms.items():
            uniform_obj.locate_variable(self.program_ref, var_name)

    def update_render_settings(self):
        pass

    def set_properties(self, properties):
        for var_name, data in properties.items():
            if var_name in self.uniforms.keys():
                self.uniforms[var_name].data = data
            elif name in self.settings.keys():
                self.settings[var_name] = data
            else:
                raise Exception(f"Material has no variable/setting named '{var_name}'")
