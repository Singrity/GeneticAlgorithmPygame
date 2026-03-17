import pygame

class Button:
    def __init__(self, width, height, text, x=0, y=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', 20)
        self.color = (200, 200, 200)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect) # draw button rectangle
        text_surface = self.font.render(self.text, True, (0, 0, 0)) # render button text
        text_rect = text_surface.get_rect(center=self.rect.center) # center text on button
        surface.blit(text_surface, text_rect) # draw text on button

    def update(self, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.color = (170, 170, 170) # darker color on hover
        else:
            self.color = (200, 200, 200) # default color

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

        