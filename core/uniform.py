from OpenGL.GL import *

class Uniform:
    def __init__(self, data_type, data) -> None:
        self.data_type = data_type
        self.data = data

        self.variable_ref = None
    
    def locate_variable(self, program_ref, variable_name):
        if self.data_type == "Light":
            self.variable_ref = {}
            self.variable_ref["type"] = glGetUniformLocation(program_ref, variable_name + ".type")
            self.variable_ref["color"] = glGetUniformLocation(program_ref, variable_name + ".color")
            self.variable_ref["direction"] = glGetUniformLocation(program_ref, variable_name + ".direction")
            self.variable_ref["position"] = glGetUniformLocation(program_ref, variable_name + ".position")
            self.variable_ref["attenuation"] = glGetUniformLocation(program_ref, variable_name + ".attenuation")
            return

        self.variable_ref = glGetUniformLocation(program_ref, variable_name)
    
    def upload_data(self):
        if self.variable_ref is None:
            raise Exception(
                'Uniform variable_ref is None. It is likely that you have not called Uniform.locate_variable(program_ref, variable name) yet.')

        if self.variable_ref == -1:
            return
        
        if self.data_type == "int":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "bool":
            glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "float":
            glUniform1f(self.variable_ref, self.data)
        elif self.data_type == "vec2":
            glUniform2f(self.variable_ref, *self.data)
        elif self.data_type == "vec3":
            glUniform3f(self.variable_ref, *self.data)
        elif self.data_type == "vec4":
            glUniform4f(self.variable_ref, *self.data)
        elif self.data_type == "mat4":
            # transpose the matrix since OpenGL expects column-major orientation
            glUniformMatrix4fv(self.variable_ref, 1, GL_TRUE, self.data)
        elif self.data_type == "sampler2D":
            texture_obj_ref, texture_unit_ref = self.data
            glActiveTexture(GL_TEXTURE0 + texture_unit_ref)
            glBindTexture(GL_TEXTURE_2D, texture_obj_ref)
            glUniform1i(self.variable_ref, texture_unit_ref)

            # reset
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, 0)
        elif self.data_type == "Light":
            glUniform1i(self.variable_ref["type"], self.data.type)
            glUniform3f(self.variable_ref["color"], *self.data.color)
            glUniform3f(self.variable_ref["direction"], *self.data.get_direction())
            glUniform3f(self.variable_ref["position"], *self.data.get_world_position())
            glUniform3f(self.variable_ref["attenuation"], *self.data.attenuation)

                    
