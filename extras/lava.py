from material.base import Material
from core.utils import load_shader

class LavaMaterial(Material):
    def __init__(self) -> None:
        vertex_shader_source = load_shader("lava/shader.vert")
        fragment_shader_source = load_shader("lava/shader.frag")

        super().__init__(vertex_shader_source, fragment_shader_source)

        # self.add_uniform("float", "time", 0.0)
        self.locate_uniforms()