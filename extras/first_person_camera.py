from core.camera import Camera
from core.matrix import Mat44
from math import sin, cos, pi
from pygame.locals import *
import pygame
import numpy as np

class FirstPersonCamera(Camera):
    def __init__(self, clock, fov=60, aspect_ratio=1, near=0.1, far=1000, initial_position=[0, 0, 0]) -> None:
        super().__init__(fov, aspect_ratio, near, far)
        self.clock = clock

        self.camera_front = [0, 0, -1]
        self.camera_up = [0, 1, 0]
        self.camera_speed = 2.5

        self.pitch = 0
        self.yaw = -90

        self.head_bob_active = False

        self.set_position(initial_position)
    
    def process_input(self, input):
        boost = input.is_key_pressed(K_LSHIFT)

        if input.is_key_pressed(K_w):
            self.move("forward", boost)
        if input.is_key_pressed(K_a):
            self.move("left", boost)
        if input.is_key_pressed(K_s):
            self.move("backward", boost)
        if input.is_key_pressed(K_d):
            self.move("right", boost)

        if input.is_mouse_moving:
            sensitivity = 0.05
            dx, dy = pygame.mouse.get_rel()
            self.yaw += dx * sensitivity
            self.pitch -= dy * sensitivity
            if self.pitch > 89:
                self.pitch = 89
            elif self.pitch < -89:
                self.pitch = -89

    def move(self, dir, boost):
        delta_time = self.clock.get_time() / 1000
        current_pos = self.get_position()
        new_pos = current_pos
        speed = self.camera_speed * delta_time
        if boost:
            speed *= 2
        if dir == "forward":
            new_pos = np.add(current_pos, np.multiply(speed, self.camera_front))
        elif dir == "backward":
            new_pos = np.subtract(current_pos, np.multiply(speed, self.camera_front))
        elif dir == "left":
            vec = np.cross(self.camera_front, self.camera_up).astype(float)
            vec /= np.linalg.norm(vec)
            new_pos = np.subtract(current_pos, np.multiply(vec, speed))
        elif dir == "right":
            vec = np.cross(self.camera_front, self.camera_up).astype(float)
            vec /= np.linalg.norm(vec)
            new_pos = np.add(current_pos, np.multiply(vec, speed))

        self.head_bob_active = True

        self.set_position(new_pos)

    def update_view_matrix(self):
        to_rad = pi / 180
        yaw = self.yaw * to_rad
        pitch = self.pitch * to_rad
        camera_pos = self.get_position()

        # keep camera on the ground
        camera_pos[1] = 1

        self.camera_front = [
            cos(yaw) * cos(pitch),
            sin(pitch),
            sin(yaw) * cos(pitch)
        ]

        if self.head_bob_active:
            self.head_bob_active = False

        self.look_at(camera_pos, np.add(camera_pos, self.camera_front), self.camera_up)
        return super().update_view_matrix()

    def look_at(self, position, target, world_up):
        look_matrix = Mat44.make_look_at(position, target, world_up)
        position = look_matrix[:3, 3]
        rotation = look_matrix[:3, :3]
        self.set_position(position)
        self.set_rotation(rotation)