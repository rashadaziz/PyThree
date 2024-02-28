from core.Object3D import Object3D
from core.matrix import Mat44
from numpy.linalg import inv

class Camera(Object3D):
    def __init__(self, fov=60, aspect_ratio=1, near=0.1, far=1000) -> None:
        super().__init__()

        self.view_matrix = Mat44.make_identity()
        self.projection_matrix = Mat44.make_perspective(fov, aspect_ratio, near, far)

    def update_view_matrix(self):
        self.view_matrix = inv(self.get_world_matrix())

    