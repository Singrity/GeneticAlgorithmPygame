import pygame
from ga import GA
from network import Network
from control_panel import ControlPanel
from button import Button

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
			graphic_pos=pygame.Vector2(20, 500),
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
				if self.control_panel.handle_key(event):
					continue
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos() if pygame.display.get_surface() else (0, 0)
				clicked_button = self.control_panel.handle_click(mouse_pos)
				if clicked_button == "Start":

					#self.control_panel.graphic.best_fitness = []
					self.genetic_algorithm.is_running = True

				elif clicked_button == "Apply" and not self.genetic_algorithm.is_running:

					input_values = self.control_panel.get_input_values()
					if self.network.size != input_values["network_size"]:
						self.network.update_size(int(input_values["network_size"]))
						
					self.genetic_algorithm = GA(
						network=self.network,
						population_size=self.population_size,
						generations=self.generations,
						mutation_rate=float(input_values["mutation_rate"]),
						)
					# Update network size if changed
					
					if self.genetic_algorithm.population_size != int(input_values["population_size"]):
						self.genetic_algorithm.population_size = int(input_values["population_size"])
					
					if self.genetic_algorithm.generations != int(input_values["generations"]):
						self.genetic_algorithm.generations = int(input_values["generations"])

					if self.genetic_algorithm.base_mutation_rate or self.genetic_algorithm.mutation_rate != float(input_values["mutation_rate"]):
						self.genetic_algorithm.base_mutation_rate = float(input_values["mutation_rate"])
						self.genetic_algorithm.mutation_rate = float(input_values["mutation_rate"])
					
					


				elif clicked_button == "Stop":
					# Clear graph and reset everything
					self.genetic_algorithm.is_running = False
					#self.network.reset()
					# Get current values from inputs
					#input_values = self.control_panel.get_input_values()
					#mutation_rate = float(input_values["mutation_rate"])
					#adaptive_mutation = input_values["adaptive_mutation"]
					#self.genetic_algorithm = GA(
						#network=self.network,
						#population_size=self.population_size,
						#generations=self.generations,
						#mutation_rate=mutation_rate,
						#)
					#self.genetic_algorithm.adaptive_mutation_enabled = adaptive_mutation
				elif clicked_button == "Reset":
					self.control_panel.graphic.clear()
					self.genetic_algorithm.is_running = False
					self.network.reset()
					# Get current values from inputs
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
					
				elif clicked_button == "Clear":
					self.control_panel.graphic.clear()
				elif clicked_button == "Exit":
					self.running = False
					pygame.quit()
					return

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