from core.base import BaseApplication
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.utils import OpenGLUtils
from geometry import BoxGeometry
from material.surface import SurfaceMaterial
from pygame.locals import *

class Test(BaseApplication):
    def initialize(self):
        OpenGLUtils.print_system_info()

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 4])

        self.mesh = Mesh(geometry=BoxGeometry(), material=SurfaceMaterial({ "useVertexColors": True }))
        self.scene.add(self.mesh)

    def update(self):
        # prone to gimbal locking
        if self.input.is_key_pressed(K_q):
            self.mesh.rotate_y(-0.4*self.delta_time)
        if self.input.is_key_pressed(K_e):
            self.mesh.rotate_y(0.4*self.delta_time)
        if self.input.is_key_pressed(K_w):
            self.mesh.rotate_x(-0.4*self.delta_time)
        if self.input.is_key_pressed(K_s):
            self.mesh.rotate_x(0.4*self.delta_time)
        if self.input.is_key_pressed(K_d):
            self.mesh.rotate_z(-0.4*self.delta_time)
        if self.input.is_key_pressed(K_a):
            self.mesh.rotate_z(0.4*self.delta_time)

        self.renderer.render(self.scene, self.camera)


def main():
    Test(screen_size=[800, 600], fps=120).run()


if __name__ == "__main__":
    main()
