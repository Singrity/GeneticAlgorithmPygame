from button import Button
from input import Input
from graph import Graphic
import math
import pygame


class ControlPanel:
    def __init__(
        self,
        panel_pos,
        panel_size,
        graphic_pos,
        graphic_size,
        input_size,
        button_size,
        initial_population_size,
        initial_generations,
        initial_mutation_rate,
        initial_network_size
    ):
        self.panel_pos = panel_pos
        self.panel_size = panel_size
        
        # Create the control surface
        self.control_surface = pygame.Surface((int(panel_size.x), int(panel_size.y)))
        self.control_surface.fill((220, 220, 220))  # light gray background
        
        # Initialize lists for buttons and inputs
        self.buttons = []
        self.inputs = []
        
        # Padding for layout
        padding_x = 20
        padding_y = 20
        spacing = 30
        
        # Current y position for layout
        current_y = padding_y
        
        # Add label at the top
        font = pygame.font.SysFont('Arial', 24, bold=True)
        title = font.render("Settings", True, (50, 50, 50))
        title_rect = title.get_rect(centerx=int(panel_size.x) // 2, top=current_y)
        self.control_surface.blit(title, title_rect)
        current_y += title_rect.height + spacing
        
        # Add input fields
        self._add_input("population_size", initial_population_size, input_size, padding_x, current_y, is_integer=True, min_value=5, max_value=10000)
        current_y += input_size.y + spacing
        
        self._add_input("generations", initial_generations, input_size, padding_x, current_y, is_integer=True, min_value=10, max_value=math.inf)
        current_y += input_size.y + spacing
        
        self._add_input("mutation_rate", initial_mutation_rate, input_size, padding_x, current_y, is_integer=False, min_value=0.01, max_value=1.0)
        current_y += input_size.y + spacing
        
        self._add_input("network_size", initial_network_size, input_size, padding_x, current_y, is_integer=True, min_value=5, max_value=100)
        current_y += input_size.y + spacing
        
        # Add adaptive mutation toggle (checkbox area)
        self.adaptive_mutation_enabled = False
        checkbox_size = 20
        checkbox_y = current_y + 5
        self.adaptive_checkbox_rect = pygame.Rect(padding_x, checkbox_y, checkbox_size, checkbox_size)
        adaptive_font = pygame.font.SysFont('Arial', 18)
        adaptive_text = adaptive_font.render("Adaptive Mutation", True, (50, 50, 50))
        adaptive_text_rect = adaptive_text.get_rect(midleft=(padding_x + checkbox_size + 10, checkbox_y + checkbox_size // 2))
        self.adaptive_text_rect = adaptive_text_rect
        # Create combined click area for checkbox + text
        self.adaptive_click_area = self.adaptive_checkbox_rect.union(adaptive_text_rect)
        current_y += checkbox_size + spacing
        
        # Add buttons
        button_y = current_y
        self._add_button("Start", button_size, padding_x, button_y)
        self._add_button("Stop", button_size, padding_x + button_size.x + spacing, button_y)
        self._add_button("Reset", button_size, padding_x + (button_size.x + spacing) * 2, button_y)
        button_y += button_size.y + spacing
        self._add_button("Apply", button_size, padding_x, button_y)
        self._add_button("Exit", button_size, padding_x + button_size.x + spacing, button_y)

        
        # Initialize graphic (fitness graph)
        self.graphic = Graphic(graphic_pos.x, graphic_pos.y, int(graphic_size.x), int(graphic_size.y))

        self._add_button("Clear", button_size, padding_x, self.graphic.rect.bottom)

    def _add_input(self, label, value, size, x, y, is_integer=False, min_value=None, max_value=None):
        input_field = Input(
            int(size.x), int(size.y),
            label=label,
            value=value,
            x=x, y=y,
            is_integer=is_integer,
            min_value=min_value,
            max_value=max_value
        )
        self.inputs.append(input_field)

    def _add_button(self, text, size, x, y):
        button = Button(int(size.x), int(size.y), text, x, y)
        self.buttons.append(button)

    def draw(self, screen, mouse_pos=None):
        # Draw the control panel surface at the right side of the screen
        screen.blit(self.control_surface, (self.panel_pos.x, self.panel_pos.y))

        # Draw all input fields
        for input_field in self.inputs:
            input_field.draw(self.control_surface)

        # Draw all buttons
        for button in self.buttons:
            button.draw(self.control_surface)

        # Draw adaptive mutation checkbox
        is_hovered = mouse_pos and self.is_mouse_over_adaptive_checkbox(mouse_pos)
        checkbox_color = (0, 120, 215) if self.adaptive_mutation_enabled else (255, 255, 255)
        border_color = (0, 100, 200) if is_hovered else (100, 100, 100)
        pygame.draw.rect(self.control_surface, border_color, self.adaptive_checkbox_rect, 2)
        pygame.draw.rect(self.control_surface, checkbox_color, self.adaptive_checkbox_rect.inflate(-4, -4))
        adaptive_font = pygame.font.SysFont('Arial', 18)
        adaptive_text = adaptive_font.render("Adaptive Mutation", True, (50, 50, 50))
        self.control_surface.blit(adaptive_text, self.adaptive_text_rect)

        # Draw the fitness graph on the control surface
        self.graphic.draw(self.control_surface)

    def update(self, mouse_pos):
        # Check if display is initialized
        if pygame.display.get_surface() is None:
            return

        # Convert mouse position to panel coordinates
        panel_mouse_pos = (mouse_pos[0] - self.panel_pos.x, mouse_pos[1] - self.panel_pos.y)

        # Update buttons
        for button in self.buttons:
            button.update(panel_mouse_pos)

        # Update inputs
        for input_field in self.inputs:
            input_field.update(panel_mouse_pos)

    def is_mouse_over_adaptive_checkbox(self, mouse_pos):
        # Check if mouse is over the adaptive mutation checkbox area
        panel_mouse_pos = (mouse_pos[0] - self.panel_pos.x, mouse_pos[1] - self.panel_pos.y)
        return self.adaptive_click_area.collidepoint(panel_mouse_pos)

    def handle_click(self, pos):
        # Convert to panel coordinates
        panel_pos = (pos[0] - self.panel_pos.x, pos[1] - self.panel_pos.y)

        # Check adaptive mutation checkbox FIRST (click area includes text)
        if self.adaptive_click_area.collidepoint(panel_pos):
            self.adaptive_mutation_enabled = not self.adaptive_mutation_enabled
            # Deactivate any active inputs
            for input_field in self.inputs:
                input_field.deactivate()
            return None

        # Check inputs
        for input_field in self.inputs:
            if input_field.handle_click(panel_pos):
                return None  # Input was activated, don't process buttons

        # Check buttons
        for button in self.buttons:
            if button.is_hovered(panel_pos):
                return button.text

        # Clicked outside everything - deactivate inputs
        for input_field in self.inputs:
            input_field.deactivate()

        return None

    def handle_key(self, event):
        # Pass keyboard events to active input fields
        for input_field in self.inputs:
            if input_field.is_active:
                if input_field.handle_key(event):
                    return True
        return False

    def get_input_values(self):
        # Get values from all input fields
        values = {}
        for input_field in self.inputs:
            label_key = input_field.label.lower().replace(":", "").replace(" ", "_")
            values[label_key] = input_field.get_value()
        values["adaptive_mutation"] = self.adaptive_mutation_enabled
        return values
    