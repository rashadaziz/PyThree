from geometry.cylindrical import CylindricalGeometry

class CylinderGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1, n_radial_segments=32, n_height_segments=4, closed=True) -> None:
        super().__init__(radius, radius, height, n_radial_segments, n_height_segments, closed, closed)