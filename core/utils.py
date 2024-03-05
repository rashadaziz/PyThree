from OpenGL.GL import *

ASSETS_PATH = 'assets/'
SHADER_PATH = ASSETS_PATH + 'shaders/'
OBJECT_PATH = ASSETS_PATH + 'objects/'
TEXTURE_PATH = ASSETS_PATH + 'textures/'

class OpenGLUtils:
    @staticmethod
    def init_shader(shader_code, shader_type):
        # try to compile shader; either vertex or fragment
        shader_ref = glCreateShader(shader_type)
        glShaderSource(shader_ref, shader_code)
        glCompileShader(shader_ref)

        is_compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)

        if not is_compile_success:
            err_msg = glGetShaderInfoLog(shader_ref)
            glDeleteShader(shader_ref)
            err_msg = f"\n{err_msg.decode('utf-8')}"
            raise Exception(err_msg)
        
        return shader_ref
    
    @staticmethod
    def init_program(vert_shader, frag_shader):
        vert_shader_ref = OpenGLUtils.init_shader(vert_shader, GL_VERTEX_SHADER)
        frag_shader_ref = OpenGLUtils.init_shader(frag_shader, GL_FRAGMENT_SHADER)
        program_ref = glCreateProgram()
        glAttachShader(program_ref, vert_shader_ref)
        glAttachShader(program_ref, frag_shader_ref)
        glLinkProgram(program_ref)

        is_link_success = glGetProgramiv(program_ref, GL_LINK_STATUS)

        if not is_link_success:
            err_msg = glGetProgramInfoLog(program_ref)
            glDeleteProgram(program_ref)
            err_msg = f"\n{err_msg.decode('utf-8')}"
            raise Exception(err_msg)
        
        return program_ref
    
    @staticmethod
    def print_system_info():
        print()
        print("~~~ System Information ~~~")
        print(f"Vendor: {glGetString(GL_VENDOR).decode('utf-8')}")
        print(f"Renderer: {glGetString(GL_RENDERER).decode('utf-8')}")
        print(f"OpenGL version: {glGetString(GL_VERSION).decode('utf-8')}")
        print(f"GLSL version: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')}")


def load_shader(shader_file_name: str):
    with open(SHADER_PATH + shader_file_name) as shader:
        content = shader.read()
    return content

def lerp(a, b, t):
    return (1 - t) * a + t * b