from core.base import BaseApplication
from core.renderer import Renderer
from core.scene import Scene
from core.mesh import Mesh
from core.utils import OpenGLUtils
from geometry import ObjectGeometry
from material.surface import SurfaceMaterial
from extras.axes_helper import AxesHelper
from extras.grid_helper import GridHelper
from extras.view_bobbing_camera import ViewBobbingCamera
from pygame.locals import *
from math import pi, sin, cos
import pygame
import quaternion
import numpy as np

class Test(BaseApplication):
    def initialize(self):
        OpenGLUtils.print_system_info()

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = ViewBobbingCamera(self.clock, effect_multiplier=1.25, aspect_ratio=self.aspect_ratio, initial_position=[-2, 1, 4])

        self.mesh = Mesh(geometry=ObjectGeometry("crocodile.obj", scale=0.01),
                         material=SurfaceMaterial({"useVertexColors": True}))
        self.mesh.translate(0, .1, 0)
        self.mesh.rotate_x(-pi/2)
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
        self.renderer.render(self.scene, self.camera)


def main():
    Test(screen_size=[1600, 900], fps=60).run()


if __name__ == "__main__":
    main()
