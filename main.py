import pygame
from ga import GA, ButtonTextToAlgType
from network import Network
from control_panel import ControlPanel
from button import Button, ButtonType
from input import Input


class App:
	def __init__(self, width=1500, height=900):
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((width, height))
		print(pygame.display.get_surface())
		self.clock = pygame.time.Clock()
		self.running = True
		self.is_running = False  # Flag to track if algorithm is running

		# Default GA parameters
		self.population_size = 30
		self.generations = 10000
		self.mutation_rate = 0.3
		self.network_size = 30

		self.network = Network(start_node_idx=0, end_node_idx=29, size=self.network_size) # create a network with 30 nodes
		self.genetic_algorithm = GA(network=self.network, population_size=self.population_size, generations=self.generations, mutation_rate=self.mutation_rate) # initialize the genetic algorithm with the network
		self.control_panel = ControlPanel(
			panel_pos=pygame.Vector2(width - width // 2.6, 0),
			panel_size=pygame.Vector2(width // 2.6, height),
			graphic_pos=pygame.Vector2(20, 650),
			graphic_size=pygame.Vector2(width // 3 - 40, 200),
			input_size=pygame.Vector2(150, 30),
			button_size=pygame.Vector2(150, 35),
			initial_population_size=self.population_size,
			initial_generations=self.generations,
			initial_mutation_rate=self.mutation_rate,
			initial_network_size=self.network_size
		)

	

	def draw(self):
		self.screen.fill((230, 230, 230)) # clear screen with white background

		mouse_pos = pygame.mouse.get_pos() if pygame.display.get_surface() else (0, 0)
		self.control_panel.draw(self.screen, mouse_pos) # draw the control panel
		self.genetic_algorithm.draw_population_size(self.screen) # draw the population size on the screen
		self.genetic_algorithm.draw_best_fitness(self.screen) # draw the best fitness value on the screen
		self.genetic_algorithm.draw_current_generation_number(self.screen) # draw the current generation number on the screen
		self.genetic_algorithm.draw_mutation_rate(self.screen) # draw the mutation rate
		self.genetic_algorithm.draw_stagnation_counter(self.screen) # draw stagnation counter
		self.network.draw(self.screen) # draw the network
		if self.genetic_algorithm.is_running:
			self.genetic_algorithm.draw_best_path(self.screen) # draw the best path found by the genetic algorithm


	def update(self):
		# Only update graph and run algorithm if running and not at limit
		if self.genetic_algorithm.is_running and self.genetic_algorithm.current_generation_number < self.genetic_algorithm.generations:
			self.control_panel.graphic.best_fitness.append(self.genetic_algorithm.best_chromosome.fitness)
			self.genetic_algorithm.run_algorithm()


		# Update control panel buttons based on mouse position
		mouse_pos = pygame.mouse.get_pos() if pygame.display.get_surface() else (0, 0)
		self.control_panel.update(mouse_pos)
		pygame.display.flip() # update the display

		self.clock.tick(60) # limit to 60 frames per second

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				pygame.quit()
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
					pygame.quit()
					return
				# Handle keyboard input for active input fields
			clicked_element = self.control_panel.handle_events(event)
			if type(clicked_element) == Button:
				if clicked_element.type == ButtonType.CROSOVER_TYPE or clicked_element.type == ButtonType.SELECTION_TYPE or clicked_element.type == ButtonType.MUTATION_TYPE:
					for button in self.control_panel.buttons:
						if button.type == clicked_element.type:
							button.is_active = False
					clicked_element.is_active = not clicked_element.is_active



				elif clicked_element.type == ButtonType.CONTROL:
					if clicked_element.text == "Start":
						self.genetic_algorithm.is_running = True
					elif clicked_element.text == "Apply" and not self.genetic_algorithm.is_running:
						input_values = self.control_panel.get_input_values()

						for button in self.control_panel.buttons:
							if button.type == ButtonType.SELECTION_TYPE and button.is_active:
								selection_button_type = button.text.value 								
							if button.type == ButtonType.CROSOVER_TYPE and button.is_active:
								crosover_button_type = button.text.value
							if button.type == ButtonType.MUTATION_TYPE and button.is_active:
								mutation_button_type = button.text.value
						

						if self.network.size != input_values["network_size"]:
							self.network.update_size(int(input_values["network_size"]))

						self.genetic_algorithm = GA(
							network=self.network,
							population_size=self.population_size,
							generations=self.generations,
							mutation_rate=self.mutation_rate,
							selection_type=selection_button_type,
							crossover_type=crosover_button_type,
							mutation_type=mutation_button_type
						)
						print(self.genetic_algorithm)

						if self.genetic_algorithm.population_size != int(input_values["population_size"]):
							self.genetic_algorithm.population_size = int(input_values["population_size"])
					
						if self.genetic_algorithm.generations != int(input_values["generations"]):
							self.genetic_algorithm.generations = int(input_values["generations"])

						if self.genetic_algorithm.base_mutation_rate or self.genetic_algorithm.mutation_rate != float(input_values["mutation_rate"]):
							self.genetic_algorithm.base_mutation_rate = float(input_values["mutation_rate"])
							self.genetic_algorithm.mutation_rate = float(input_values["mutation_rate"])
					
					if clicked_element.text == "Stop":
						self.genetic_algorithm.is_running = False

					if clicked_element.text == "Reset":
						self.genetic_algorithm.is_running = False
						self.control_panel.graphic.clear()
						self.network.reset()
						input_values = self.control_panel.get_input_values()
						mutation_rate = float(input_values["mutation_rate"])
						self.genetic_algorithm = GA(
							network=self.network,
							population_size=self.population_size,
							generations=self.generations,
							mutation_rate=mutation_rate,
							)
						if self.genetic_algorithm.population_size != int(input_values["population_size"]):
							self.genetic_algorithm.population_size = int(input_values["population_size"])
					
						if self.genetic_algorithm.generations != int(input_values["generations"]):
							self.genetic_algorithm.generations = int(input_values["generations"])

						if self.genetic_algorithm.base_mutation_rate or self.genetic_algorithm.mutation_rate != float(input_values["mutation_rate"]):
							self.genetic_algorithm.base_mutation_rate = float(input_values["mutation_rate"])
							self.genetic_algorithm.mutation_rate = float(input_values["mutation_rate"])

					if clicked_element.text == "Exit":
						self.running = False
						pygame.quit()
						return

			if type(clicked_element) == Input:
				for input in self.control_panel.inputs:
					input.is_active = False
				clicked_element.is_active = not clicked_element.is_active



				
	def run(self):
		while self.running:
			self.handle_events()
			if self.running:  # Check if still running after handling events
				self.update()
				self.draw()

		pygame.quit()
		return


if __name__ == "__main__":
	app = App()
	app.run()