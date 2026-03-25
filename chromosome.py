"""
Козма Богдан Григориевич
kozma.bogdan02@gmail.com
https://lms.mospolytech.ru/mod/assign/view.php?id=487354
2026
"""

class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0 # result of the fitness function, to be calculated in ga algorithm 
        self.probability = 0 # probability of selection, to be calculated in selection method of ga algorithm

    def __str__(self):
        return f"Chromosome(genes={self.genes}, fitness={self.fitness})"

    def __repr__(self):
        
        return f"Chromosome(genes={self.genes}, fitness={self.fitness})"