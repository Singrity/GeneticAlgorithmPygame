class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0 # result of the fitness function, to be calculated in ga algorithm 

    def __str__(self):
        return f"Chromosome(genes={self.genes}, fitness={self.fitness})"