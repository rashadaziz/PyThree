from core.texture import Texture
import pygame


class TextTexture(Texture):
    def __init__(
        self,
        text="",
        system_font="Arial",
        font_file=None,
        font_size=24,
        font_color=[0, 0, 0],
        bg_color=[255, 255, 255],
        transparent=False,
        image_width=None,
        image_height=None,
        margin_horizontal=0.0,
        margin_vertical=0.0,
        image_border_width=0.0,
        image_border_color=[0, 0, 0],
        center=True
    ) -> None:
        super().__init__()
        self.font = pygame.font.SysFont(system_font, font_size)
        if font_file:
            self.font = pygame.font.Font(font_file)

        font_surf = self.font.render(text, True, font_color)
        text_width, text_height = self.font.size(text)

        if image_width is None:
            image_width = text_width
        if image_height is None:
            image_height = text_height

        self.surface = pygame.Surface(
            (image_width, image_height), pygame.SRCALPHA)

        if not transparent:
            self.surface.fill(bg_color)

        corner = (margin_horizontal*(image_width-text_width),
                  margin_vertical*(image_height-text_height))
        dest_rect = font_surf.get_rect(topleft=corner)

        if center:
            dest_rect.topleft = ((image_width-text_width)/2,
                                 (image_height-text_height)/2)

        if image_border_width:
            pygame.draw.rect(self.surface, image_border_color, [
                             0, 0, image_width, image_height], image_border_width)

        self.surface.blit(font_surf, dest_rect)
        self.upload_data()
