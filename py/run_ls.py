import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-inst', type=str, required=True)
parser.add_argument('-alg', type=str, required=True)
parser.add_argument('-time', type=int, default=20, required=False)
args = parser.parse_args()

dataset_names = ["as-22july06", "email", "football", "hep-th", "jazz", 
                "karate", "netscience", "power", "star", "star2", "delaunay_n10"]
if args.alg == "ls1" or args.alg == "ls2":
    for randSeed in range(10):
        os.system(f"python py/main.py -inst {args.inst} -alg {args.alg} -time {args.time} -seed {randSeed}")
