from button import Button
import pygame



class ControlPanel:
    def __init__(self):
        self.buttons = []
        self.control_surface = pygame.Surface((600, 200)) # create a surface for the control panel
        self.control_surface.fill((220, 220, 220)) # light gray background

        self.add_button(Button(20, 20, 160, 40, "Start"))
        self.add_button(Button(220, 20, 160, 40, "Reset"))

    def add_button(self, button):
        self.buttons.append(button)

    def convert_mouse_pos_to_panel(self, mouse_pos):
        # Determine where the control surface is blitted on the main screen
        screen = pygame.display.get_surface()
        if screen is None:
            return (-9999, -9999)
        sw, sh = screen.get_size()
        panel_left = sw // 2 - self.control_surface.get_width() // 2
        panel_top = sh - self.control_surface.get_height()

        panel_x = mouse_pos[0] - panel_left
        panel_y = mouse_pos[1] - panel_top
        return (panel_x, panel_y)

    def draw(self, screen):
        screen.blit(self.control_surface, (screen.get_width() // 2 - self.control_surface.get_width() // 2, screen.get_height() - self.control_surface.get_height()))
        for button in self.buttons:
            button.draw(self.control_surface)

    def update(self, mouse_pos):
        converted_mouse_pos = self.convert_mouse_pos_to_panel(mouse_pos)
        for button in self.buttons:
            button.update(converted_mouse_pos)

    def handle_click(self, pos):
        converted = self.convert_mouse_pos_to_panel(pos)
        for button in self.buttons:
            if button.is_hovered(converted):
                return button.text
        return None
    