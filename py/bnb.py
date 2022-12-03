import networkx as nx
import time
import math
import approx

def BranchBound(Graph, Cutoff):
    StartTime = time.time()
    backtrack = False #set to True when we reach a pruned node or leaf
    BestVC = [] #Best Vertex Cover so far
    BestVC_Size = Graph.number_of_nodes() #Upper Bound = Size of best Vertex Cover so far; Initially = total number of nodes
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
        (candidate_node, in_VC, _) = F.pop() 
        backtrack = False #set to True when we reach a pruned node or leaf
        if in_VC: #if we add cand to VC, we can delete it from our subproblem
            SubG.remove_node(candidate_node)
        else: #if we don't add cand to VC, we have to add all of cand's neighbours to VC
            for node in list(SubG.neighbors(candidate_node)):
                VC.append((node, 1))
                SubG.remove_node(node)

        VC.append((candidate_node, in_VC))
        VC_Size = sum([x[1] for x in VC])

        #[Check 1: reached a feasible (complete) solution]
        if SubG.number_of_edges() == 0:
            if VC_Size < BestVC_Size:
                BestVC = VC.copy()
                BestVC_Size = VC_Size
                track_sols.append((VC_Size, time.time()-StartTime))
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
                F.extend([(new_cand[0], 0, (candidate_node, in_VC)), (new_cand[0], 1, (candidate_node, in_VC))])

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

    return_str = ""
    for t in track_sols:
        return_str += '%.2f,%i\n' % ((t[1]),t[0])

    return [x[0] for x in BestVC if x[1] == 1], return_str

def LowerBound(SubG): #uses ln(max degree) approx
    _, x = approx.max_degree_greedy(SubG, 0, 600)
    return int(x)/math.log((max(2, max(SubG.degree, key = lambda x: x[1])[1])))
