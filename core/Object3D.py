import quaternion
from core.matrix import Mat44
from typing import TypeVar, List
import numpy as np
from math import sin, cos, atan2, pi

TObject3D = TypeVar('TObject3D', bound="Object3D")


class Object3D:
    def __init__(self) -> None:
        self.translation_matrix = Mat44.make_identity()
        self.rotation_matrix = Mat44.make_identity()
        self.scale_matrix = Mat44.make_identity()

        self.parent: TObject3D | None = None
        self.children: List[TObject3D] = []

    def add(self, child: TObject3D):
        self.children.append(child)
        child.parent = self

    def remove(self, child: TObject3D):
        self.children.remove(child)
        child.parent = None

    def get_world_matrix(self):
        model_matrix = self.translation_matrix @ self.rotation_matrix @ self.scale_matrix

        # if this is the root
        if self.parent is None:
            return model_matrix

        # recursively query the world matrix
        return self.parent.get_world_matrix() @ model_matrix
    
    def get_model_matrix(self):
        return self.translation_matrix @ self.rotation_matrix @ self.scale_matrix
    
    def get_world_translation(self):
        if self.parent is None:
            return self.translation_matrix
        
        return self.parent.get_world_translation() @ self.translation_matrix
    
    def get_world_rotation(self):
        if self.parent is None:
            return self.rotation_matrix
        
        return self.parent.get_world_rotation() @ self.rotation_matrix

    def get_world_scale(self):
        if self.parent is None:
            return self.scale_matrix
        
        return self.parent.get_world_scale() @ self.scale_matrix

    def get_descendants(self) -> List[TObject3D]:
        descendants: List[TObject3D] = []
        nodes_to_traverse = [self]
        while len(nodes_to_traverse):
            node = nodes_to_traverse.pop(0)
            descendants.append(node)
            nodes_to_traverse = node.children + nodes_to_traverse

        return descendants

    def apply_translation(self, matrix, is_local=True):
        if is_local:
            self.translation_matrix = self.translation_matrix @ matrix
        else:
            self.translation_matrix = matrix @ self.translation_matrix

        return self

    def apply_rotation(self, q):
        self.rotation_matrix[:3, :3] = quaternion.as_rotation_matrix(
            q) @ self.rotation_matrix[:3, :3]

        return self

    def apply_scale(self, matrix, is_local=True):
        if is_local:
            self.scale_matrix = self.scale_matrix @ matrix
        else:
            self.scale_matrix = matrix @ self.scale_matrix

        return self

    def translate(self, x, y, z, is_local=True):
        m = Mat44.make_translation(x, y, z)
        return self.apply_translation(m, is_local)

    def rotate_around_axis(self, angle, axis):
        q = np.quaternion(cos(angle/2), *np.multiply(axis,
                          [sin(angle/2), sin(angle/2), sin(angle/2)]))
        return self.apply_rotation(q)

    def rotate_x(self, angle):
        return self.rotate_around_axis(angle, [1, 0, 0])

    def rotate_y(self, angle):
        return self.rotate_around_axis(angle, [0, 1, 0])

    def rotate_z(self, angle):
        return self.rotate_around_axis(angle, [0, 0, 1])

    def scale(self, scale, is_local=True):
        m = Mat44.make_scale(scale)
        return self.apply_scale(m, is_local)

    """
    Get the last column of this matrix
    [1, 0, 0, Tx]
    [0, 1, 0, Ty]
    [0, 0, 1, Tz]
    [0, 0, 0,  1]
    """

    def get_position(self):
        return self.translation_matrix[:3, 3]

    def get_world_position(self):
        world_transform = self.get_world_matrix()
        return world_transform[:3, 3]
    
    def get_world_position_vec4(self):
        world_transform = self.get_world_matrix()
        return world_transform[:, 3]

    def get_rotation_matrix(self):
        return self.rotation_matrix[:3, :3].copy()
    
    def get_direction(self):
        forward = np.array([0, 0, -1])
        return self.get_world_rotation()[:3, :3] @ forward

    def set_position(self, position):
        self.translation_matrix.itemset((0, 3), position[0])
        self.translation_matrix.itemset((1, 3), position[1])
        self.translation_matrix.itemset((2, 3), position[2])

        return self

    def set_rotation(self, rotation):
        self.rotation_matrix[:3, :3] = rotation
        
        return self

    def set_scale(self, scale):
        self.scale_matrix[0, 0] = scale
        self.scale_matrix[1, 1] = scale
        self.scale_matrix[2, 2] = scale

        return self

    def set_direction(self, direction):
        target = np.add(self.get_position(), direction)
        self.look_at(target)

        return self

    def look_at(self, target):
        dx, dy, dz = np.subtract(target, self.get_world_position())
        pitch = atan2(dy, np.sqrt(dx**2+dz**2))
        yaw = atan2(dz, dx) + pi/2
        yaw = -yaw

        # x-axis quaternion
        q1 = np.quaternion(cos(pitch/2), sin(pitch/2), 0, 0)

        # y-axis quaternion
        q2 = np.quaternion(cos(yaw/2), 0, sin(yaw/2), 0)

        self.set_rotation(quaternion.as_rotation_matrix(q2 * q1))

        return self
        