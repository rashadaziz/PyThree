from core.camera import Camera
from math import sin, cos, pi, atan2
from pygame.locals import *
import pygame
import numpy as np
import quaternion

class FirstPersonCamera(Camera):
    def __init__(self, clock, fov=60, aspect_ratio=1, near=0.1, far=1000, initial_position=[0, 1, 0]) -> None:
        super().__init__(fov, aspect_ratio, near, far)
        self.clock = clock

        self.locked = False
        self.no_clip = initial_position[1] > 1
        self.spacebar_timer = 0
        self.space_was_pressed = False
        self.is_moving = False
        self.boost = False

        self.move_direction = np.array([0, 0, 0]).astype(float)

        self.camera_front = np.array([0, 0, 0]).astype(float)
        self.camera_up = [0, 1, 0]
        self.camera_speed = 5

        self.set_position(initial_position)
        self.update_rotation_matrix()

    def process_input(self, input):
        if self.locked:
            return
        
        if self.space_was_pressed:
            self.spacebar_timer += self.clock.get_time() / 1000

        if self.spacebar_timer > 0.4:
            self.spacebar_timer = 0
            self.space_was_pressed = False

        self.boost = input.is_key_pressed(K_LSHIFT)

        if input.is_key_pressed(K_w):
            self.move("forward")
        if input.is_key_pressed(K_a):
            self.move("left")
        if input.is_key_pressed(K_s):
            self.move("backward")
        if input.is_key_pressed(K_d):
            self.move("right")

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
            self.handle_mouse_look(*pygame.mouse.get_rel())
        
        if self.no_clip:
            delta_time = self.clock.get_time() / 1000
            y_pos = self.translation_matrix[1, 3]
            if input.is_key_pressed(K_SPACE):
                self.translation_matrix.itemset((1, 3), y_pos+self.camera_speed*delta_time*1.2)
            if input.is_key_pressed(K_LCTRL):
                self.translation_matrix.itemset((1, 3), y_pos-self.camera_speed*delta_time*1.2)

    def handle_mouse_look(self, dx, dy):
        sensitivity = 0.8e-3
        yaw_angle = -dx*sensitivity
        pitch_angle = -dy*sensitivity

        q_yaw = np.quaternion(cos(yaw_angle/2), 0, sin(yaw_angle/2), 0)
        q_pitch = np.quaternion(cos(pitch_angle/2), sin(pitch_angle/2), 0, 0)
        self.rotation_matrix[:3, :3] = quaternion.as_rotation_matrix(q_yaw) @ self.rotation_matrix[:3, :3]
        self.rotation_matrix[:3, :3] = self.rotation_matrix[:3, :3] @ quaternion.as_rotation_matrix(q_pitch)

    def move(self, dir):
        self.is_moving = True

        camera_dir = self.camera_front

        if not self.no_clip:
            # kill y component of movement direction
            camera_dir = [self.camera_front[0], 0, self.camera_front[2]]
            camera_dir /= np.linalg.norm(camera_dir)

        if dir == "forward":
            self.move_direction += camera_dir
        elif dir == "backward":
            self.move_direction -= camera_dir
        elif dir == "left":
            vec = np.cross(camera_dir, self.camera_up).astype(float)
            vec /= np.linalg.norm(vec)
            self.move_direction -= vec
        elif dir == "right":
            vec = np.cross(camera_dir, self.camera_up).astype(float)
            vec /= np.linalg.norm(vec)
            self.move_direction += vec

    def update_rotation_matrix(self):
        self.camera_front = np.negative(self.rotation_matrix[:3, 2]).astype(float)

    def update_view_matrix(self):
        if not self.no_clip and self.translation_matrix[1, 3] > 1:
            delta_time = self.clock.get_time() / 1000
            y_pos = self.translation_matrix[1, 3]
            self.translation_matrix.itemset((1, 3), max(y_pos-self.camera_speed*3*delta_time, 1))
        elif not self.no_clip:  
            # keep camera on the ground
            self.translation_matrix.itemset((1, 3), 1)

        delta_time = self.clock.get_time() / 1000
        speed = self.camera_speed * delta_time
        if self.boost:
            speed *= 2
        
        if np.linalg.norm(self.move_direction) > 0:
            dir = self.move_direction / np.linalg.norm(self.move_direction)
            self.translate(*np.multiply(speed, dir))

        return super().update_view_matrix()
    
    def update(self):
        self.update_rotation_matrix()
        self.update_view_matrix()
        self.is_moving = False
        self.move_direction = np.array([0, 0, 0]).astype(float)