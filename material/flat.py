from material.base import Material
from core.utils import load_shader
from OpenGL.GL import *

class FlatMaterial(Material):
    def __init__(self, texture=None, properties={}) -> None:
        vertex_shader_source = load_shader("flat-shading/shader.vert")
        fragment_shader_source = load_shader("flat-shading/shader.frag")

        super().__init__(vertex_shader_source, fragment_shader_source)

        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0]) 
        self.add_uniform("Light", "light0", None) 
        self.add_uniform("Light", "light1", None) 
        self.add_uniform("Light", "light2", None) 
        self.add_uniform("Light", "light3", None) 
        self.add_uniform("bool", "useTexture", 0) 
        if texture == None:
            self.add_uniform("bool", "useTexture", False) 
        else:
            self.add_uniform("bool", "useTexture", True)
            self.add_uniform("sampler2D", "texture", [texture.texture_ref, 1])

        self.locate_uniforms()

        self.settings["doubleSide"] = True
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1

        self.set_properties(properties)

    def update_render_settings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["lineWidth"])

        return super().update_render_settings()