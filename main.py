from core.base import BaseApplication
from core.renderer import Renderer
from core.scene import Scene
from core.mesh import Mesh
from core.utils import OpenGLUtils, ASSETS_PATH
from core.texture import Texture
from geometry import SphereGeometry, BoxGeometry
from material.texture import TextureMaterial
from material.surface import SurfaceMaterial
from extras.axes_helper import AxesHelper
from extras.grid_helper import GridHelper
from extras.view_bobbing_camera import ViewBobbingCamera
from pygame.locals import *
from math import pi, sin, cos
import pygame
import quaternion
import numpy as np
import imgui
from imgui.integrations.pygame import PygameRenderer

class Test(BaseApplication):
    def initialize(self):
        OpenGLUtils.print_system_info()

        imgui.create_context()
        self.gui_renderer = PygameRenderer()

        io = imgui.get_io()
        io.display_size = self.screen.get_size()

        self.show_gui = False
        sw, sh = self.screen.get_size()
        self.gui_size = (sw//4, sh//2)
        self.last_mouse_pos = None

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = ViewBobbingCamera(
            self.clock, effect_multiplier=1, aspect_ratio=self.aspect_ratio, initial_position=[-2, 1, 4])

        planet_texture = Texture(ASSETS_PATH + "textures/earth.jpg")
        self.planet = Mesh(geometry=SphereGeometry(),
                           material=TextureMaterial(planet_texture))
        self.planet.translate(8, 2, 0)
        self.scene.add(self.planet)

        sky_box_texture = Texture(ASSETS_PATH + "textures/skybox.png")
        self.sky_box = Mesh(geometry=SphereGeometry(
            radius=100), material=TextureMaterial(sky_box_texture))
        self.scene.add(self.sky_box)

        self.box = Mesh(geometry=BoxGeometry(),
                        material=SurfaceMaterial())
        self.scene.add(self.box)
        self.box.translate(0, 1, 0)

        self.planet.add(AxesHelper(axis_length=2.5))
        self.box.add(AxesHelper(axis_length=2.5))

        grid = GridHelper()
        grid.rotate_x(-pi/2)
        self.scene.add(grid)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.color = [0, 0, 0]

    def process_events(self, events):
        super().process_events(events)
        if not self.show_gui:
            self.camera.process_input(self.input)
        if self.input.is_key_down(K_F1):
            self.show_gui = not self.show_gui
            pygame.mouse.set_visible(self.show_gui)
            pygame.event.set_grab(not self.show_gui)
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

        imgui.show_test_window()

        imgui.set_next_window_size(0, 0)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Debug Window", flags=imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

        imgui.text("Camera Controls")
        _ , self.camera.pitch = imgui.slider_float("pitch", self.camera.pitch, -89, 89)
        _ , self.camera.yaw = imgui.drag_float("yaw", self.camera.yaw, 1, -360, 360)
        imgui.text("")

        imgui.text("Box Controls")
        _ , color = imgui.color_edit3("color", *self.box.material.uniforms["baseColor"].data)
        self.box.material.uniforms["baseColor"].data = color

        imgui.end()

        imgui.render()
        self.gui_renderer.render(imgui.get_draw_data())

    def update(self):
        self.planet.rotate_y(pi/100)
        q_orbit = np.quaternion(cos(-pi/600), 0, sin(-pi/600), 0)
        position = self.planet.get_world_position()
        new_position = position @ quaternion.as_rotation_matrix(q_orbit)

        self.box.look_at(self.planet.get_world_position())

        self.planet.set_position(new_position)
        self.renderer.render(self.scene, self.camera)

        if self.show_gui:
            self.render_gui()

def main():
    Test(screen_size=[1600, 900], fps=60).run()


if __name__ == "__main__":
    main()
