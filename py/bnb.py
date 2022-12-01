import argparse
import networkx as nx
import time
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
    print(G.edges())
    return G, nNodes

def BranchBound(Graph, Cutoff):
    StartTime = time.time()
    backtrack = False #set to True when we reach a pruned node or leaf
    BestVC = [] #Best Vertex Cover so far
    BestVC_Size = Graph.number_of_nodes() #Upper Bound = Size of best Vertex Cover so far ; Initially = total number of nodes
    VC = [] #Vertex Cover, contains (node, in VC? 0/1)
    F = [] #Frontier Stack, contains (node, in VC? 0/1, (parent node, in VC? 0/1)) 
    SubG = Graph.copy() #Current sub problem; Initially = full graph

    #[Choose] Pick the candidate node with the highest degree
    candidate_node = max(SubG.degree, key = lambda x: x[1])[0]

    #[Expand] Add 2 branches to frontier: one with candidate node in VC, one without candidate node in VC
    F.extend([(candidate_node, 0, (None, None)), (candidate_node, 1, (None, None))]) 

    track_sols = []  #Tracking all solutions, contains (|VC solution|, time taken to find solution)

    TimeSoFar = 0
    while F and TimeSoFar < Cutoff:
        (cand, in_VC, parent) = F.pop() 
        
        if in_VC: #if we add cand to VC, we can delete it from our subproblem
            SubG.remove_node(cand)
        else: #if we don't add cand to VC, we have to add all of cand's neighbours to VC
            for node in list(SubG.neighbors(cand)):
                VC.append((node, 1))
                SubG.remove_node(node)

        VC.append((cand, in_VC))
        VC_Size = sum([x[1] for x in VC])

        #[Check 1: reached a feasible (complete) solution]
        if SubG.number_of_edges() == 0:
            if VC_Size < BestVC_Size:
                BestVC = VC.copy()
                BestVC_Size = VC_Size
                print("reached a solution: ", VC_Size)
                track_sols.append((VC_Size, time.time()-StartTime)) #can directly write to trace file here 
            backtrack = True 

        #reached a partial solution 
        else:
            #[Check 3a: is not dead end and LB > UB, prune the subtree]
            if LowerBound(SubG) + VC_Size >= BestVC_Size:
                backtrack = True
            #[Check 3b: is not dead end and LB < UB, add to frontier]
            else:
                #[Choose] new candidate is the maximum degree node of our current subproblem
                new_cand = max(SubG.degree, key = lambda x: x[1])    
                #[Expand] add two branches to frontier, one w new_cand in VC, one w/o             
                F.extend([(new_cand[0], 0, (cand, in_VC)), (new_cand[0], 1, (cand, in_VC))])

        #To climb back up the tree and check the remaining branches
        if backtrack and F:
            if F[-1][2] not in VC: #reached root 
                VC.clear()
                SubG = Graph.copy()
            else:
                Parent_VC_id = VC.index(F[-1][2]) + 1
                VC_discard = VC[-(len(VC) - Parent_VC_id):] 
                VC = VC[:Parent_VC_id] #VC brought back to a previous state

                #Reconstructing the subproblem to a previous state
                for y in VC_discard:
                    SubG.add_node(y[0])
                    for nbr in Graph.neighbors(y[0]):
                        if (nbr in SubG.nodes()) and (nbr not in [x[0] for x in VC]):
                            SubG.add_edge(nbr, y[0])

        TimeSoFar = time.time() - StartTime
        if  TimeSoFar > Cutoff:
            print('Cutoff time reached')

    # print ([x[0] for x in BestVC if x[1] == 1])
    # print(track_sols)
    return [x[0] for x in BestVC if x[1] == 1], track_sols

#ESTIMATE LOWERBOUND
def LowerBound(graph):
    #maximum matching
    lb = len(nx.max_weight_matching(graph))/2 
    #maximal matching
    # lb = 0 
    # tempG = graph.copy()
    # while list(tempG.edges()):
    #     edge = list(tempG.edges()).pop()
    #     tempG.remove_nodes_from([edge[0],edge[1]])
    #     lb = lb + 1

    return lb    

##################################################################
# MAIN BODY OF CODE

def main(inputfile, output_dir, cutoff, randSeed):
    #READ INPUT FILE INTO GRAPH
    g, _ = construct_graph(inputfile)

    Sol_VC, times = BranchBound(g, cutoff)

    # WRITE SOLUTION AND TRACE FILES TO "*.SOL" AND '*.TRACE"  RESPECTIVELY
    inputdir, inputfile = os.path.split(args.inst)

    #WRITE SOL FILES
    with open('.\Output\\' + inputfile.split('.')[0] + '_BnB_'+str(cutoff)+'.sol', 'w') as f:
        #f.write('%i\n' % (len(Sol_VC)))
        f.write(str(len(Sol_VC)) + '\n')
        f.write(str(Sol_VC)[1:-1])


    #WRITE TRACE FILES
    with open('.\Output\\' + inputfile.split('.')[0] + '_BnB_'+str(cutoff)+'.trace', 'w') as f:
        for t in times:
            f.write('%.2f,%i\n' % ((t[1]),t[0]))

if __name__ == '__main__':
    #create parser; example: python bnb.py --datafile ../Data/karate.graph --cutoff_time 200
    parser=argparse.ArgumentParser(description='Input parser for BnB')
    parser.add_argument('-inst',action='store',type=str,required=True,help='Inputgraph datafile')
    parser.add_argument('-alg',action='store',default=1000,type=str,required=True,help='Name of algorithm')
    parser.add_argument('-time',action='store',default=1000,type=int,required=True,help='Cutoff running time for algorithm')
    parser.add_argument('-seed',action='store',default=1000,type=int,required=False,help='random seed')
    args=parser.parse_args()

    algorithm = args.alg
    graph_file = args.inst
    output_dir = 'Output/'
    cutoff = args.time
    randSeed = args.seed
    main(graph_file, output_dir, cutoff, randSeed)
