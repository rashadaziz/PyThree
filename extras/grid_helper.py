from core.mesh import Mesh
from geometry import Geometry
from material.line import LineMaterial


class GridHelper(Mesh):
    def __init__(self, size=10, n_divisions=10, grid_color=[0, 0, 0], center_color=[.5, .5, .5], line_width=1) -> None:
        geometry = Geometry()
        position_data = []
        color_data = []
        
        values = []
        gap = size / n_divisions
        for n in range(n_divisions+1):
            values.append(-size/2 + n * gap)


        for x in values:
            position_data.append( [x, -size/2, 0] )
            position_data.append( [x,  size/2, 0] )
            if x == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)
        # add horizontal lines
        for y in values:
            position_data.append( [-size/2, y, 0] )
            position_data.append( [ size/2, y, 0] )
            if y == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)

        geometry.add_attribute("vec3", "vertexPosition", position_data)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        geometry.count_vertices()

        material = LineMaterial({
            "useVertexColors": True,
            "lineWidth": line_width,
            "lineType": "segments"
        })

        super().__init__(geometry, material)
