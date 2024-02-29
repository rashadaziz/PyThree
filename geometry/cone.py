from geometry.cylindrical import CylindricalGeometry


class ConeGeometry(CylindricalGeometry):
    def __init__(self, radius_bottom=1, height=1, n_radial_segments=32, n_height_segments=4, closed=True) -> None:
        super().__init__(0, radius_bottom, height,
                         n_radial_segments, n_height_segments, False, closed)
