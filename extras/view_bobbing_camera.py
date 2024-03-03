from extras.first_person_camera import FirstPersonCamera
from core.matrix import Mat44
from math import sin, cos
import numpy as np


class ViewBobbingCamera(FirstPersonCamera):
    def __init__(self, clock, effect_multiplier=1, fov=60, aspect_ratio=1, near=0.1, far=1000, initial_position=[0, 1, 0]) -> None:
        super().__init__(clock, fov, aspect_ratio, near, far, initial_position)

        self.bob_translation_matrix = Mat44.make_identity()

        self.time = 0
        self.effect_multiplier = effect_multiplier

    def get_world_matrix(self):
        fps_matrix = self.translation_matrix @ self.rotation_matrix @ self.scale_matrix
        bob_matrix = self.bob_translation_matrix
        model_matrix = fps_matrix @ bob_matrix
        if self.parent is None:
            return model_matrix

        return self.parent.get_world_matrix() @ model_matrix

    def update_view_matrix(self):
        delta_time = self.clock.get_time() / 1000
        x_speed = 10*self.time
        y_speed = 15*self.time
        x_amplitude = 0.0045*self.effect_multiplier
        y_amplitude = 0.03*self.effect_multiplier
        x_amplitude_rest = 0.009*self.effect_multiplier
        y_amplitude_rest = 0.015*self.effect_multiplier
        constant = 50

        is_on_ground = not self.no_clip and np.isclose(
            self.get_position()[1], 1)

        if self.is_moving and is_on_ground:
            self.bob_translation_matrix.itemset(
                (1, 3), y_amplitude*sin(y_speed)*delta_time*constant)
            self.bob_translation_matrix.itemset(
                (0, 3), x_amplitude*cos(x_speed)*delta_time*constant)
        elif is_on_ground:
            self.bob_translation_matrix.itemset(
                (1, 3), y_amplitude_rest*sin(y_speed*0.1)*delta_time*constant)
            self.bob_translation_matrix.itemset(
                (0, 3), x_amplitude_rest*cos(x_speed*0.1)*delta_time*constant)
        else:
            self.bob_translation_matrix.itemset((1, 3), 0)
            self.bob_translation_matrix.itemset((0, 3), 0)

        return super().update_view_matrix()

    def update(self):
        self.time += self.clock.get_time() / 1000

        return super().update()
