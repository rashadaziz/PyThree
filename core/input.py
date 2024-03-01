import pygame
from pygame.locals import *

class Input:
    def __init__(self) -> None:
        self.is_program_exited = False
        
        self.key_down_set = set()
        self.key_pressed_set = set()
        self.key_up_set = set()

        self.is_mouse_moving = False

    def get(self):
        self.mouse_moving = False
        self.key_down_set.clear()
        self.key_up_set.clear()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_program_exited = True
            if event.type == KEYDOWN:
                self.key_down_set.add(event.key)
                self.key_pressed_set.add(event.key)
            if event.type == KEYUP:
                self.key_up_set.add(event.key)
                self.key_pressed_set.remove(event.key)
            if event.type == MOUSEMOTION:
                self.is_mouse_moving = True

    def is_key_down(self, key):
        return key in self.key_down_set
    
    def is_key_up(self, key):
        return key in self.key_up_set
    
    def is_key_pressed(self, key):
        return key in self.key_pressed_set
            