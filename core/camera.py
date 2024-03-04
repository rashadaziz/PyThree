from core.Object3D import Object3D
from core.matrix import Mat44
from core.input import Input
from numpy.linalg import inv


class Camera(Object3D):
    def __init__(self, fov=60, aspect_ratio=1, near=0.1, far=1000) -> None:
        super().__init__()

        self.view_matrix = Mat44.make_identity()
        self.projection_matrix = Mat44.make_perspective(
            fov, aspect_ratio, near, far)

    def set_perspective(self, fov=60, aspect_ratio=1, near=0.1, far=1000):
        self.projection_matrix = Mat44.make_perspective(
            fov, aspect_ratio, near, far)

    def set_ortographic(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        self.projection_matrix = Mat44.make_orthographic(
            left, right, bottom, top, near, far)

    def update_view_matrix(self):
        self.view_matrix = inv(self.get_world_matrix())

    def update_rotation_matrix(self):
        pass

    def update(self):
        pass

    def process_input(self, input: Input):
        pass
