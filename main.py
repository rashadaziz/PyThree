from core.base import BaseApplication
from core.renderer import Renderer
from core.scene import Scene
from core.mesh import Mesh
from core.utils import OpenGLUtils
from geometry import SphereGeometry
from material.surface import SurfaceMaterial
from extras.axes_helper import AxesHelper
from extras.grid_helper import GridHelper
from extras.first_person_camera import FirstPersonCamera
from pygame.locals import *
from math import sin, cos, pi
import pygame

class Test(BaseApplication):
    def initialize(self):
        OpenGLUtils.print_system_info()

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = FirstPersonCamera(clock=self.clock, aspect_ratio=self.aspect_ratio, initial_position=[0, 1, 0])

        self.mesh = Mesh(geometry=SphereGeometry(n_radius_segments=20, n_height_segments=10),
                         material=SurfaceMaterial({"useVertexColors": True}))
        self.scene.add(self.mesh)

        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)
        grid = GridHelper(size=20, grid_color=[1, 1, 1],
                          center_color=[1, 1, 0])

        grid.rotate_x(-pi/2)
        self.scene.add(grid)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def update(self):
        self.camera.process_input(self.input)

        self.mesh.rotate_x(0.32*self.delta_time)
        self.mesh.rotate_y(0.178*self.delta_time)
        self.mesh.set_position([sin(0.75*self.time), cos(0.75*self.time), 0])

        self.renderer.render(self.scene, self.camera)


def main():
    Test(screen_size=[1280, 720], fps=60).run()


if __name__ == "__main__":
    main()
