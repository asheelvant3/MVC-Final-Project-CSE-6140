#Maximum Degree Greedy is an approximation algorithm used to solve the Minimum 
#Vertex Cover Problem (MVC) using a greedy approach where you select the next 
#vertex with the highest degree from the set of unexplored vertices and add it 
#to the MVC. The length of our MVC set will be the Vertex Covering Number (VCN).

from collections import defaultdict
import networkx
import time

class Graph:
    def __init__(self):
        self.vertices = 0
        self.edges = 0
        self.graph = None

    def parse(self, instance, G):
        f = open(instance, "r")
        lines = f.readlines()
        vertices, edges, ign = lines[0].split()
        self.vertices = int(vertices)
        self.edges = int(edges)

        for i in range(1, self.vertices + 1):
            neigh_vertices = lines[i].split()
            for vertex in neigh_vertices:
                G.add_edge(i, int(vertex))

        self.graph = G

#implement maximum degree greedy algorithm 
def max_degree_greedy(G, start, cutoff):
    degrees = dict(G.degree())
    v_max_degree = max(degrees, key=degrees.get)

    current = time.time()
    mvc = set()

    while current - start < cutoff and degrees[v_max_degree]: 
        mvc.add(v_max_degree)

        for neigh in G.neighbors(v_max_degree):
            degrees[neigh] = degrees[neigh] - 1

        degrees[v_max_degree] = 0
        v_max_degree = max(degrees, key=degrees.get)

    return str(mvc), str(len(mvc))

def solve(instance, cutoff):
    G = Graph()
    G.parse(instance, networkx.Graph())
    print(G.graph.edges)
    start = time.time()
    mvc, vcn = max_degree_greedy(G.graph, start, cutoff)
    print("MVC", mvc)
    runtime = time.time() - start
    print("runtime for approximation algorithm:", str(runtime))

    #return minimum vertex cover, vertex covering number, and runtime of the algorithm
    return mvc, vcn,  str('{:f}'.format(runtime))
