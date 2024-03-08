from OpenGL.GL import *
from core.mesh import Mesh
from core.scene import Scene
from core.camera import Camera
from core.light import Light
from typing import List
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

    def render_impl(self, camera: Camera, meshes: List[Mesh], lights: List[Light]):
        for mesh in meshes:
            if not mesh.visible:
                continue
            mesh.render(camera=camera, lights=lights)

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

        glStencilMask(0xFF)
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

        self.render_impl(camera, mesh_list, light_list)
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
