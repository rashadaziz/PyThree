from geometry.ellipsoid import EllipsoidGeometry

class SphereGeometry(EllipsoidGeometry):
    def __init__(self, radius=1, n_radius_segments=32, n_height_segments=16) -> None:
        super().__init__(2*radius, 2*radius, 2*radius, n_radius_segments, n_height_segments)