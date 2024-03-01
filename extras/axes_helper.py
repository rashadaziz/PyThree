from core.mesh import Mesh
from geometry import Geometry
from material.line import LineMaterial


class AxesHelper(Mesh):
    def __init__(self, axis_length=1, line_width=4, axis_colors=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]) -> None:
        geometry = Geometry()
        position_data = [
            [0, 0, 0], [axis_length, 0, 0], # x-axis
            [0, 0, 0], [0, axis_length, 0], # y-axis
            [0, 0, 0], [0, 0, axis_length] # z-axis
        ]
        color_data = [
            axis_colors[0], axis_colors[0],
            axis_colors[1], axis_colors[1],
            axis_colors[2], axis_colors[2]
        ]

        geometry.add_attribute("vec3", "vertexPosition", position_data)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        geometry.count_vertices()

        material = LineMaterial({
            "useVertexColors": True,
            "lineWidth": line_width,
            "lineType": "segments"
        })

        super().__init__(geometry, material)
