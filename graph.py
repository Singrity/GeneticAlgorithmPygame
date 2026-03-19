import pygame


class Graphic:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.best_fitness = []

    def draw(self, surface):
        surface.fill((255, 255, 255), self.rect)

        if len(self.best_fitness) < 2:
            return

        # Draw anti-aliased axes
        pygame.draw.aaline(surface, (0, 0, 0), (self.rect.left, self.rect.bottom), (self.rect.left, self.rect.top)) # Y-axis
        pygame.draw.aaline(surface, (0, 0, 0), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom)) # X-axis

        # Plot fitness values
        max_fitness = max(self.best_fitness)
        min_fitness = min(self.best_fitness)
        fitness_range = max_fitness - min_fitness if max_fitness != min_fitness else 1

        for i in range(1, len(self.best_fitness)):
            x1 = self.rect.left + (i - 1) / (len(self.best_fitness) - 1) * self.rect.width
            y1 = self.rect.bottom - ((self.best_fitness[i - 1] - min_fitness) / fitness_range * self.rect.height)
            x2 = self.rect.left + i / (len(self.best_fitness) - 1) * self.rect.width
            y2 = self.rect.bottom - ((self.best_fitness[i] - min_fitness) / fitness_range * self.rect.height)
            pygame.draw.aaline(surface, (255, 0, 0), (x1, y1), (x2, y2))

    def clear(self):
        self.best_fitness = []
