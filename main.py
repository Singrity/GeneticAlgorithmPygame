import pygame
from ga import GA
from network import Network
from control_panel import ControlPanel
from button import Button

class App:
	def __init__(self, width=800, height=1000):
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()
		self.running = True
		self.network = Network(start_node_idx=0, end_node_idx=29, size=30) # create a network with 10 nodes
		self.genetic_algorithm = GA(network=self.network, population_size=20, generations=100, mutation_rate=0.3, chromosome_length=30) # initialize the genetic algorithm with the network
		self.control_panel = ControlPanel()

	

	def draw(self):

		self.screen.fill((255, 255, 255)) # clear screen with white background

		self.control_panel.draw(self.screen) # draw the control panel
		self.genetic_algorithm.draw_best_path(self.screen) # draw the best path found by the genetic algorithm
		self.genetic_algorithm.draw_best_fitness(self.screen) # draw the best fitness value on the screen
		self.genetic_algorithm.deaw_current_generation_number(self.screen) # draw the current generation number on the screen
		self.network.draw(self.screen) # draw the network


	def update(self):
		

		if self.genetic_algorithm.current_generation_number < self.genetic_algorithm.generations:
			self.genetic_algorithm.run_algorithm() # run the genetic algorithm to find the best path
		self.control_panel.update(pygame.mouse.get_pos()) # update control panel buttons based on mouse position
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
			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked_button = self.control_panel.handle_click(pygame.mouse.get_pos())
				if clicked_button == "Start":
					self.genetic_algorithm.current_generation_number = 0
				elif clicked_button == "Reset":
					self.genetic_algorithm.reset() # TODO implement reset method in GA class to reinitialize the population and reset generation number

	def run(self):
		while self.running:
			self.handle_events()
			self.update()
			self.draw()		
			

		pygame.quit()
		return


if __name__ == "__main__":
	app = App()
	app.run()