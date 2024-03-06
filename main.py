from core.base import BaseApplication
from core.renderer import Renderer
from core.scene import Scene
from core.utils import OpenGLUtils
from core.light import DirectionalLight
from core.mesh import Mesh
from geometry import RectangleGeometry
from material.phong import PhongMaterial
from extras.impossible_cube import ImpossibleCube
from extras.view_bobbing_camera import ViewBobbingCamera
from imgui.integrations.pygame import PygameRenderer
from OpenGL.GL import *
from pygame.locals import *
import pygame
import numpy as np
import imgui


class Test(BaseApplication):
    def initialize(self):
        OpenGLUtils.print_system_info()

        imgui.create_context()
        self.gui_renderer = PygameRenderer()

        io = imgui.get_io()
        io.display_size = self.screen.get_size()

        self.show_gui = False
        self.last_mouse_pos = None

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = ViewBobbingCamera(
            self.clock, near=0.01, effect_multiplier=1.1, aspect_ratio=self.aspect_ratio, initial_position=[0, 1, 6])
        

        self.cube = ImpossibleCube(object_material=PhongMaterial)
        self.cube.translate(0, 2, 0)
        self.scene.add(self.cube)

        # self.scene.add(Mesh(SphereGeometry(radius=250), TextureMaterial(texture=Texture("skybox.png"))))
        self.scene.add(Mesh(RectangleGeometry(width=8, height=10), PhongMaterial(
            properties={"baseColor": [1, 0, 0]})).rotate_x(-np.pi/2).translate(-4, 0, 0))
        self.scene.add(Mesh(RectangleGeometry(width=8, height=10), PhongMaterial(
            properties={"baseColor": [0, 0, 1]})).rotate_x(-np.pi/2).translate(4, 0, 0))

        self.scene.add(DirectionalLight(direction=[1, 1, -1]))
        self.scene.add(DirectionalLight(direction=[-1, 1, 1]))
        self.scene.add(DirectionalLight(direction=[1, -1, 1]))
        self.scene.add(DirectionalLight(direction=[-1, -1, -1]))

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def process_events(self, events):
        super().process_events(events)
        if not self.show_gui:
            self.camera.process_input(self.input)
        if self.input.is_key_down(K_F1):
            self.show_gui = not self.show_gui
            pygame.mouse.set_visible(self.show_gui)
            if self.show_gui:
                # get mouse pos during camera mode
                before_pos = pygame.mouse.get_pos()
                if self.last_mouse_pos:
                    pygame.mouse.set_pos(self.last_mouse_pos)
                self.last_mouse_pos = before_pos
            else:
                self.last_mouse_pos = pygame.mouse.get_pos()
                pygame.mouse.set_pos(self.last_mouse_pos)
                # reset relative position
                pygame.mouse.get_rel()

        for event in events:
            self.gui_renderer.process_event(event)
        self.gui_renderer.process_inputs()

    def render_gui(self):
        imgui.new_frame()

        imgui.set_next_window_size(0, 0)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Debug Window", flags=imgui.WINDOW_NO_COLLAPSE |
                    imgui.WINDOW_NO_RESIZE)

        imgui.text("Camera Controls")
        _, self.camera.pitch = imgui.slider_float(
            "pitch", self.camera.pitch, -85, 85)
        _, self.camera.yaw = imgui.drag_float(
            "yaw", self.camera.yaw, 1, -360, 360)
        _, self.camera.translation_matrix[0, 3] = imgui.drag_float(
            "x", self.camera.translation_matrix[0, 3], 0.5, -np.inf, +np.inf)
        _, self.camera.translation_matrix[1, 3] = imgui.drag_float(
            "y", self.camera.translation_matrix[1, 3], 0.5, -np.inf, +np.inf)
        _, self.camera.translation_matrix[2, 3] = imgui.drag_float(
            "z", self.camera.translation_matrix[2, 3], 0.5, -np.inf, +np.inf)

        imgui.text(f"Camera Facing: {self.camera.get_direction()}")

        imgui.end()

        imgui.render()
        self.gui_renderer.render(imgui.get_draw_data())

    def update(self):
        self.cube.rotate_y(np.pi/300 * np.sin(self.time))
        self.cube.rotate_x(np.pi/400 * np.cos(self.time))
        self.cube.rotate_z(np.pi/350 * np.sin(self.time))

        self.renderer.render(self.scene, self.camera)
        if self.show_gui:
            self.render_gui()


def main():
    Test(screen_size=[1600, 900], fps=60).run()


if __name__ == "__main__":
    main()
