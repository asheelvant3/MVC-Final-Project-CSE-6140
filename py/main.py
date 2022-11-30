import argparse
from importlib.resources import path
import os
import random
import time

import bnb
import approx
import ls1
import ls2

parser = argparse.ArgumentParser()
parser.add_argument('-inst', type=str, required=True)
parser.add_argument('-alg', type=str, required=True)
parser.add_argument('-time', type=float, default=600, required=False)
parser.add_argument('-seed', type=int, default=30, required=False)
args = parser.parse_args()

def parse_edges(instance, G):
        f = open(instance, "r")
        lines = f.readlines()
        vertices, edges, ign = lines[0].split()
        vertices = int(vertices)
        edges = int(edges)

        for i in range(1, vertices + 1):
            neigh_vertices = lines[i].split()
            for vertex in neigh_vertices:
                G.add_edge(i, int(vertex))

        return G

def solve(instance, method, cutoff, rand_seed):
    
    #graph from data instances
    graph = instance.split('/')[-1].split('.')[0]

    random.seed(rand_seed)
    
    start_time = time.time()

    #output files
    output_directory = './output/' 
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    trace = "_".join([graph, method, str(cutoff), str(rand_seed)]) + '.trace'
    ot = open(os.path.join(output_directory, trace), 'w')

    solution = "_".join([graph, method, str(cutoff), str(rand_seed)]) + '.sol'

    #execute algorithms
    if method == 'bnb':
        pass
    elif method == 'approx':
        mvc, vcn, total_time = approx.solve(instance, cutoff)

        path_sol = os.path.join(output_directory, solution)
        f = open(path_sol, 'w')
        f.write(vcn + "\n" + mvc)
        f.close()

        path_trace = os.path.join(output_directory, trace)
        f = open(path_trace, 'w')
        f.write(', '.join([total_time, vcn]))
        f.close()

    elif method == 'ls1':
        pass
    elif method == 'ls2':
        pass
    else:
        print("Invalid method entered.")

solve(args.inst, args.alg, args.time, args.seed)
