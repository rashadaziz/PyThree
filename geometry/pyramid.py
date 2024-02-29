from geometry.cylindrical import CylindricalGeometry


class PyramidGeometry(CylindricalGeometry):
    def __init__(self, width_bottom=1, height=1, sides=4, n_height_segments=4, closed=True) -> None:
        super().__init__(0, width_bottom, height,
                         sides, n_height_segments, False, closed)
