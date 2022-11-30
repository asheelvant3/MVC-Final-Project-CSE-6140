import time
import math
import random
import numpy as np
import networkx as nx
import os

def construct_graph(filename):
    G = nx.Graph()
    lines = open(filename, 'r').readlines()
    nNodes, _, _ = lines[0].split()
    nNodes = int(nNodes)
    for curr_node in range(1, nNodes+1):
        neighNodes = [int(node) for node in lines[curr_node].split()]
        for neighNode in neighNodes:
            G.add_edge(curr_node, neighNode)
    return G, nNodes

def write_results(final_solution, return_str, nNodes, output_dir, trace_filename, solution_filename):
    with open(os.path.join(output_dir, trace_filename), 'w') as file_trace:
        file_trace.write(return_str)
    with open(os.path.join(output_dir, solution_filename), 'w') as file_solution:
        file_solution.write(str(nNodes) + "\n")
        file_solution.write(','.join([str(n) for n in sorted(final_solution)]))