import numpy as np
from math import sin, cos, tan, pi


class Mat44:
    @staticmethod
    def make_identity():
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def make_translation(x, y, z):
        return np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def make_rotation_x(angle):
        c = cos(angle)
        s = sin(angle)
        return np.array([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1]
        ]).astype(float)
    
    @staticmethod
    def make_rotation_y(angle):
        c = cos(angle)
        s = sin(angle)
        return np.array([
            [ c, 0, s, 0],
            [ 0, 1, 0, 0],
            [-s, 0, c, 0],
            [ 0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def make_rotation_z(angle):
        c = cos(angle)
        s = sin(angle)
        return np.array([
            [c, -s,  0, 0],
            [s,  c,  0, 0],
            [0,  0,  1, 0],
            [0,  0,  0, 1]
        ]).astype(float)
    
    @staticmethod
    def make_scale(s):
        return np.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def make_perspective(fov=60, aspect_ratio=1, near=0.1, far=1000):
        a = fov * pi/180
        d = 1 / tan(a/2)
        r = aspect_ratio
        b = (far + near) / (near - far)
        c = 2*far*near / (near - far)
        return np.array([
            [d/r, 0,  0, 0],
            [0,   d,  0, 0],
            [0,   0,  b, c],
            [0,   0, -1, 0]
        ]).astype(float)
    
    @staticmethod
    def make_look_at(position, target, world_up=[0, 1, 0]):
        forward = np.subtract(target, position)
        right = np.cross(forward, world_up)
        
        # if forward and world_up are parallel
        if np.linalg.norm(right) < 1e-6:
            offset = np.array([0, 0, -1e-3])
            right = np.cross(forward, world_up + offset)

        up = np.cross(right, forward)
        forward = np.divide(forward, np.linalg.norm(forward))
        right = np.divide(right, np.linalg.norm(right))
        up = np.divide(up, np.linalg.norm(up))
        return np.array(
            [[right[0], up[0], -forward[0], position[0]],
             [right[1], up[1], -forward[1], position[1]],
             [right[2], up[2], -forward[2], position[2]],
             [0, 0, 0, 1]]
        ).astype(float)