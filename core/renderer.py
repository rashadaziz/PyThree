from OpenGL.GL import *
from core.mesh import Mesh
from core.scene import Scene
from core.camera import Camera

class Renderer:
    def __init__(self, clear_color=[0, 0, 0]) -> None:
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(*clear_color, 1)

    def render(self, scene: Scene, camera: Camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.update_view_matrix()

        descendant_list = scene.get_descendants()
        mesh_list: list[Mesh] = list(filter(lambda obj: isinstance(obj, Mesh), descendant_list))

        for mesh in mesh_list:
            if not mesh.visible:
                continue

            glUseProgram(mesh.material.program_ref)

            glBindVertexArray(mesh.vao_ref)

            mesh.material.uniforms["modelMatrix"].data = mesh.get_world_matrix()
            mesh.material.uniforms["viewMatrix"].data = camera.view_matrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projection_matrix

            for _, uniform_obj in mesh.material.uniforms.items():
                uniform_obj.upload_data()

            mesh.material.update_render_settings()
            
            glDrawArrays(mesh.material.settings['drawStyle'], 0, mesh.geometry.vertex_count)