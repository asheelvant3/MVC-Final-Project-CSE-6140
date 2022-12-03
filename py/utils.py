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
    return G

def write_results(VC_opt, return_str, output_dir, inst, method, cutoff, randSeed = 0):
    if method == "ls1" or method == "ls2":
        trace_filename = f"{inst}_{method}_{cutoff}_{randSeed}.trace"
        solution_filename = f"{inst}_{method}_{cutoff}_{randSeed}.sol"
    else:
        trace_filename = f"{inst}_{method}_{cutoff}.trace"
        solution_filename = f"{inst}_{method}_{cutoff}.sol"
    with open(os.path.join(output_dir, trace_filename), 'w') as file_trace:
        file_trace.write(return_str)
    with open(os.path.join(output_dir, solution_filename), 'w') as file_solution:
        file_solution.write(f"{len(VC_opt)}\n")
        file_solution.write(','.join([str(n) for n in sorted(VC_opt)]))
