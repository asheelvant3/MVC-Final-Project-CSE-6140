import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-alg', type=str, required=True)
parser.add_argument('-time', type=int, default=20, required=False)
args = parser.parse_args()

data_dir = "DATA"
# dataset_names = ["as-22july06", "email", "football", "hep-th", "jazz", 
#                 "karate", "netscience", "power", "star", "star2", "delaunay_n10"]
# dataset_names = ["as-22july06", "email", "football", "hep-th", "jazz", 
#                 "karate", "netscience", "delaunay_n10"]
dataset_names = ["star", "star2", "power"]
if args.alg == "ls1" or args.alg == "ls2":
    for dataset in dataset_names:
        print(dataset)
        data_path = f"{data_dir}/{dataset}.graph"
        for randSeed in range(10):
            os.system(f"python py/main.py -inst {data_path} -alg {args.alg} -time {args.time} -seed {randSeed}")
