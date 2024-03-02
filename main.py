from core.base import BaseApplication
from core.renderer import Renderer
from core.scene import Scene
from core.mesh import Mesh
from core.utils import OpenGLUtils
from geometry import BoxGeometry
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
        self.camera = ViewBobbingCamera(clock=self.clock, aspect_ratio=self.aspect_ratio, initial_position=[0, 1, 4])

        self.mesh = Mesh(geometry=BoxGeometry(),
                         material=SurfaceMaterial({"useVertexColors": True}))
        self.mesh.set_position([0, 2, 0])
        self.scene.add(self.mesh)

        self.camera.locked = True
        self.camera.look_at(self.mesh.get_world_position())

        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)
        grid = GridHelper(size=20, grid_color=[1, 1, 1],
                          center_color=[1, 1, 0])

        grid.rotate_x(-pi/2)
        self.scene.add(grid)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.rot_x = 0
        self.rot_y = 0

    def update(self):
        self.camera.process_input(self.input)
        rotation_speed = 0.01

        dx, dy = pygame.mouse.get_rel()
        
        rot_x = rotation_speed * dx
        rot_y = rotation_speed * dy

        mesh_pos = self.mesh.get_world_position()
        camera_pos = self.camera.get_world_position()

        right = np.cross(self.camera.camera_up, np.subtract(mesh_pos, camera_pos))
        up = np.cross(np.subtract(mesh_pos, camera_pos), right)
        right = np.divide(right, np.linalg.norm(right))
        up = np.divide(up, np.linalg.norm(up))
        
        qx = np.quaternion(cos(rot_x/2), *np.multiply(up, [rot_x/2, rot_x/2, rot_x/2]))
        qy = np.quaternion(cos(-rot_y/2), *np.multiply(right, [-rot_y/2, -rot_y/2, -rot_y/2]))

        self.mesh.rotation_matrix[:3, :3] = quaternion.as_rotation_matrix(qy * qx) @ self.mesh.rotation_matrix[:3, :3]

        self.renderer.render(self.scene, self.camera)


def main():
    Test(screen_size=[1280, 720], fps=60).run()


if __name__ == "__main__":
    main()
