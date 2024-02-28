from geometry.parametric import Parametric

class Plane(Parametric):
    def __init__(self, width=1, height=1, n_width_segments=8, n_height_segments=8) -> None:
        def surface_function(u, v):
            return [u, v, 0]

        super().__init__(-width/2, width/2, n_width_segments, -height/2, height/2, n_height_segments, surface_function)

        