from core.camera import Camera
from core.matrix import Mat44
from math import sin, cos, pi, atan2
from pygame.locals import *
import pygame
import numpy as np
import quaternion

class FirstPersonCamera(Camera):
    def __init__(self, clock, fov=60, aspect_ratio=1, near=0.1, far=1000, initial_position=[0, 1, 0]) -> None:
        super().__init__(fov, aspect_ratio, near, far)
        self.clock = clock

        self.pitch = 0
        self.yaw = 0
        
        self.locked = False
        self.no_clip = False
        self.spacebar_timer = 0
        self.space_was_pressed = False

        self.camera_front = [0, 0, 0]
        self.camera_up = [0, 1, 0]
        self.camera_speed = 2.5

        self.set_position(initial_position)
        self.update_rotation_matrix()

    def process_input(self, input):
        if self.space_was_pressed:
            self.spacebar_timer += self.clock.get_time() / 1000

        if self.spacebar_timer > 0.4:
            self.spacebar_timer = 0
            self.space_was_pressed = False

        if self.locked:
            return

        boost = input.is_key_pressed(K_LSHIFT)

        if input.is_key_pressed(K_w):
            self.move("forward", boost)
        if input.is_key_pressed(K_a):
            self.move("left", boost)
        if input.is_key_pressed(K_s):
            self.move("backward", boost)
        if input.is_key_pressed(K_d):
            self.move("right", boost)

        if input.is_key_down(K_SPACE):
            if self.spacebar_timer > 0 and self.space_was_pressed:
                self.no_clip = not self.no_clip
                if self.no_clip:
                    self.translation_matrix.itemset((1, 3), 1.2)
                self.space_was_pressed = False
                self.spacebar_timer = 0
            else:
                self.space_was_pressed = True

        if input.is_mouse_moving:
            sensitivity = 0.05
            dx, dy = pygame.mouse.get_rel()
            self.yaw += dx * sensitivity
            self.pitch -= dy * sensitivity
            if self.pitch > 89:
                self.pitch = 89
            elif self.pitch < -89:
                self.pitch = -89
        
        if self.no_clip:
            delta_time = self.clock.get_time() / 1000
            y_pos = self.translation_matrix[1, 3]
            if input.is_key_pressed(K_SPACE):
                self.translation_matrix.itemset((1, 3), y_pos+self.camera_speed*delta_time*1.2)
            if input.is_key_pressed(K_LCTRL):
                self.translation_matrix.itemset((1, 3), y_pos-self.camera_speed*delta_time*1.2)

    def look_at(self, target):
        to_deg = 180 / pi
        dx, dy, dz = np.subtract(self.get_world_position(), target)
        pitch = -atan2(dy, np.sqrt(dx**2+dz**2)) * to_deg
        yaw = atan2(dz, dx)*to_deg - 90

        self.pitch = pitch
        self.yaw = yaw

    def move(self, dir, boost):
        delta_time = self.clock.get_time() / 1000
        current_pos = self.get_world_position()
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

        self.set_position(new_pos)

    def update_rotation_matrix(self):
        to_rad = pi / 180
        yaw = -self.yaw * to_rad
        pitch = self.pitch * to_rad

        # x-axis quaternion
        q1 = np.quaternion(cos(pitch/2), sin(pitch/2), 0, 0)

        # y-axis quaternion
        q2 = np.quaternion(cos(yaw/2), 0, sin(yaw/2), 0)

        rotation_matrix = quaternion.as_rotation_matrix(q2 * q1)
        self.camera_front = np.negative(self.rotation_matrix[:3, 2])

        self.set_rotation(rotation_matrix)

    def update_view_matrix(self):
        self.update_rotation_matrix()

        if not self.no_clip and self.translation_matrix[1, 3] > 1:
            delta_time = self.clock.get_time() / 1000
            y_pos = self.translation_matrix[1, 3]
            self.translation_matrix.itemset((1, 3), max(y_pos-self.camera_speed*3*delta_time, 1))
        elif not self.no_clip:  
            # keep camera on the ground
            self.translation_matrix.itemset((1, 3), 1)

        return super().update_view_matrix()