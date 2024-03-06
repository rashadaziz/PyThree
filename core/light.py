from core.Object3D import Object3D


class Light(Object3D):
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3

    def __init__(self, type=0) -> None:
        super().__init__()
        self.type = type
        self.color = [1, 1, 1]
        self.attenuation = [1, 0, 0]


class AmbientLight(Light):
    def __init__(self, color=[1, 1, 1]) -> None:
        super().__init__(Light.AMBIENT)


class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], direction=[0, -1, 0]) -> None:
        super().__init__(Light.DIRECTIONAL)
        self.color = color
        self.set_direction(direction)


class PointLight(Light):
    def __init__(self, color=[1, 1, 1], position=[0, 0, 0], attenuation=[1, 0, 0.1]) -> None:
        super().__init__(Light.POINT)
        self.color = color
        self.set_position(position)
        self.attenuation = attenuation
