import pygame
from core.utils import TEXTURE_PATH
from OpenGL.GL import *

class Texture:
    def __init__(self, file_name=None, properties={}) -> None:
        self.surface = None
        self.texture_ref = glGenTextures(1)

        self.properties = {
            "magFilter": GL_LINEAR,
            "minFilter": GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL_REPEAT
        }

        self.set_properties(properties)

        if file_name:
            self.load_image(TEXTURE_PATH + file_name)
            self.upload_data()

    def load_image(self, file_name):
        self.surface = pygame.image.load(file_name).convert_alpha()
    
    def set_properties(self, props):
        for name, data in props.items():
            if name in self.properties.keys():
                self.properties[name] = data
            else:
                raise Exception(f"Texture has no property named '{name}'")
            
    def upload_data(self):
        width, height = self.surface.get_size()
        pixel_data = pygame.image.tostring(self.surface, "RGBA", 1)
        glBindTexture(GL_TEXTURE_2D, self.texture_ref)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, False, GL_RGBA, GL_UNSIGNED_BYTE, pixel_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        # magnify/minify settings
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.properties["magFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.properties["minFilter"])
        # set what happens when texture coordinates go outside range [0, 1]
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.properties["wrap"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.properties["wrap"])
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1, 1, 1, 1])

        # reset
        glBindTexture(GL_TEXTURE_2D, 0)