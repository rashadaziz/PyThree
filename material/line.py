from material.basic import BasicMaterial
from OpenGL.GL import *

class LineMaterial(BasicMaterial):
    def __init__(self, properties={}) -> None:
        super().__init__()

        self.settings["drawStyle"] = GL_LINE_STRIP
        self.settings["lineWidth"] = 1
        self.settings["lineType"] = "connected"

        self.set_properties(properties)

    def update_render_settings(self):
        glLineWidth(self.settings["lineWidth"])

        line_type = self.settings["lineType"]

        if line_type == "connected":
            self.settings["drawStyle"] = GL_LINE_STRIP
        elif line_type == "loop":
            self.settings["drawStyle"] = GL_LINE_LOOP
        elif line_type == "segments":
            self.settings["drawStyle"] = GL_LINES
        else:
            raise Exception(f"Attempting to draw LineMaterial with unknown line style '{line_type}'")