from geometry.cylindrical import Cylindrical

class Prism(Cylindrical):
    def __init__(self, radius=1, height=1, sides=6, n_height_segments=4, closed=True) -> None:
        super().__init__(radius, radius, height, sides, n_height_segments, closed, closed)