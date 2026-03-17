import random
from time import sleep, time
from network import Network
import pygame
from chromosome import Chromosome

class GA:
    def __init__(self,
                network: Network,
                population_size: int = 10,
                generations: int = 50,
                mutation_rate: float = 0.01,
    ):
        self.network = network
        self.population_size = population_size
        self.generations = generations
        self.base_mutation_rate = mutation_rate
        self.mutation_rate = mutation_rate
        self.chromosome_length = self.network.size
        self.current_generation_number = 0

        self.population = self.initialize_population()

        # evaluate initial population and set best
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)
        #self.best_fitness_ever = self.best_chromosome.fitness  # Track best fitness ever found
        #self.mutation_count = 0
        self.generations_without_improvement = 0  # Track stagnation
        #self.adaptive_mutation_enabled = False

        self.base_probability = 0.5  # Base probability for selection methods

    def create_random_chromosome(self):
        actual_length = min(self.chromosome_length, self.network.size)
        available_nodes = list(range(self.network.size))

        start_node = self.network.start_node_idx
        end_node = self.network.end_node_idx
        
        genes = [start_node] + [random.choice(available_nodes) for _ in range(actual_length - 2)] + [end_node]
        # Randomly select nodes with replacement (duplicates allowed)
        return Chromosome(genes) # path through the network

    def initialize_population(self):
        return [self.create_random_chromosome() for _ in range(self.population_size)]

    def fitness(self, chromosome):
        total_distance = 0
        for i in range(len(chromosome.genes) - 1):
            node_a = chromosome.genes[i]
            node_b = chromosome.genes[i + 1]
            total_distance += self.network.graph[node_a][node_b]
        chromosome.fitness = total_distance
        return total_distance

    def evaluate_population(self):
        for chromosome in self.population:
            self.fitness(chromosome)

    ### Selection, Crossover, Mutation methods ###

    def proportional_selection(self, current_population, current_best_fitness):
        for chromosome in current_population:
            chromosome.probability = 1 / (1 + chromosome.fitness - current_best_fitness)
        
        parents = [chromosome for chromosome in current_population if random.random() < chromosome.probability]

        return parents

    def tournament_selection(self, current_population, tournament_size=3):
        for chromosome in current_population:
            chromosome.probability = 1 - (1 - self.base_probability) ** tournament_size
        
        parents = [chromosome for chromosome in current_population if random.random() < chromosome.probability]

        return parents

    def rang_selection(self, current_population):
        """population_should_be_sorted_by_fitness"""
        for rang, chromosome in enumerate(current_population):
            chromosome.probability = 2 * (self.population_size - rang + 1) / (self.population_size * (self.population_size + 1))
        
        parents = [chromosome for chromosome in current_population if random.random() < chromosome.probability]
        return parents

    def one_point_crossover(self, current_population):
        parent1 = random.choice(current_population)
        parent2 = random.choice(current_population)
        
        if parent1 == parent2:
            return self.one_point_crossover(current_population)  # Ensure different parents
        
        crossover_point = random.randint(1, self.chromosome_length - 2)

        child_genes = [parent1.genes[self.network.start_node_idx]] + parent1.genes[self.network.start_node_idx:crossover_point] + parent2.genes[crossover_point:self.network.end_node_idx] + [parent1.genes[self.network.end_node_idx]] 

        return Chromosome(child_genes)

    def two_point_crossover(self, current_population):
        parent1 = random.choice(current_population)
        parent2 = random.choice(current_population)
        
        if parent1 == parent2:
            return self.two_point_crossover(current_population)  # Ensure different parents
        
        point1 = random.randint(0, self.chromosome_length - 2)
        point2 = random.randint(point1 + 1, self.chromosome_length - 1)
        
        child_genes = parent1.genes[:point1] + parent2.genes[point1:point2] + parent1.genes[point2:]

        return Chromosome(child_genes)
    
    def uniform_crossover(self, current_population):
        parent1 = random.choice(current_population)
        parent2 = random.choice(current_population)
        
        if parent1 == parent2:
            return self.uniform_crossover(current_population)  # Ensure different parents
        
        child_genes = []
        for gene1, gene2 in zip(parent1.genes, parent2.genes):
            child_genes.append(gene1 if random.random() < 0.5 else gene2)

        return Chromosome(child_genes)

    def bit_flip_mutation(self, children):
        nodes = list(range(self.network.size))
        for i in range(1, len(children.genes) - 1):  # Skip start and end nodes
            children.genes[i] = random.choice(nodes)
        return children

    def gaussian_mutation(self, children ,mean=0, stddev=1):
        for i in range(len(children.genes)):
            mutation_value = int(random.gauss(mean, stddev))
            children.genes[i] = (children.genes[i] + mutation_value) % self.network.size
        return children


    def reduction(self, population):
        population.sort(key=lambda chromosome: chromosome.fitness)
        return population[:self.population_size] # keep only the best individuals

    def draw_best_path(self, screen):
        best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)
        font = pygame.font.SysFont('Arial', 20)

        for i in range(len(best_chromosome.genes) - 1):
            node_a = self.network.nodes[best_chromosome.genes[i]]
            node_b = self.network.nodes[best_chromosome.genes[i + 1]]

            # Draw anti-aliased edge line
            pygame.draw.aaline(screen, (255, 0, 0), node_a.rect.center, node_b.rect.center, 5)

            # Get weight from graph
            weight = self.network.graph[best_chromosome.genes[i]][best_chromosome.genes[i + 1]]

            # Calculate midpoint for weight text
            mid_x = (node_a.rect.center[0] + node_b.rect.center[0]) // 2
            mid_y = (node_a.rect.center[1] + node_b.rect.center[1]) // 2 - 20

            # Render weight text
            text_surface = font.render(str(weight), True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(mid_x, mid_y))
            screen.blit(text_surface, text_rect)

    def draw_best_fitness(self, surface):
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f"Best Fitness: {self.best_chromosome.fitness}", True, (0, 0, 0))
        surface.blit(text_surface, (10, 10))

    def draw_population_size(self, surface):
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f"Population: {self.population_size}", True, (0, 0, 0))
        surface.blit(text_surface, (10, 70))

    def draw_current_generation_number(self, surface):
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f"Generation: {self.current_generation_number}", True, (0, 0, 0))
        surface.blit(text_surface, (10, 40))

    def draw_mutation_rate(self, surface):
        font = pygame.font.SysFont('Arial', 24)
        # Show if adaptive mutation is active
        if self.mutation_rate > self.base_mutation_rate:
            text_surface = font.render(f"Mutation Rate: {self.mutation_rate:.2f} (ADAPTIVE!)", True, (255, 0, 0))
        else:
            text_surface = font.render(f"Mutation Rate: {self.mutation_rate:.2f}", True, (0, 0, 0))
        surface.blit(text_surface, (10, 100))

    def draw_stagnation_counter(self, surface):
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render(f"No improvement: {self.generations_without_improvement}/1000 gens", True, (100, 100, 100))
        surface.blit(text_surface, (10, 130))
    
    def draw_mutation_count(self, surface: pygame.surface.Surface):
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f"Mutations: {self.mutation_count}", True, (0, 0, 0))
        surface.blit(text_surface, (10, 400))

    def reset(self):
        self.network.reset()
        self.population = self.initialize_population()
        self.current_generation_number = 0
        self.mutation_count = 0
        self.generations_without_improvement = 0
        self.mutation_rate = self.base_mutation_rate
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)
        self.best_fitness_ever = self.best_chromosome.fitness

    def run_algorithm(self):
        # Advance a single generation each call so the main loop can control updates
        if self.current_generation_number >= self.generations:
            return

        # Evaluate current population
        #self.evaluate_population()
        #self.first_population = self.population.copy()

        # Check population diversity
        #diversity = self.calculate_diversity()

        # If population too similar, inject random immigrants
