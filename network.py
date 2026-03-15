import random
import math
from node import Node
from edge import Edge   




class Network:
    MAX_PATH_LENGTH = 20
    def __init__(self, start_node_idx, end_node_idx, size):
        self.size = size
        self.nodes = []
        self.start_node_idx = start_node_idx
        self.end_node_idx = end_node_idx
        self.edges = []
        self.graph = []
        self.generate_network()

    def generate_network(self):
        # Create nodes arranged evenly around a circle inside the bounding box
        left = 50
        top = 50
        right = 750
        bottom = 750

        cx = (left + right) / 2
        cy = (top + bottom) / 2
        # radius: use 40% of the smaller dimension to keep nodes well inside bounds
        radius = min((right - left), (bottom - top)) * 0.4

        for i in range(self.size):
            # offset by -pi/2 so index 0 is at the top of the circle
            angle = 2 * math.pi * i / max(1, self.size) - math.pi / 2
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            if i == self.start_node_idx:
                is_start = True
                is_end = False
            elif i == self.end_node_idx:
                is_start = False
                is_end = True
            else:
                is_start = False
                is_end = False

            self.nodes.append(Node(x, y, i, is_start, is_end))

        # Create edges with random weights (undirected: create each pair once)
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == j:
                    row.append(0) # no self loops
                else:
                    # For undirected graph, populate symmetric weights in graph
                    if j > i:
                        weight = random.randint(1, 10)
                        row.append(weight)
                        # ensure graph is symmetric later
                        self.edges.append(Edge(self.nodes[i], self.nodes[j], weight))
                    else:
                        # placeholder; will be filled from the symmetric entry
                        row.append(0)
            self.graph.append(row)
        # make adjacency symmetric
        for i in range(self.size):
            for j in range(i+1, self.size):
                self.graph[j][i] = self.graph[i][j]

    def draw(self, screen):
        for edge in self.edges:
            edge.draw(screen)
        for node in self.nodes:
            node.draw(screen)


    def get_start_node(self):
        return self.nodes[self.start_node_idx]
    
    def get_end_node(self):
        return self.nodes[self.end_node_idx]
        


