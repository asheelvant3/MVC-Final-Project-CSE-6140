import argparse
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

def main(instance, method, cutoff, rand_seed):
    
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

    if method == 'bnb':
        pass
    elif method == 'approx':
        pass
    elif method == 'ls1':
        pass
    elif method == 'ls2':
        pass
    else:
        print("Invalid method entered.")


main(args.inst, args.alg, args.time, args.seed)
