from extras.first_person_camera import FirstPersonCamera
from core.camera import Camera
from math import sin, cos


class ViewBobbingCamera(FirstPersonCamera):
    def __init__(self, clock, fov=60, aspect_ratio=1, near=0.1, far=1000, initial_position=[0, 1, 0]) -> None:
        super().__init__(clock, fov, aspect_ratio, near, far, initial_position)

        self.bob_cam = Camera()
        self.add(self.bob_cam)

        self.time = 0

    def get_world_matrix(self):
        fps_matrix = self.translation_matrix @ self.rotation_matrix @ self.scale_matrix
        bob_matrix = self.bob_cam.translation_matrix @ self.bob_cam.rotation_matrix @ self.bob_cam.scale_matrix
        model_matrix = fps_matrix @ bob_matrix

        if self.parent is None:
            return model_matrix

        return self.parent.get_world_matrix() @ model_matrix

    def update_view_matrix(self):
        delta_time = self.clock.get_time() / 1000
        x_speed = 10*self.time
        y_speed = 15*self.time
        x_amplitude = 0.0045
        y_amplitude = 0.03
        x_damping = 0.994
        y_damping = 0.98
        constant = 50

        if self.is_moving and not self.no_clip:
            self.bob_cam.translation_matrix.itemset(
                (1, 3), y_amplitude*sin(y_speed)*delta_time*constant)
            self.bob_cam.translation_matrix.itemset(
                (0, 3), x_amplitude*cos(x_speed)*delta_time*constant)
        else:
            x, y = self.bob_cam.translation_matrix[:2, 3]
            self.bob_cam.translation_matrix.itemset(
                (1, 3), y*y_damping*delta_time*constant)
            self.bob_cam.translation_matrix.itemset(
                (0, 3), x*x_damping*delta_time*constant)

        return super().update_view_matrix()

    def update(self):
        self.time += self.clock.get_time() / 1000

        return super().update()
