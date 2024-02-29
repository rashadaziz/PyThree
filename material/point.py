from material.basic import BasicMaterial
from OpenGL.GL import *

class PointMaterial(BasicMaterial):
    def __init__(self, properties={}) -> None:
        super().__init__()

        self.settings["drawStyles"] = GL_POINTS
        self.settings["pointSize"] = 8
        self.settings["roundedPoints"] = False

        self.set_properties(properties)

    def update_render_settings(self):
        glPointSize(self.settings["pointSize"])

        if self.settings["rounderPoints"]:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)