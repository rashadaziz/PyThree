from geometry.parametric import Parametric
from geometry.polygon import Polygon
from core.matrix import Mat44
from math import sin, cos, pi


class Cylindrical(Parametric):
    def __init__(self, radius_top=1, radius_bottom=1, height=1, n_radial_segments=32, n_height_segments=4, closed_top=True, closed_bottom=True) -> None:
        def surface_function(u, v):
            return [
                (v*radius_top + (1-v)*radius_bottom) * sin(u),
                height * (v-0.5),
                (v*radius_top + (1-v)*radius_bottom * cos(u))
            ]

        super().__init__(0, 2*pi, n_radial_segments, 0, 1, n_height_segments, surface_function)

        if closed_top:
            top_geom = Polygon(n_radial_segments, radius_top)
            transform = Mat44.make_translation(0, height/2, 0) @ Mat44.make_rotation_y(-pi/2) @ Mat44.make_rotation_x(-pi/2)
            top_geom.apply_matrix(transform)
            self.merge(top_geom)
        
        if closed_bottom:
            bottom_geom = Polygon(n_radial_segments, radius_bottom)
            transform = Mat44.make_translation(0, -height/2, 0) @ Mat44.make_rotation_y(-pi/2) @ Mat44.make_rotation_x(pi/2)
            bottom_geom.apply_matrix(transform)
            self.merge(bottom_geom)