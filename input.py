import pygame


class Input:
    """
    Input element for entering numeric values (e.g., mutation rate, population size).
    Supports focus/click to activate, keyboard input, and optional min/max constraints.
    """

    def __init__(self, width, height, label, value, x=0, y=0, min_value=None, max_value=None, is_integer=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = value
        self.original_value = value
        self.min_value = min_value
        self.max_value = max_value
        self.is_integer = is_integer

        self.font = pygame.font.SysFont('Arial', 20)
        self.label_color = (50, 50, 50)
        self.bg_color = (255, 255, 255)
        self.border_color = (100, 100, 100)
        self.active_color = (0, 120, 215)
        self.text_color = (0, 0, 0)

        self.is_active = False
        self.input_text = str(value)

    def draw(self, surface):
        # Draw label
        label_surface = self.font.render(self.label, True, self.label_color)
        label_rect = label_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
        surface.blit(label_surface, label_rect)

        # Draw input background
        border_color = self.active_color if self.is_active else self.border_color
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 2)

        # Draw value text
        text_surface = self.font.render(self.input_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        # Update visual state based on hover (optional hover effect could be added)
        pass

    def is_clicked(self, pos) -> bool:
        if self.rect.collidepoint(pos):
            self.input_text = str(self.value)
            return True
        else:
            self.input_text = str(self.value)
            return False

    def handle_events(self, event: pygame.event.Event):
        if not self.is_active:
            return 

        if event.key == pygame.K_RETURN:
            self._commit_value()
            self.is_active = False
        elif event.key == pygame.K_ESCAPE:
            self.input_text = str(self.original_value)
            self.is_active = False
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_MINUS or (event.key >= pygame.K_0 and event.key <= pygame.K_9):
            # Allow minus sign and digits
            char = event.unicode
            if char.isdigit() or (char == '-' and len(self.input_text) == 0):
                self.input_text += char
        elif event.key == pygame.K_PERIOD and not self.is_integer:
            # Allow decimal point for float inputs
            if '.' not in self.input_text:
                self.input_text += '.'


    def _commit_value(self):
        try:
            if self.is_integer:
                new_value = int(self.input_text) if self.input_text else 0
            else:
                new_value = float(self.input_text) if self.input_text else 0.0

            # Apply constraints
            if self.min_value is not None:
                new_value = max(self.min_value, new_value)
            if self.max_value is not None:
                new_value = min(self.max_value, new_value)

            self.value = new_value
            self.input_text = str(new_value)
            self.original_value = new_value
        except ValueError:
            # Invalid input, revert to original value
            self.input_text = str(self.original_value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.original_value = value
        self.input_text = str(value)

    def deactivate(self):
        self.is_active = False
        self.input_text = str(self.value)

    def __repr__(self):
        return f"Input(label={self.label}, is_active={self.is_active})"