import argparse
from importlib.resources import path
import os
import numpy as np
import time

import bnb
import approx
import ls1
from ls2 import SimulatedAnnealing
from utils import construct_graph, write_results

parser = argparse.ArgumentParser()
parser.add_argument('-inst', type=str, required=True)
parser.add_argument('-alg', type=str, required=True)
parser.add_argument('-time', type=int, default=600, required=False)
parser.add_argument('-seed', type=int, default=30, required=False)
args = parser.parse_args()

def solve(instance, method, cutoff, rand_seed):
    
    #graph from data instances
    instance_name = instance.split('/')[-1].split('.')[0]

    np.random.seed(rand_seed)
    
    start_time = time.time()

    #output files
    output_directory = './output/' 
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    #execute algorithms
    if method == 'bnb':
        g = construct_graph(instance)
        Sol, Track = bnb.BranchBound(g, cutoff)
        write_results(Sol, Track, output_directory, instance_name, method, cutoff, rand_seed)
    elif method == 'approx':
        mvc, vcn, total_time = approx.solve(instance, cutoff)
        c = str(cutoff)
        s = str(rand_seed)

        path_sol = os.path.join(output_directory, "_".join([instance_name, method, c, s]) + '.sol')
        f = open(path_sol, 'w')
        f.write(vcn + "\n" + mvc)
        f.close()

        path_trace = os.path.join(output_directory, "_".join([instance_name, method, c, s]) + '.trace')
        f = open(path_trace, 'w')
        f.write(', '.join([total_time, vcn]))
        f.close()

    elif method == 'ls1':
        ls1.run(instance, cutoff, rand_seed)
    elif method == 'ls2':
        G = construct_graph(instance)
        VC_opt, return_str = SimulatedAnnealing(G, cutoff, start_time, return_str = "", seed = rand_seed)
        write_results(VC_opt, return_str, output_directory, instance_name, method, cutoff, rand_seed)
    else:
        print("Invalid method entered. Please enter one of [bnb|approx|ls1|ls2].")

solve(args.inst, args.alg, args.time, args.seed)