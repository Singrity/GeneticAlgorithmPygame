from button import Button, ButtonType
from input import Input
from graph import Graphic
from ga import SelectionType, CrossoverType, MutationType, ALG_TO_BUTTON_TEXT
import pygame

"""
Козма Богдан Григориевич
kozma.bogdan02@gmail.com
https://lms.mospolytech.ru/mod/assign/view.php?id=487354
2026
"""

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

        
        
        self.button_size = button_size
        self.panel_pos = panel_pos
        self.panel_size = panel_size
        self.input_size = input_size
        self.initial_population_size = initial_population_size
        self.initial_generations = initial_generations
        self.initial_mutation_rate = initial_mutation_rate
        self.initial_network_size = initial_network_size

        

        
        
        # Create the control surface
        self.control_surface = pygame.Surface((int(panel_size.x), int(panel_size.y)))
        
        # Initialize lists for buttons and inputs
        self.buttons = []
        self.inputs = []
        
        # Padding for layout
        self.padding_x = 20
        self.padding_y = 20
        self.spacing = 30

        self.control_buttons_pos = pygame.Vector2(self.panel_pos.x + self.padding_x, self.panel_pos.y + self.padding_y)
        self.alg_type_buttons_pos = pygame.Vector2(self.panel_pos.x + self.padding_x, self.panel_pos.y + self.padding_y + 500)
        
        
        # # Initialize graphic (fitness graph)
        self.graphic = Graphic(graphic_pos.x, graphic_pos.y, int(graphic_size.x), int(graphic_size.y))


        self.type_button_size = pygame.Vector2(130, 25)
     

        self.setup_control_panel()


    def setup_control_panel(self):
        control_button_names = [
                [
                    ("Start", False, ButtonType.CONTROL),
                    ("Stop", False, ButtonType.CONTROL),
                    ("Reset", False, ButtonType.CONTROL),
                ],
                [
                    ("Apply", False, ButtonType.CONTROL),
                    ("Next", False, ButtonType.CONTROL),
                    ("Exit", False, ButtonType.CONTROL),
                ],
                [
                    ("Cicle", True, ButtonType.RUN_TYPE),
                    ("Step", False, ButtonType.RUN_TYPE),
                    
                ]
            ]
        type_button_names = [
                [
                    (ALG_TO_BUTTON_TEXT[SelectionType.PROPORTIONAL], True, ButtonType.SELECTION_TYPE),
                    (ALG_TO_BUTTON_TEXT[SelectionType.TOURNAMENT], False, ButtonType.SELECTION_TYPE),
                    (ALG_TO_BUTTON_TEXT[SelectionType.RANG], False, ButtonType.SELECTION_TYPE)
                ],
                [
                    (ALG_TO_BUTTON_TEXT[CrossoverType.ONE_POINT], True, ButtonType.CROSOVER_TYPE),
                    (ALG_TO_BUTTON_TEXT[CrossoverType.TWO_POINT], False, ButtonType.CROSOVER_TYPE),
                    (ALG_TO_BUTTON_TEXT[CrossoverType.UNIFORM], False, ButtonType.CROSOVER_TYPE)
                ],
                [
                    (ALG_TO_BUTTON_TEXT[MutationType.BIT_FLIP], True, ButtonType.MUTATION_TYPE),
                    (ALG_TO_BUTTON_TEXT[MutationType.GAUSSIAN], False, ButtonType.MUTATION_TYPE)
                ]
            ]
        inputs = [[("population_size", self.initial_population_size, 5, 1000, True), ("generations", self.initial_generations, 1, 10000000, True), ("mutation_rate", self.initial_mutation_rate, 0, 1, False), ("network_size", self.initial_network_size, 1, 100, True)]]

        

        current_control_button_y = self.panel_pos.y + self.padding_y + 300
        for row in control_button_names:
            for i, (name, is_active, b_type) in enumerate(row):
                button = Button(
                    text=name,
                    x=self.padding_x + i * (self.button_size.x + self.spacing),
                    y=current_control_button_y,
                    is_active=is_active,
                    btype=b_type
                )
                self.buttons.append(button)
            current_control_button_y += self.button_size.y + self.spacing

        # Add type buttons
        current_type_button_y = self.panel_pos.y + self.padding_y + 480
        for row in type_button_names:
            for i, (name, is_active, b_type) in enumerate(row):
                button = Button(
                    text=name,
                    x=int(self.padding_x + i * (self.type_button_size.x + self.spacing)),
                    y=current_type_button_y,
                    is_active=is_active,
                    btype=b_type
                )
                self.buttons.append(button)
            current_type_button_y += self.type_button_size.y + self.spacing

        current_input_y = self.panel_pos.y + self.padding_y + 70
        for row in inputs:
            for i, (name, default_value, min, max, is_integer) in enumerate(row):
                input = Input(
                    width=self.input_size.x,
                    height=self.input_size.y,
                    label=name,
                    value=default_value,
                    x=self.padding_x,
                    y=current_input_y,
                    min_value=min,
                    max_value=max,
                    is_integer=is_integer
                )
                self.inputs.append(input)
                current_input_y += self.input_size.y + self.spacing

        for bid, button in enumerate(self.buttons):
            button.bid += bid



    def draw(self, screen, mouse_pos=None):
        # Draw the control panel surface at the right side of the screen
        screen.blit(self.control_surface, (self.panel_pos.x, self.panel_pos.y))

        self.control_surface.fill((220, 220, 220))  # light gray background

        title_font = pygame.font.SysFont('Arial', 24, bold=True)
        title = title_font.render("Settings", True, (50, 50, 50))
        title_rect = title.get_rect(centerx=int(self.panel_size.x) // 2, top=30)

        author_data_font = pygame.font.SysFont('Arial', 16)
        author_data_name = author_data_font.render("Козма Богдан Григориевич", True, (50, 50, 50))

        author_student_email = author_data_font.render("kozma.bogdan02@gmail.com", True, (50, 50, 50))
        author_student_course_link = author_data_font.render("lms.mospolytech.ru/course/view.php?id=14927", True, (50, 50, 50))
        author_student_year = author_data_font.render("2026", True, (50, 50, 50))
        
        author_data_rect = author_data_name.get_rect(x=250, y=100 + 50)
        author_student_email_rect = author_student_email.get_rect(x=250, y=116 + 50)
        author_student_course_link_rect = author_student_course_link.get_rect(x=250, y=132 + 50)
        author_student_year_rect = author_student_year.get_rect(x=250, y=148 + 50)


        self.control_surface.blit(author_data_name, author_data_rect)
        self.control_surface.blit(author_student_email, author_student_email_rect)
        self.control_surface.blit(author_student_course_link, author_student_course_link_rect)
        self.control_surface.blit(author_student_year, author_student_year_rect)
        self.control_surface.blit(title, title_rect)

        # Draw all input fields
        for input_field in self.inputs:
            input_field.draw(self.control_surface)

        # Draw all buttons
        for button in self.buttons:
            button.draw(self.control_surface)
        
        # separator line
        #pygame.draw.line(self.control_surface, (255, 255, 255), (0, 480), (self.panel_size.x, 480), 1)
        pygame.draw.line(self.control_surface, (255, 255, 255), (0, 645), (self.panel_size.x, 645), 1)

        
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


    def get_clicked_element(self, pos) -> Button | Input | None:
        # Convert to panel coordinates
        converted_mouse_pos_to_control_suraface = (pos[0] - self.panel_pos.x, pos[1] - self.panel_pos.y)

        # Check buttons
        for button in self.buttons:
            if button.is_hovered(converted_mouse_pos_to_control_suraface):
                for input_field in self.inputs:
                    input_field.deactivate()
                return button
        
        for input in self.inputs:
            if input.is_clicked(converted_mouse_pos_to_control_suraface):
                return input

            
    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            for input in self.inputs:
                input.handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos() if pygame.display.get_surface() else (0, 0)
            clicked_element = self.get_clicked_element(mouse_pos)
            return clicked_element


    # def handle_key(self, event):
    #     # Pass keyboard events to active input fields
    #     for input_field in self.inputs:
    #         if input_field.is_active:
    #             if input_field.handle_key(event):
    #                 return True
    #     return False

    def get_input_values(self):
        # Get values from all input fields
        values = {}
        for input_field in self.inputs:
            label_key = input_field.label.lower().replace(":", "").replace(" ", "_")
            values[label_key] = input_field.get_value()
        #values["adaptive_mutation"] = self.adaptive_mutation_enabled
        return values
    