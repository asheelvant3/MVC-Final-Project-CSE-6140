# import BnB
from SA import run_SA
from utils import *
import approx
# import GA

import time
import os
import argparse
import random
import numpy as np

opt_cutoff = {'karate':14, 'football':94, 'jazz':158, 'email':594, 'delaunay_n10':703,'netscience':899, 'power':2203,'as-22july06':3303,'hep-th':3926,'star2':4542,'star':6902}


def main(graph, algo, cutoff, seed):
    # random.seed(seed)
    np.random.seed(seed)

    inst_name = graph.split('/')[-1].split('.')[0]

    output_dir = './output/'

    start_time = time.time()

    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if algo == 'BnB':
        pass

    if algo == 'SA':
        G, nNodes = construct_graph(graph)
        print(G.edges)
        final_solution, return_str = run_SA(G, cutoff, start_time, return_str = "", seed = seed)
        write_results(final_solution, return_str, nNodes, output_dir, inst_name, algo, cutoff, seed)

    if algo == 'approx':
        pass

    if algo == 'GA':
        pass


# Run as executable from terminal
if __name__ == '__main__':
    # parse arguments in the following format:
    # python Python/main.py -inst DATA/email.graph -alg approx -time 600 -seed 30

    parser = argparse.ArgumentParser(
        description='Run algorithm with specified parameters')
    parser.add_argument('-inst', type=str, required=True, help='graph file')
    parser.add_argument('-alg', type=str, required=True,
                        help='algorithm to use')
    parser.add_argument('-time', type=int, default=600,
                        required=False, help='runtime cutoff for algorithm')
    parser.add_argument('-seed', type=int, default=30,
                        required=False, help='random seed for algorithm')
    args = parser.parse_args()

    main(args.inst, args.alg, args.time, args.seed)
