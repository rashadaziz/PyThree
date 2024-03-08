from core.camera import Camera
from core.light import Light
from core.mesh import Mesh
from core.renderer import Renderer
from core.mesh import Mesh
from geometry import RectangleGeometry
from material.surface import SurfaceMaterial
from extras.portal import Portal
from typing import List
from OpenGL.GL import *


class PortalRenderer(Renderer):
    def __init__(self, clear_color=[0, 0, 0], max_recursion_level=0) -> None:
        super().__init__(clear_color)
        self.max_recursion_level = max_recursion_level

    def render_others(self, others: List[Mesh], camera: Camera, lights: List[Light]):
        for other in others:
            if not other.visible:
                continue
            other.render(camera, lights, manual_settings=True)

    def render_portals(self, portals: List[Portal], others: List[Mesh], player_cam: Camera, lights: List[Light], recursion_level=0):
        glEnable(GL_CULL_FACE)

        for portal in portals:
            if portal.destination is None:
                continue

            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
            glDepthMask(GL_FALSE)
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_STENCIL_TEST)
            glStencilFunc(GL_NOTEQUAL, recursion_level, 0xFF)
            glStencilOp(GL_INCR, GL_KEEP, GL_KEEP)
            glStencilMask(0xFF)

            portal.render(player_cam, lights, manual_settings=True)

            if recursion_level == self.max_recursion_level:
                glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
                glDepthMask(GL_TRUE)
                glClear(GL_DEPTH_BUFFER_BIT)
                glEnable(GL_DEPTH_TEST)
                glEnable(GL_STENCIL_TEST)
                glStencilMask(0)
                glStencilFunc(GL_EQUAL, recursion_level + 1, 0xFF)

                portal_cam = Camera(
                    aspect_ratio=self.screen_size[0]/self.screen_size[1])
                portal.set_destination_view(player_cam, portal_cam)
                # others.append(Mesh(RectangleGeometry(width=1.5, height=2.5), SurfaceMaterial(properties={"baseColor": [0.5, 0.5, 0.5]}
                # )).translate(*portal.get_world_position()).set_rotation(portal.get_world_rotation()[:3, :3]))
                self.render_others(others, portal_cam, lights)
            else:
                portal_cam = Camera(
                    aspect_ratio=self.screen_size[0]/self.screen_size[1])
                portal.set_destination_view(player_cam, portal_cam)
                self.render_portals(portals, others, portal_cam,
                                    lights, recursion_level + 1)

            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
            glDepthMask(GL_FALSE)
            glEnable(GL_STENCIL_TEST)
            glStencilMask(0)
            glStencilFunc(GL_NOTEQUAL, recursion_level + 1, 0xFF)
            glStencilOp(GL_DECR, GL_KEEP, GL_KEEP)

            portal.render(player_cam, lights, manual_settings=True)

        glDisable(GL_STENCIL_TEST)
        glStencilMask(0)
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        glClear(GL_DEPTH_BUFFER_BIT)

        for portal in portals:
            portal.render(player_cam, lights, manual_settings=True)

        glDepthFunc(GL_LESS)
        glEnable(GL_STENCIL_TEST)
        glStencilMask(0)
        glStencilFunc(GL_LEQUAL, recursion_level, 0xFF)
        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        glDepthMask(GL_TRUE)
        glEnable(GL_DEPTH_TEST)

        self.render_others(others, player_cam, lights)

    def render_impl(self, camera: Camera, meshes: List[Mesh], lights: List[Light]):
        def portal_filter(obj): return isinstance(obj, Portal)
        def others_filter(obj): return not isinstance(obj, Portal)
        portals = list(filter(portal_filter, meshes))
        others = list(filter(others_filter, meshes))
        self.render_portals(portals, others, camera, lights)
