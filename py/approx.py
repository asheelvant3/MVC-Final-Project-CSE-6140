#Maximum Degree Greedy is an approximation algorithm used to solve the Minimum 
#Vertex Cover Problem (MVC) using a greedy approach where you select the next 
#vertex with the highest degree from the set of unexplored vertices and add it 
#to the MVC. The length of our MVC set will be the Vertex Covering Number (VCN).

from collections import defaultdict
import matplotlib.pyplot as plt
import networkx
import time

class MVC:
    def __init__(self, mvc, vcn):
        self.mvc = mvc
        self.vcn = vcn

    def set_vcn(self, vcn):
        self.vcn = vcn

    def get_vcn(self):
        return self.vcn

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
        # print("graph", G.nodes())
        self.graph = G

#implement maximum degree greedy algorithm 
def max_degree_greedy(G, start, cutoff):
    degrees = dict(G.degree())  #find degrees for each vertex and store in a dictionary
    v_max_degree = max(degrees, key=degrees.get)    #find max degree in the graph

    current = time.time()
    mvc = set()

    while current - start < cutoff and degrees[v_max_degree] > 0:   
        mvc.add(v_max_degree)   #add max degree to our vertex cover

        #remove node method 
        # G.remove_node(v_max_degree)
        # degrees = dict(G.degree())
        # v_max_degree = max(degrees, key=degrees.get)

        #update degree to -1 to remove node from consideration method
        for neigh in G.neighbors(v_max_degree):
            degrees[neigh] = degrees[neigh] - 1 
        degrees[v_max_degree] = -1  #efficient way to mimic removal of a node
        v_max_degree = max(degrees, key=degrees.get)

    return str(mvc), str(len(mvc))

def solve(instance, cutoff):
    G = Graph()
    G.parse(instance, networkx.Graph())
    # print(G.graph.edges)
    start = time.time()
    # call the maximum degree greedy algorithm
    mvc, vcn = max_degree_greedy(G.graph, start, cutoff)
    # print("MVC", mvc)
    runtime = time.time() - start
    print("runtime for approximation algorithm:", str(runtime))

    #return minimum vertex cover, vertex covering number, and runtime of the algorithm
    return mvc, vcn,  str('{:f}'.format(runtime))

