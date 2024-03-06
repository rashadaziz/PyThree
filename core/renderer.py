from OpenGL.GL import *
from core.mesh import Mesh
from core.scene import Scene
from core.camera import Camera
from core.light import Light
import pygame


class Renderer:
    def __init__(self, clear_color=[0, 0, 0]) -> None:
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_BLEND)
        glEnable(GL_STENCIL_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*clear_color, 1)

        self.screen_size = pygame.display.get_surface().get_size()

    def render(self, scene: Scene, camera: Camera, clear_color_buffer=True, clear_depth_buffer=True, render_target=None):
        if render_target is None:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glViewport(0, 0, *self.screen_size)
        else:
            glBindFramebuffer(GL_FRAMEBUFFER, render_target.frame_buffer_ref)
            glViewport(0, 0, render_target.width, render_target.height)

        if clear_color_buffer:
            glClear(GL_COLOR_BUFFER_BIT)
        if clear_depth_buffer:
            glClear(GL_DEPTH_BUFFER_BIT)

        glClear(GL_STENCIL_BUFFER_BIT)

        camera.update()

        descendant_list = scene.get_descendants()
        camera_descendant_list = camera.get_descendants()
        descendant_list.extend(camera_descendant_list)
        mesh_list: list[Mesh] = list(filter(lambda obj: isinstance(
            obj, Mesh), descendant_list))
        light_list: list[Light] = list(filter(lambda obj: isinstance(obj, Light), descendant_list))
        while len(light_list) < 4:
            light_list.append(Light())

        for mesh in mesh_list:
            if not mesh.visible:
                continue
            
            glUseProgram(mesh.material.program_ref)
            glBindVertexArray(mesh.vao_ref)

            mesh.material.uniforms["modelMatrix"].data = mesh.get_world_matrix()
            mesh.material.uniforms["viewMatrix"].data = camera.view_matrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projection_matrix

            if "light0" in mesh.material.uniforms.keys():
                for i in range(4):
                    var_name = "light" + str(i)
                    light_obj = light_list[i]
                    mesh.material.uniforms[var_name].data = light_obj
            
            if "viewPosition" in mesh.material.uniforms.keys():
                mesh.material.uniforms["viewPosition"].data = camera.get_world_position()

            for uniform_obj in mesh.material.uniforms.values():
                uniform_obj.upload_data()

            mesh.material.update_render_settings()

            glDrawArrays(
                mesh.material.settings['drawStyle'], 0, mesh.geometry.vertex_count)

            # reset
            glUseProgram(0)
            glBindVertexArray(0)
            glStencilMask(0xFF)
            glStencilFunc(GL_ALWAYS, 0, 0xFF)
            glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
