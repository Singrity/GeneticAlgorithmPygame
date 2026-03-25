import pygame

"""
Козма Богдан Григориевич
kozma.bogdan02@gmail.com
https://lms.mospolytech.ru/mod/assign/view.php?id=487354
2026
"""

class Node:
    def __init__(self, x, y, idx, is_start=False, is_end=False):
        self.idx = idx
        self.is_start_node = is_start
        self.is_end_node = is_end
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20) # create a rectangle for the node
        self.color = (0, 130, 170)
        self.font = pygame.font.SysFont('Arial', 16)

    def draw(self, screen):
        if self.is_start_node:
            self.color = (0, 170, 0) # green for start node
        elif self.is_end_node:
            self.color = (170, 0, 0) # red for end node
        else:
            self.color = (0, 0, 170) # blue for other nodes


        # Draw anti-aliased circle
        pygame.draw.circle(screen, self.color, self.rect.center, 20) # draw node as a blue circle
        self.render_text(screen, str(self.idx)) # render node index as text

    def render_text(self, screen, text):
        text_surface = self.font.render(text, True, (250, 250, 250))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)