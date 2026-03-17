import pygame

class Edge:
    def __init__(self, node_a, node_b, weight):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight
        self.font = pygame.font.SysFont('Arial', 16)

    def draw(self, screen):
        # draw anti-aliased edge line between node centers
        a_pos = self.node_a.rect.center
        b_pos = self.node_b.rect.center

        # render weight and center the text at the midpoint
        self.render_text(screen, str(self.weight))
        pygame.draw.aaline(screen, (190, 190, 190), a_pos, b_pos)

    def render_text(self, screen, text):
        text_surface = self.font.render(text, True, (0, 0, 200))
        mid_x = (self.node_a.rect.center[0] + self.node_b.rect.center[0]) // 2
        mid_y = ((self.node_a.rect.center[1] + self.node_b.rect.center[1]) // 2) - 10
        text_rect = text_surface.get_rect(center=(mid_x, mid_y))
        screen.blit(text_surface, text_rect)