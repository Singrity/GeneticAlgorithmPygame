import random
from time import sleep, time

import pygame
from chromosome import Chromosome

class GA:
    def __init__(self, network, population_size=10, generations=50, mutation_rate=0.01, chromosome_length=None):
        self.network = network
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.chromosome_length = chromosome_length if chromosome_length else network.size
        self.population = self.initialize_population()
        self.current_generation_number = 0
        # evaluate initial population and set best
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)
        
    def create_random_chromosome(self):
        genes = list(range(self.network.size - 2)) # nodes in the network
        random.shuffle(genes)
        genes = [self.network.get_start_node().idx] + genes[:self.chromosome_length - 2] + [self.network.get_end_node().idx] # ensure start and end are included
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
        point = random.randint(1, self.chromosome_length - 2) # crossover point
        child_genes = parent1.genes[:point] + parent2.genes[point:]
        child_genes[0] = self.network.get_start_node().idx # ensure start is correct
        child_genes[-1] = self.network.get_end_node().idx # ensure end is correct
        return Chromosome(child_genes)
    
    def mutate(self, chromosome):
        for i in range(1, self.chromosome_length - 1): # avoid swap start and end
            swap_with = random.randint(1, self.chromosome_length - 2)
            chromosome.genes[i], chromosome.genes[swap_with] = chromosome.genes[swap_with], chromosome.genes[i]
        return chromosome

    def reduction(self, population):
        population.sort(key=lambda chromosome: chromosome.fitness)
        return population[:self.population_size] # keep only the best individuals

    def draw_best_path(self, screen):
        best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)
        for i in range(len(best_chromosome.genes) - 1):
            node_a = self.network.nodes[best_chromosome.genes[i]]
            node_b = self.network.nodes[best_chromosome.genes[i + 1]]
            pygame.draw.line(screen, (255, 0, 0), node_a.rect.center, node_b.rect.center, 5) # draw best path in red

    def draw_best_fitness(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f"Best Fitness: {self.best_chromosome.fitness}", True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))  

    def deaw_current_generation_number(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f"Generation: {self.current_generation_number}", True, (0, 0, 0))
        screen.blit(text_surface, (10, 40))
  
    def run_algorithm(self):
        # Advance a single generation each call so the main loop can control updates
        if self.current_generation_number >= self.generations:
            return

        # Evaluate current population
        self.evaluate_population()
        self.first_population = self.population.copy() # store the initial population for comparison

        selected = self.selection()

        new_population = []
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = self.crossover(parent1, parent2)
            if random.random() < self.mutation_rate:
                child = self.mutate(child)
            new_population.append(child)

        self.population = self.reduction(self.population + new_population)
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)

        # increment generation counter
        self.current_generation_number += 1
        print(self.current_generation_number - 1, self.best_chromosome.fitness)
            
            
            