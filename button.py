import pygame
from enum import Enum, auto
from ga import ALG_TO_BUTTON_TEXT

class ButtonType(Enum):
    CONTROL = auto()
    SELECTION_TYPE = auto()
    CROSOVER_TYPE = auto()
    MUTATION_TYPE = auto()



class Button:
    def __init__(self, text: str, x=0, y=0, is_active: bool = False, bid: int = 0, btype: ButtonType = ButtonType.CONTROL):
        print(text)
        self.bid = bid
        self.btype = btype
        if self.btype == ButtonType.CONTROL:
            self.rect = pygame.Rect(x, y, 150, 35)
        elif self.btype == ButtonType.SELECTION_TYPE or self.btype == ButtonType.CROSOVER_TYPE or self.btype == ButtonType.MUTATION_TYPE:
            self.rect = pygame.Rect(x, y, 130, 25)
            self.active_rect = pygame.Rect(x - 5, y - 5, self.rect.width + 10, self.rect.height + 10)
        self.is_active = is_active
        

        self.active_color = (170, 170, 170)
        self.text = text
        self.font = pygame.font.SysFont('Arial', 20)
        self.color = (200, 200, 200)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect) # draw button rectangle
        if self.is_active:
            pygame.draw.rect(surface, self.active_color, self.active_rect, 1) # draw button rectangle
            self.color = (170, 170, 170)
        else:
            self.color = (200, 200, 200)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0)) # render button text
        text_rect = text_surface.get_rect(center=self.rect.center) # center text on button
        surface.blit(text_surface, text_rect) # draw text on button

    def update(self, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.color = (170, 170, 170) # darker color on hover
        elif not self.active_color:
            self.color = (200, 200, 200) # default color

    def is_hovered(self, pos):

        return self.rect.collidepoint(pos)

    def __repr__(self):
        repr_str = f"Button(id={self.bid}, text='{self.text}', rect={self.rect}, type={self.btype}, is_active={self.is_active})"
 
        return repr_str