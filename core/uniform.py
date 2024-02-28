from OpenGL.GL import *

class Uniform:
    def __init__(self, data_type, data) -> None:
        self.data_type = data_type
        self.data = data

        self.variable_ref = None
    
    def locate_variable(self, program_ref, variable_name):
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
            glUniformMatrix4fv(self.variable_ref, 1, GL_TRUE, self.data)
        
