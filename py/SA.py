import time
import numpy as np

def run_SA(G, maxTime, start_time, return_str, Temperature = 0.8, Temperature_scaler = 0.95, seed = 10):  
    np.random.seed(seed)

    VC_curr = [n for n in G.nodes()]
    node_degree = [(node, degree) for node, degree in sorted(G.degree(VC_curr), key=lambda item: item[1])]
    node_idx = 0
    while ((time.time() - start_time) < maxTime) and (node_idx < len(node_degree)):
        curr_node = node_degree[node_idx][0]
        isRemove = [1 for neigh_node in G.neighbors(curr_node) if neigh_node not in VC_curr]
        if not len(isRemove):    
            VC_curr.remove(curr_node)            
        node_idx += 1

    unvisited_nodes = []
    while ((time.time() - start_time) < maxTime):
        
        while len(unvisited_nodes) == 0:
            return_str += f"{time.time()-start_time}, {len(VC_curr)}\n"
            VC_opt = VC_curr.copy()
            node2remove = np.random.choice(VC_opt)
            make_unvisited = [neigh_node for neigh_node in G.neighbors(node2remove) if neigh_node not in VC_curr]
            make_unvisited += [node2remove]*len(make_unvisited)
            unvisited_nodes.extend(make_unvisited)
            VC_curr.remove(node2remove)     

        VC_cand = VC_curr.copy()
        unvisited_nodes_cand = unvisited_nodes.copy()
        node2remove = np.random.choice(VC_curr)
        make_unvisited = [neigh_node for neigh_node in G.neighbors(node2remove) if neigh_node not in VC_curr]
        make_unvisited += [node2remove]*len(make_unvisited)
        unvisited_nodes.extend(make_unvisited)        
        VC_curr.remove(node2remove)   

        node2add = np.random.choice(unvisited_nodes)
        make_visited = [neigh_node for neigh_node in G.neighbors(node2add) if neigh_node not in VC_curr]
        make_visited += [node2add]*len(make_visited)
        for mv in make_visited:
            unvisited_nodes.remove(mv)
        VC_curr.append(node2add)

        if len(unvisited_nodes_cand) < len(unvisited_nodes):
            delta = len(unvisited_nodes_cand) - len(unvisited_nodes) 
            annhealing_const = np.exp(delta/Temperature)
            if np.random.rand() <= annhealing_const:
                pass
            else:  
                VC_curr = VC_cand.copy()
                unvisited_nodes = unvisited_nodes_cand.copy()
        
        Temperature = Temperature_scaler * Temperature 

    print(f"SA final solution size: {len(VC_opt)}") 
    return VC_opt, return_str



# class SA:    
#     def simAnn(self, G, return_str, S, maxTime, start_time, T = 0.8):   
#         VC_opt = S.copy()
#         uncovered_edges = []
#         all_nodes = set([n for n in G.nodes()])
#         while ((time.time() - start_time) < maxTime):
#             T = 0.95 * T 

#             # looking for a better solution with less vertice
#             while not uncovered_edges:
#                 VC_opt = S.copy()
#                 return_str += f"{time.time()-start_time}, {len(VC_opt)}\n"
#                 delete_v = np.random.choice(S)
#                 for v in G.neighbors(delete_v):
#                     if v not in S:
#                         if v < delete_v:
#                             uncovered_edges.append((v, delete_v))
#                         else:
#                             uncovered_edges.append((delete_v, v))
#                 S.remove(delete_v)     


#             # del node
#             S_current = S.copy()
#             uncovered_edges_cand = uncovered_edges.copy()
#             delete_v = np.random.choice(S)
#             for v in G.neighbors(delete_v):
#                 if v not in S:
#                     if v < delete_v:
#                         uncovered_edges.append((v, delete_v))
#                     else:
#                         uncovered_edges.append((delete_v, v))
#             S.remove(delete_v)   


#             # add node
#             uncovered_nodes = all_nodes - set(S)
#             add_v = np.random.choice(list(uncovered_nodes))
#             S.append(add_v)
#             for v in G.neighbors(add_v):
#                 if v not in S:
#                     if v < add_v:
#                         uncovered_edges.remove((v, add_v))
#                     else:
#                         uncovered_edges.remove((add_v, v))

#             # accept a new solution based on the probability which is proportional to the 
#             # difference between the quality of the best solution and the current solution, and the temperature. 
#             if len(uncovered_edges_cand) < len(uncovered_edges): 
#                 p = math.exp(2*float(len(uncovered_edges_cand) - len(uncovered_edges))/T)
#                 alpha = np.random.rand()
#                 if alpha > p:    
#                     S = S_current.copy()
#                     uncovered_edges = uncovered_edges_cand.copy()

#         return VC_opt, return_str

#     def simulate_annealing(self, G, maxTime, start_time, return_str, T = 0.8):  

#         Ginit = G.copy()
#         S = [n for n in Ginit.nodes()]
#         node_degree = [(node, degree) for node, degree in sorted(Ginit.degree(S), key=lambda item: item[1])]
#         node_idx = 0
#         while ((time.time() - start_time) < maxTime and node_idx < len(node_degree)):
#             flag = True
#             curr_node = node_degree[node_idx][0]
#             for neigh_node in Ginit.neighbors(curr_node):
#                 if neigh_node not in S:
#                     flag = False
#             if flag:    
#                 S.remove(curr_node)            
#             node_idx += 1
#         print(f"Initial Solution size: {len(S)}")

#         S_ret = S.copy()
#         unvisited_nodes = []
#         while ((time.time() - start_time) < maxTime):
#             # looking for a better solution with less vertice
#             while not unvisited_nodes:
#                 S_ret = S.copy()
#                 return_str += f"{time.time()-start_time}, {len(S_ret)}\n"
#                 delete_v = np.random.choice(S)
#                 for v in G.neighbors(delete_v):
#                     if v not in S:
#                         unvisited_nodes.append(v)
#                         unvisited_nodes.append(delete_v)
#                 S.remove(delete_v)     

#             S_current = S.copy()
#             unvisited_nodes_cand = unvisited_nodes.copy()
#             delete_v = np.random.choice(S)
#             for v in G.neighbors(delete_v):
#                 if v not in S:
#                     unvisited_nodes.append(v)
#                     unvisited_nodes.append(delete_v)            
#             S.remove(delete_v)   

#             add_v = np.random.choice(unvisited_nodes)
#             for v in G.neighbors(add_v):
#                 if v not in S:
#                     unvisited_nodes.remove(v)
#                     unvisited_nodes.remove(add_v)
#             S.append(add_v)

#             if len(unvisited_nodes_cand) < len(unvisited_nodes):
#                 delta = len(unvisited_nodes_cand) - len(unvisited_nodes) 
#                 p = np.exp(delta/T)
#                 alpha = np.random.rand()
#                 if alpha > p:    
#                     S = S_current.copy()
#                     unvisited_nodes = unvisited_nodes_cand.copy()

#             T = 0.95 * T 
            
#         return S_ret, return_str
