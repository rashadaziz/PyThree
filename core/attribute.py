from OpenGL.GL import *
import numpy as np

class Attribute:
    def __init__(self, data_type, data) -> None:
        # int/float/vec2/vec3/vec4
        self.data_type = data_type
        # array of data to be stored in buffer
        self.data = data

        self.buffer_ref = glGenBuffers(1)

        self.upload_data()

    def upload_data(self):
        data = np.array(self.data).astype(np.float32)
        # create buffer referenced by buffer_ref
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)
        # store data to the buffer
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)
    
    def associate_variable(self, program_ref, variable_name):
        variable_ref = glGetAttribLocation(program_ref, variable_name)

        if variable_ref == -1:
            return
        
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)

        if self.data_type == 'int':
            glVertexAttribPointer(variable_ref, 1, GL_INT, False, 0, None)
        elif self.data_type == 'float':
            glVertexAttribPointer(variable_ref, 1, GL_FLOAT, False, 0, None)
        elif self.data_type == 'vec2':
            glVertexAttribPointer(variable_ref, 2, GL_FLOAT, False, 0, None)
        elif self.data_type == 'vec3':
            glVertexAttribPointer(variable_ref, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == 'vec4':
            glVertexAttribPointer(variable_ref, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception(f"Attribute {variable_name} has unknown type: {self.data_type}")
        
        glEnableVertexAttribArray(variable_ref)
        