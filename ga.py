import random
from time import sleep, time
from network import Network
import pygame
from chromosome import Chromosome
from enum import Enum, auto

class SelectionType(Enum):
    PROPORTIONAL = auto()
    TOURNAMENT = auto()
    RANG = auto()

class CrossoverType(Enum):
    ONE_POINT = auto()
    TWO_POINT = auto()
    UNIFORM = auto()

class MutationType(Enum):
    BIT_FLIP = auto()
    GAUSSIAN = auto()

class ButtonTextToAlgType(Enum):
    prop = SelectionType.PROPORTIONAL
    tour = SelectionType.TOURNAMENT
    rang = SelectionType.RANG
    one = CrossoverType.ONE_POINT
    two = CrossoverType.TWO_POINT
    uni = CrossoverType.UNIFORM
    bit = MutationType.BIT_FLIP
    gaus = MutationType.GAUSSIAN





class GA:
    def __init__(self,
                network: Network,
                population_size: int = 10,
                generations: int = 50,
                mutation_rate: float = 0.01,
                selection_type: SelectionType = SelectionType.PROPORTIONAL,
                crossover_type: CrossoverType = CrossoverType.ONE_POINT,
                mutation_type: MutationType = MutationType.BIT_FLIP
    ):

        self.selection_type = selection_type
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type       

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

        self.is_running = False

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
        fitness_values = [chromosome.fitness for chromosome in current_population]
        min_fitness = min(fitness_values)
        max_fitness = max(fitness_values)

        fitness_range = max_fitness - min_fitness if max_fitness != min_fitness else 1

        for chromosome in current_population:
            normalized_fitness = (chromosome.fitness - min_fitness) / fitness_range
            chromosome.probability = 1.0 - (0.8 * normalized_fitness)
        
        parents = [chromosome for chromosome in current_population if random.random() < chromosome.probability]

        while len(parents) < 2:
            random_chromosome = random.choice(current_population)
            if random_chromosome not in parents:
                parents.append(random_chromosome)

        return parents

    def tournament_selection(self, current_population, tournament_size=5):


        parents = []

        while len(parents) < self.population_size:
            tournament = random.sample(current_population, min(tournament_size, len(current_population)))

            winner = min(tournament, key=lambda chromosome: chromosome.fitness)

            parents.append(winner)

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

        child_genes = (
                parent1.genes[:crossover_point] +  # От начала до точки кроссовера
                parent2.genes[crossover_point:]     # От точки кроссовера до конца
            )

        return Chromosome(child_genes)

    def two_point_crossover(self, current_population):
        parent1 = random.choice(current_population)
        parent2 = random.choice(current_population)
        
        if parent1 == parent2:
            return self.two_point_crossover(current_population)  # Ensure different parents
        

        point1 = random.randint(1, self.chromosome_length - 2)
        point2 = random.randint(1, self.chromosome_length - 2)

        while point1 == point2:
            point1 = random.randint(1, self.chromosome_length - 2)
            point2 = random.randint(1, self.chromosome_length - 2)

        
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
        for i in range(1, len(children.genes) - 1):
            mutation_value = int(random.gauss(mean, stddev))
            children.genes[i] = (children.genes[i] + mutation_value) % self.network.size
        return children


    def reduction(self, population):
        population.sort(key=lambda chromosome: chromosome.fitness)
        return population[:self.population_size] # keep only the best individuals

    def draw_best_path(self, screen):
        best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)
        font = pygame.font.SysFont('Arial', 20)
        same_node_count = 0
        for i in range(len(best_chromosome.genes) - 1):
            node_a = self.network.nodes[best_chromosome.genes[i]]
            node_b = self.network.nodes[best_chromosome.genes[i + 1]]
            
            if node_a == node_b:
                same_node_count += 1
                for i in range(same_node_count):
                    radius = node_a.rect.width + 5 + i * 3
                    pygame.draw.circle(screen, (100, 100, 100), node_a.rect.center, radius, 2)
            else:
                same_node_count = 0
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

        self.is_running = True
        # Advance a single generation each call so the main loop can control updates
        if self.current_generation_number >= self.generations:
            self.is_running = False
            return


        new_population = []

        match self.selection_type:
            case SelectionType.PROPORTIONAL:
                selected_parrents = self.proportional_selection(self.population, self.best_chromosome.fitness)
            case SelectionType.TOURNAMENT:
                selected_parrents = self.tournament_selection(self.population, self.best_chromosome.fitness)
            case SelectionType.RANG:
                selected_parrents = self.rang_selection(self.population)
        

        best_chromosome = min(self.population, key=lambda chrom: chrom.fitness)
        new_population.append(best_chromosome)

        while len(new_population) < self.population_size:
            if len(selected_parrents) < 2:
                match self.selection_type:
                    case SelectionType.PROPORTIONAL:
                        selected_parrents = self.proportional_selection(self.population, self.best_chromosome.fitness)
                    case SelectionType.TOURNAMENT:
                        selected_parrents = self.tournament_selection(self.population, self.best_chromosome.fitness)
                    case SelectionType.RANG:
                        selected_parrents = self.rang_selection(self.population)
                continue
            match self.crossover_type:
                case CrossoverType.ONE_POINT:
                    child = self.one_point_crossover(selected_parrents)
                case CrossoverType.TWO_POINT:
                    child = self.two_point_crossover(selected_parrents)
                case CrossoverType.UNIFORM:
                    child = self.uniform_crossover(selected_parrents)
            if random.random() < self.mutation_rate:
                match self.mutation_type:
                    case MutationType.BIT_FLIP:
                        child = self.bit_flip_mutation(child)
                    case MutationType.GAUSSIAN:
                        child = self.gaussian_mutation(child)
            new_population.append(child)

        
        self.population = new_population[:self.population_size]
        self.evaluate_population()
        self.best_chromosome = min(self.population, key=lambda chromosome: chromosome.fitness)


       
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


    def __repr__(self):
        return f"algtype: {self.selection_type, self.crossover_type, self.mutation_type}"
            
            

   