from OpenGL.GL import *
import pygame
from core.texture import Texture

class RenderTarget:
    def __init__(self, resolution=[512, 512], texture=None, properties={}) -> None:
        self.width, self.height = resolution
        
        if texture is not None:
            self.texture = texture
        else:
            self.texture = Texture(None, {
                "magFilter": GL_LINEAR,
                "minFilter": GL_LINEAR,
                "wrap": GL_CLAMP_TO_EDGE
            })
            self.texture.set_properties(properties)
            self.texture.surface = pygame.Surface(resolution)
            self.texture.upload_data()
        
        self.frame_buffer_ref = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.frame_buffer_ref)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.texture.texture_ref, 0)

        depth_buffer_ref = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depth_buffer_ref)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buffer_ref)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Framebuffer error")

        # reset
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
