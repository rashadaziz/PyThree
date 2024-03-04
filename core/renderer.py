from OpenGL.GL import *
from core.mesh import Mesh
from core.scene import Scene
from core.camera import Camera

class Renderer:
    def __init__(self, clear_color=[0, 0, 0]) -> None:
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*clear_color, 1)

    def render(self, scene: Scene, camera: Camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.update()

        descendant_list = scene.get_descendants()
        camera_descendant_list = camera.get_descendants()
        mesh_list: list[Mesh] = list(filter(lambda obj: isinstance(obj, Mesh), descendant_list + camera_descendant_list))

        for mesh in mesh_list:
            if not mesh.visible:
                continue

            glUseProgram(mesh.material.program_ref)
            glBindVertexArray(mesh.vao_ref)

            mesh.material.uniforms["modelMatrix"].data = mesh.get_world_matrix()
            mesh.material.uniforms["viewMatrix"].data = camera.view_matrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projection_matrix

            for uniform_obj in mesh.material.uniforms.values():
                uniform_obj.upload_data()

            mesh.material.update_render_settings()
            
            glDrawArrays(mesh.material.settings['drawStyle'], 0, mesh.geometry.vertex_count)

            # reset
            glUseProgram(0)
            glBindVertexArray(0)