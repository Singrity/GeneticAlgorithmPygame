import random
from time import sleep, time

import pygame
from chromosome import Chromosome

class GA:
    def __init__(self, network, population_size=10, generations=50, mutation_rate=0.01, chromosome_length=None):
        self.network = network
        self.population_size = population_size
        self.generations = generations
        self.base_mutation_rate = mutation_rate
        self.mutation_rate = mutation_rate
        self.chromosome_length = chromosome_length if chromosome_length else network.size
        self.population = self.initialize_population()
        self.current_generation_number = 0
        # evaluate initial population and set best
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)
        self.best_fitness_ever = self.best_chromosome.fitness  # Track best fitness ever found
        self.mutation_count = 0
        self.generations_without_improvement = 0  # Track stagnation
        self.adaptive_mutation_enabled = False

    def create_random_chromosome(self):
        # Create chromosome with random nodes (duplicates ALLOWED)
        actual_length = min(self.chromosome_length, self.network.size)
        # All nodes except start and end can be visited multiple times
        available_nodes = list(range(self.network.size))
        available_nodes.remove(self.network.get_start_node().idx)
        available_nodes.remove(self.network.get_end_node().idx)
        
        # Randomly select nodes with replacement (duplicates allowed)
        middle_genes = [random.choice(available_nodes) for _ in range(actual_length - 2)]
        genes = [self.network.get_start_node().idx] + middle_genes + [self.network.get_end_node().idx]
        return Chromosome(genes) # path through the network

    def initialize_population(self):
        return[self.create_random_chromosome() for _ in range(self.population_size)]

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

    def selection(self):
        # Select the best 50% of the population based on fitness
        self.population.sort(key=lambda chromosome: chromosome.fitness)
        return self.population[:self.population_size // 2]

    def crossover(self, parent1, parent2):
        """
        Simple crossover - allows duplicates.
        """
        # Use minimum length to avoid index out of bounds
        min_len = min(len(parent1.genes), len(parent2.genes))
        if min_len <= 2:
            return Chromosome(parent1.genes[:])
        
        # Keep start and end nodes fixed
        start_node = parent1.genes[0]
        end_node = parent1.genes[-1]
        
        # Simple crossover: take first part from parent1, rest from parent2
        point = random.randint(1, min_len - 2)
        child_genes = parent1.genes[:point] + parent2.genes[point:]
        
        # Ensure start and end are correct
        child_genes[0] = start_node
        child_genes[-1] = end_node
        
        return Chromosome(child_genes)

    def mutate(self, chromosome):
        """
        Random reset mutation - replaces a gene with a random node (duplicates allowed).
        This allows the algorithm to discover that visiting the same node multiple times can have 0 cost.
        """
        chrom_len = len(chromosome.genes)
        if chrom_len <= 2:
            return chromosome

        # Get ALL nodes including start (0) and end (29) - this allows cycles!
        available_nodes = list(range(self.network.size))
        
        # Mutate ONE random gene (simple swap mutation)
        idx = random.randint(1, chrom_len - 2)
        chromosome.genes[idx] = random.choice(available_nodes)
        
        return chromosome

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
        self.evaluate_population()
        self.first_population = self.population.copy()

        # Check population diversity
        diversity = self.calculate_diversity()

        # If population too similar, inject random immigrants
        if diversity < 0.15:  # Less than 15% diversity
            self.inject_random_immigrants(immigrants_count=max(1, self.population_size // 4))

        # Get current best chromosome
        current_best = min(self.population, key=lambda chromosome: chromosome.fitness)

        # Check if we found a better solution
        if current_best.fitness < self.best_fitness_ever:
            self.best_fitness_ever = current_best.fitness
            self.best_chromosome = Chromosome(current_best.genes[:])
            self.best_chromosome.fitness = current_best.fitness
            self.generations_without_improvement = 0  # Reset counter
        else:
            self.generations_without_improvement += 1

        # Adaptive mutation: only if enabled via toggle
        if self.adaptive_mutation_enabled:
            if self.generations_without_improvement > 1000:
                multiplier = self.generations_without_improvement / 1000
                self.mutation_rate = min(0.5, self.base_mutation_rate * multiplier)
            else:
                self.mutation_rate = self.base_mutation_rate
        else:
            # Adaptive mutation disabled - use base rate only
            self.mutation_rate = self.base_mutation_rate

        selected = self.selection()

        new_population = []

        # Elitism: preserve the best chromosome in the next generation (always first)
        elite_copy = Chromosome(self.best_chromosome.genes[:])
        elite_copy.fitness = self.best_chromosome.fitness
        new_population.append(elite_copy)

        # Create population_size - 1 children (elite takes 1 spot)
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = self.crossover(parent1, parent2)

            # Apply mutation to EVERY chromosome with probability mutation_rate
            if random.random() < self.mutation_rate:
                child = self.mutate(child)
                self.mutation_count += 1

            new_population.append(child)

        # Don't use reduction here - we already have exactly population_size
        # and elite is guaranteed to be first
        self.population = new_population
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)

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
            
            
            