#        if diversity < 0.15:  # Less than 15% diversity
 #           self.inject_random_immigrants(immigrants_count=max(1, self.population_size // 4))

        # Get current best chromosome
  #      current_best = min(self.population, key=lambda chromosome: chromosome.fitness)

        # Check if we found a better solution
  #      if current_best.fitness < self.best_fitness_ever:
 #           self.best_fitness_ever = current_best.fitness
  #          self.best_chromosome = Chromosome(current_best.genes[:])
  #          self.best_chromosome.fitness = current_best.fitness
  #          self.generations_without_improvement = 0  # Reset counter
  #      else:
  #          self.generations_without_improvement += 1
##
        # Adaptive mutation: only if enabled via toggle
        # if self.adaptive_mutation_enabled:
        #     if self.generations_without_improvement > 1000:
        #         multiplier = self.generations_without_improvement / 1000
        #         self.mutation_rate = min(0.5, self.base_mutation_rate * multiplier)
        #     else:
        #         self.mutation_rate = self.base_mutation_rate
        # else:
        #     # Adaptive mutation disabled - use base rate only
        #     self.mutation_rate = self.base_mutation_rate

        new_population = []
        selected_parrents = self.proportional_selection(self.population, self.best_chromosome.fitness)

        while len(new_population) < self.population_size:
            if len(selected_parrents) < 2:
                selected_parrents = self.proportional_selection(self.population, self.best_chromosome.fitness)
                continue
            child = self.one_point_crossover(selected_parrents)
            if random.random() < self.mutation_rate:
                child = self.bit_flip_mutation(child)
            new_population.append(child)

        
        self.population = new_population
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)


        # new_population = []

        # # Elitism: preserve the best chromosome in the next generation (always first)
        # elite_copy = Chromosome(self.best_chromosome.genes[:])
        # elite_copy.fitness = self.best_chromosome.fitness
        # new_population.append(elite_copy)

        # # Create population_size - 1 children (elite takes 1 spot)
        # while len(new_population) < self.population_size:
        #     parent1, parent2 = random.sample(selected, 2)
        #     child = self.crossover(parent1, parent2)

        #     # Apply mutation to EVERY chromosome with probability mutation_rate
        #     if random.random() < self.mutation_rate:
        #         child = self.mutate(child)
        #         self.mutation_count += 1

        #     new_population.append(child)

        # Don't use reduction here - we already have exactly population_size
        # and elite is guaranteed to be first
        #self.population = new_population
        #self.evaluate_population()
        #self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)

        # increment generation counter
        self.current_generation_number += 1
        print(self.current_generation_number - 1, self.best_chromosome)

    def calculate_diversity(self):
        """
        Calculate population diversity as ratio of unique chromosomes.
        Returns value between 0 (all identical) and 1 (all unique).
        """
        if len(self.population) <= 1:
            return 1.0
        
        # Convert chromosomes to tuples for comparison
        unique_genes = set()
        for chromosome in self.population:
            gene_tuple = tuple(chromosome.genes)
            unique_genes.add(gene_tuple)
        
        return len(unique_genes) / len(self.population)

    def inject_random_immigrants(self, immigrants_count):
        """
        Replace worst chromosomes with random ones to restore diversity.
        This is a standard GA technique to escape local minima.
        """
        # Sort by fitness (worst first)
        self.population.sort(key=lambda chromosome: chromosome.fitness, reverse=True)
        
        # Replace worst chromosomes with random ones (keep elite!)
        for i in range(min(immigrants_count, self.population_size - 1)):
            self.population[i] = self.create_random_chromosome()
        
        print(f"  → Injected {immigrants_count} immigrants (diversity={self.calculate_diversity():.2f})")
            
            
pygame.font.init()

network = Network(
    0, 1, 20
)
ga = GA(
    network=network
)


print(ga.population)

