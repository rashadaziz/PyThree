import pygame
import sys
from abc import ABCMeta, abstractmethod
from core.input import Input


class BaseApplication(metaclass=ABCMeta):
    def __init__(self, screen_size=(512, 512), fps=60) -> None:
        pygame.init()
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL

        # enable anti-aliasing
        pygame.display.gl_set_attribute(
            pygame.GL_MULTISAMPLEBUFFERS, 1
        )
        pygame.display.gl_set_attribute(
            pygame.GL_MULTISAMPLESAMPLES, 4
        )

        # disable deprecated features
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE
        )

        pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 8)

        # init pygame window
        self.screen = pygame.display.set_mode(screen_size, display_flags)
        self.aspect_ratio = screen_size[0] / screen_size[1]

        self.is_running = True
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.time = 0
        self.delta_time = self.clock.get_time() / 1000

        self.input = Input()
        pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def process_events(self, events: "list[pygame.Event]"):
        self.input.process_events(events)
        if self.input.is_program_exited:
            self.is_running = False

    def run(self):
        self.initialize()
        while self.is_running:
            # process user input
            events = pygame.event.get()
            self.process_events(events)

            self.delta_time = self.clock.get_time() / 1000
            self.time += self.delta_time

            # update state
            self.update()

            # update screen
            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")

            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit(0)
