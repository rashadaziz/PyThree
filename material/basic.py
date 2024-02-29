from material.base import Material
from core.utils import load_shader

class BasicMaterial(Material):
    def __init__(self) -> None:
        vertex_shader_source = load_shader('basic-material/shader.vert')
        fragment_shader_source = load_shader('basic-material/shader.frag')

        super().__init__(vertex_shader_source, fragment_shader_source)

        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform("bool", "useVertexColors", False)
        self.locate_uniforms()