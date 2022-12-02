import time
import numpy as np

def greedy(G, VC_curr, maxTime, start_time):
    """
    Function to find a greedy vertex cover solution from a given set of potential vertex covers

    Input Parameters: \n
        G: NetworkX graph object \n
        VC_curr: Current vertex cover \n
        maxTime: Cutoff time to stop simulation \n
        start_time: Time to keep as baseline to record performance and benchmark \n

    Output: \n
        A list of nodes that forms a greedy optimal vertex cover \n
    """
    node_degree = [(node, degree) for node, degree in sorted(G.degree(VC_curr), key=lambda item: item[1])]
    node_idx = 0
    # For each node sorted by degree, check if its neighbors are in the current VC.
    # If the node has neighbors in the current VC, you can safely remove the node from VC as it will still cover all edges.
    while ((time.time() - start_time) < maxTime) and (node_idx < len(node_degree)):
        curr_node = node_degree[node_idx][0]
        isRemove = [1 for neigh_node in G.neighbors(curr_node) if neigh_node not in VC_curr]
        if not len(isRemove):    
            VC_curr.remove(curr_node)            
        node_idx += 1
    return VC_curr

def SimulatedAnnealing(G, maxTime, start_time, return_str = "", Temperature = 0.8, Temperature_scaler = 0.95, seed = 10):  
    """
    Function to run simulated annealing with cutoff

    Input parameters: \n
        G: NetworkX graph object \n
        maxTime: Cutoff time to stop simulation \n
        start_time: Time to keep as baseline to record performance and benchmark \n
        return_str: String that contains information to write \n
        Temperature: Temperature used in annealing \n
        Temperature_scaler: Factor that gets multiplied with temperature before moving to next iteration \n
        Seed: Random seed \n
    
    Output: \n
        A list of nodes that forms an optimal vertex cover \n
        String that contains information to write \n
    """
    np.random.seed(seed)

    VC_curr = [n for n in G.nodes()] # Initialize the current VC with set of all nodes
    unreachable_nodes = []
    while ((time.time() - start_time) < maxTime):
        # When Temperature is equal to zero, we return the greedy solution from the current vertex cover
        if Temperature == 0:
            VC_curr_can = greedy(G.copy(), VC_curr.copy(), maxTime, start_time)
            if len(VC_curr_can)  < len(VC_curr):
                return_str += f"{time.time()-start_time}, {len(VC_curr)}\n"
                VC_opt = VC_curr_can
            else:
                VC_opt = VC_curr
            return VC_opt, return_str

        # First find the possible nodes we can remove and shift them to the list of unreachable_nodes
        while len(unreachable_nodes) == 0:
            return_str += f"{time.time()-start_time}, {len(VC_curr)}\n"
            VC_opt = VC_curr.copy() # Assign the optimal VC to the current VC
            # Randomly choose a node to remove
            # Check if it has its neighbors included in the current VC
            # If it has its neighbors not included in the current VC, then shift all these nodes to unreachable list
            node2remove = np.random.choice(VC_opt) 
            make_unreachable = [neigh_node for neigh_node in G.neighbors(node2remove) if neigh_node not in VC_curr]
            make_unreachable += [node2remove]*len(make_unreachable)
            unreachable_nodes.extend(make_unreachable)
            VC_curr.remove(node2remove)     

        # Local Search Exploration

        # Save a copy of the current solution before searching
        VC_old = VC_curr.copy()
        unreachable_nodes_old = unreachable_nodes.copy()

        # Randomly delete a node from the current VC. 
        node2remove = np.random.choice(VC_curr)
        # To the unreachable nodes list, add the deleted node along with its neighbours that are not included in the current VC
        make_unreachable = [neigh_node for neigh_node in G.neighbors(node2remove) if neigh_node not in VC_curr]
        make_unreachable += [node2remove]*len(make_unreachable)
        unreachable_nodes.extend(make_unreachable)        
        VC_curr.remove(node2remove)   

        # Randomly add a node to the current VC
        node2add = np.random.choice(unreachable_nodes)
        # Since we are taking a node from univisited_nodes list and adding it to the current VC, 
        # all the neighbours of the node can be visited. Hence, we should also remove its neighbors from 
        # the univisited_nodes list
        make_visited = [neigh_node for neigh_node in G.neighbors(node2add) if neigh_node not in VC_curr]
        make_visited += [node2add]*len(make_visited)
        for mv in make_visited:
            unreachable_nodes.remove(mv)
        VC_curr.append(node2add)

        # We measure the improvement using the list of nodes that cannot be visited (delta)
        delta = len(unreachable_nodes_old) - len(unreachable_nodes) 
        # If delta >= 0, we accept the new solution with probabiliity = 1
        if delta < 0:
            # We accept the new solution with a probabiliity that is a function of delta and the temperature
            annhealing_const = np.exp(delta/Temperature)
            probab2explore = 1 - annhealing_const # Probabiliity to explore
            if np.random.rand() > probab2explore:
                pass
            else:  
                VC_curr = VC_old.copy()
                unreachable_nodes = unreachable_nodes_old.copy()

        # Decrease the temperature using the scaling factor before continuing to the next iteration
        Temperature = Temperature_scaler * Temperature 

    print(f"SA final solution size: {len(VC_opt)}") 
    return VC_opt, return_str