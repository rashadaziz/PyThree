from geometry.parametric import Parametric
from math import sin, cos, pi

class Ellipsoid(Parametric):
    def __init__(self, width=1, height=1, depth=1, n_radius_segments=32, n_height_segments=16) -> None:
        def surface_function(u, v):
            return [
                width/2 * sin(u) * cos(v),
                height/2 * sin(v),
                depth/2 * cos(u) * cos(v)
            ]

        super().__init__(0, 2*pi, n_radius_segments, -pi/2, pi/2, n_height_segments, surface_function)