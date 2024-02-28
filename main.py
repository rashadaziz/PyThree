from core.base import BaseApplication
from core.utils import OpenGLUtils, load_shader
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Mat44
from OpenGL.GL import *
from pygame.locals import *
import math


class Test(BaseApplication):
    def initialize(self):
        OpenGLUtils.print_system_info()

        vert_shader_code = load_shader('shader.vert')
        frag_shader_code = load_shader('shader.frag')

        self.program_ref = OpenGLUtils.init_program(
            vert_shader_code, frag_shader_code)
        
        self.base_color = Uniform("vec3", [1.0, .0, .0])
        self.base_color.locate_variable(self.program_ref, "baseColor")

        # Render Settings
        glClearColor(.0, .0, .0, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Setup Object
        vao_ref = glGenVertexArrays(1)
        glBindVertexArray(vao_ref)

        position_data = [
            [ .0,  .2, .0],
            [ .1, -.2, .0],
            [-.1, -.2, .0]
        ]
        self.vertex_count = len(position_data)
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        # Setup Uniform Variables
        model_matrix = Mat44.make_translation(0, 0, -1)
        self.model_matrix = Uniform("mat4", model_matrix)
        self.model_matrix.locate_variable(self.program_ref, "modelMatrix")

        projection_matrix = Mat44.make_perspective()
        self.projection_matrix = Uniform("mat4", projection_matrix)
        self.projection_matrix.locate_variable(self.program_ref, "projectionMatrix")

        # other variables
        self.move_speed = 0.5
        self.rot_speed = 90 * (math.pi/180)

    def update(self):
        dist_diff = self.move_speed * self.delta_time
        rot_diff = self.rot_speed * self.delta_time

        # global transform matrix
        glb_transform = Mat44.make_identity()

        # global translation
        if self.input.is_key_pressed(K_w):
            glb_transform = glb_transform @ Mat44.make_translation(0, dist_diff, 0)
        if self.input.is_key_pressed(K_s):
            glb_transform = glb_transform @ Mat44.make_translation(0, -dist_diff, 0)
        if self.input.is_key_pressed(K_a):
            glb_transform = glb_transform @ Mat44.make_translation(-dist_diff, 0, 0)
        if self.input.is_key_pressed(K_d):
            glb_transform = glb_transform @ Mat44.make_translation(dist_diff, 0, 0)
        if self.input.is_key_pressed(K_z):
            glb_transform = glb_transform @ Mat44.make_translation(0, 0, dist_diff)
        if self.input.is_key_pressed(K_x):
            glb_transform = glb_transform @ Mat44.make_translation(0, 0, -dist_diff)

        # global rotation
        if self.input.is_key_pressed(K_q):
            glb_transform = glb_transform @ Mat44.make_rotation_y(rot_diff)
        if self.input.is_key_pressed(K_e):
            glb_transform = glb_transform @ Mat44.make_rotation_y(-rot_diff)
        
        self.model_matrix.data = glb_transform @ self.model_matrix.data

        # local transform matrix
        lcl_transform = Mat44.make_identity()

        # local translation
        if self.input.is_key_pressed(K_i):
            lcl_transform = lcl_transform @ Mat44.make_translation(0, dist_diff, 0)
        if self.input.is_key_pressed(K_k):
            lcl_transform = lcl_transform @ Mat44.make_translation(0, -dist_diff, 0)
        if self.input.is_key_pressed(K_j):
            lcl_transform = lcl_transform @ Mat44.make_translation(-dist_diff, 0, 0)
        if self.input.is_key_pressed(K_l):
            lcl_transform = lcl_transform @ Mat44.make_translation(dist_diff, 0, 0)

        # local rotation
        if self.input.is_key_pressed(K_u):
            lcl_transform = lcl_transform @ Mat44.make_rotation_y(rot_diff)
        if self.input.is_key_pressed(K_o):
            lcl_transform = lcl_transform @ Mat44.make_rotation_y(-rot_diff)

        self.model_matrix.data = self.model_matrix.data @ lcl_transform

        # render scene
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        glUseProgram(self.program_ref) 
        self.projection_matrix.upload_data() 
        self.model_matrix.upload_data()
        self.base_color.upload_data()
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


def main():
    Test().run()


if __name__ == "__main__":
    main()
