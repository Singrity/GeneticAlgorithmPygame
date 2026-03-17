import pygame


class Toggle:
    """
    Toggle switch element for enabling/disabling options (e.g., adaptive mutation).
    Click to switch between ON and OFF states.
    """

    def __init__(self, x, y, width, height, label, is_on=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.is_on = is_on

        self.font = pygame.font.SysFont('Arial', 20)
        self.label_color = (50, 50, 50)
        self.track_on_color = (0, 180, 0)  # Green when ON
        self.track_off_color = (150, 150, 150)  # Gray when OFF
        self.thumb_color = (255, 255, 255)
        self.border_color = (100, 100, 100)

        # Toggle dimensions
        self.track_height = height - 4
        self.thumb_radius = (height - 8) // 2

    def draw(self, surface):
        # Draw label
        label_surface = self.font.render(self.label, True, self.label_color)
        label_rect = label_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
        surface.blit(label_surface, label_rect)

        # Draw track (background)
        track_color = self.track_on_color if self.is_on else self.track_off_color
        track_rect = pygame.Rect(
            self.rect.left + 2,
            self.rect.top + 2,
            self.rect.width - 4,
            self.track_height
        )
        pygame.draw.rect(surface, track_color, track_rect, border_radius=self.track_height // 2)
        pygame.draw.rect(surface, self.border_color, track_rect, 2, border_radius=self.track_height // 2)

        # Draw thumb (circle that moves)
        if self.is_on:
            thumb_x = self.rect.right - self.thumb_radius - 4
        else:
            thumb_x = self.rect.left + self.thumb_radius + 4
        thumb_y = self.rect.centery

        pygame.draw.circle(surface, self.thumb_color, (thumb_x, thumb_y), self.thumb_radius)
        pygame.draw.circle(surface, self.border_color, (thumb_x, thumb_y), self.thumb_radius, 2)

        # Draw ON/OFF text
        status_text = "ON" if self.is_on else "OFF"
        status_color = self.track_on_color if self.is_on else self.track_off_color
        status_surface = self.font.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        surface.blit(status_surface, status_rect)

    def update(self, mouse_pos):
        pass

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.is_on = not self.is_on
            return True
        return False

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def get_value(self):
        return self.is_on

    def set_value(self, is_on):
        self.is_on = is_on
