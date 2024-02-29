from core.matrix import Mat44
from typing import TypeVar, List

TObject3D = TypeVar('TObject3D', bound="Object3D")

class Object3D:
    def __init__(self) -> None:
        self.transform = Mat44.make_identity()
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
        # if this is the root
        if self.parent is None:
            return self.transform

        # recursively query the world matrix
        return self.parent.get_world_matrix() @ self.transform

    def get_descendants(self) -> List[TObject3D]:
        descendants: List[TObject3D] = []
        nodes_to_traverse = [self]
        while len(nodes_to_traverse):
            node = nodes_to_traverse.pop(0)
            descendants.append(node)
            nodes_to_traverse = node.children + nodes_to_traverse

        return descendants
    
    def apply_matrix(self, matrix, is_local=True):
        if is_local:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform
    
    def translate(self, x, y, z, is_local=True):
        m = Mat44.make_translation(x, y, z)
        self.apply_matrix(m, is_local)
    
    def rotate_x(self, angle, is_local=True):
        m = Mat44.make_rotation_x(angle)
        self.apply_matrix(m, is_local)
    
    def rotate_y(self, angle, is_local=True):
        m = Mat44.make_rotation_y(angle)
        self.apply_matrix(m, is_local)
    
    def rotate_z(self, angle, is_local=True):
        m = Mat44.make_rotation_z(angle)
        self.apply_matrix(m, is_local)

    def scale(self, scale, is_local=True):
        m = Mat44.make_scale(scale)
        self.apply_matrix(m, is_local)

    """
    Get the last column of this matrix
    [1, 0, 0, Tx]
    [0, 1, 0, Ty]
    [0, 0, 1, Tz]
    [0, 0, 0,  1]
    """
    def get_position(self):
        return [
            self.transform.item((0, 3)),
            self.transform.item((1, 3)),
            self.transform.item((2, 3)),
        ]
    
    def get_world_position(self):
        world_transform = self.get_world_matrix()
        return [
            world_transform.item((0, 3)),
            world_transform.item((1, 3)),
            world_transform.item((2, 3)),
        ]
    
    def set_position(self, position):
        self.transform.itemset((0, 3), position[0])
        self.transform.itemset((1, 3), position[1])
        self.transform.itemset((2, 3), position[2])