from datetime import datetime, timedelta
from random import choice, seed
from itertools import chain
from utils import construct_graph
import networkx as nx 
import os
output_directory = './output/' 
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
def fast_vc(graph, filename, cutoff_time, random_seed):
    seed(random_seed)
    # edges=graph.edges()
    # vertex_cover = [0] * (max(graph.nodes()) + 1)
    edges=list(set(chain(
        *[[(u, v) if u < v else (v, u) for v in graph[u]] for u in graph])))
    vertex_cover = [0] * (max(graph) + 1)
    for i, j in edges:
        if vertex_cover[i] + vertex_cover[j] == 0:
            ind=max(i, j, key=lambda x: len(graph[x]))
            vertex_cover[ind] = 1
    # print(edges)
    loss = [0] * len(vertex_cover) #loss for each vertex
    for i, j in edges:
        if vertex_cover[i] + vertex_cover[j] == 1: #picking vertex which exists in the vertex cover
            if vertex_cover[i] < vertex_cover[j]:
                loss[j] = loss[j]+1
            else:
                loss[i] =loss[i]+ 1
    for i in range(len(vertex_cover)): #removing vertices with loss 0
        if loss[i] == 0:
            vertex_cover[i] = 0
            if i in graph:
                for j in graph[i]:
                    loss[j] = loss[j]+1

    gain = [0] * len(vertex_cover)
    edges=  list(set(chain(  *[[(u, v) if u < v else (v, u) for v in graph[u]] for u in graph]
    )))
    calc = None

    # IO stuff
    start_time = cur_time = datetime.now()
    inf = float('inf')
    out = filename.split('/')[-1].split('.')[0] \
           + '_ls1_' + str(cutoff_time) + '_' \
           + str(random_seed)
    base=output_directory+out
    print(base)
    # base=open(os.path.join(output_directory, base),'w')
    calc=calculation(start_time,cutoff_time,graph,vertex_cover,out,gain,loss,edges)
    with open(base + '.sol', 'w') as sol:
        sol.write(str(sum(calc)) + '\n')
        sol.write(
            ','.join([str(i + 1) for i in range(len(calc)) if calc[i] == 1]))
    return calc


# Run the algorithm on an input graph with a specified time and random seed
def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    fast_vc(graph, filename, cutoff_time, random_seed)
def calculation(start_time,cutoff_time,graph,vertex_cover,out,gain,loss,edges):
    inf = float('inf')
    cur_time = datetime.now()
    base=output_directory+out
    with open(base + '.trace', 'w') as trace:
        while cur_time - start_time < timedelta(seconds=cutoff_time):
                is_solution=True
                for u in graph:
                    for v in graph[u]:
                        if vertex_cover[u] + vertex_cover[v] == 0:
                            is_solution =False
                if is_solution: 
                    # Since vertices are only shuffled around when the candidate
                    # is not a solution, any time the candidate is a solution, it
                    # will be the best one
                    calc = [i for i in vertex_cover]
                    trace.write('{:0.2f}'.format(
                        (cur_time - start_time).total_seconds()
                    ))
                    trace.write(',' + str(sum(calc)) + '\n')
                    # Finding the vertex with minimum loss and remove it from vertex cover
                    min_loss = min([i for i in range(len(vertex_cover))],
                                key=lambda i: inf if vertex_cover[i] == 0 else loss[i])
                    vertex_cover[min_loss] = 0
                    gain[min_loss] = 0
                    for v in graph[min_loss]: #the loss and gain of all neighbors is assigned to min loss cause egdes are uncovered
                        if vertex_cover[v] == 0:
                            gain[v] += 1
                        else:
                            loss[v] += 1
                    continue
                # choose the vertex with approximately minimum loss and remove it
                indices = [i for i in range(len(vertex_cover)) if vertex_cover[i] == 1]
                best_ind = indices[0]
                for i in range(50): #picking vertex with best loss
                    ch = choice(indices)
                    if loss[ch] < loss[best_ind]:
                        best_ind = ch
                u=best_ind
                vertex_cover[u] = 0
                gain[u] = 0
                for v in graph[u]: #updating neighboring vertices loss and gain values
                    if vertex_cover[v] == 0:
                        gain[v] += 1
                    else:
                        loss[v] += 1
                r = choice(edges) #picking an edge not covered and adding the most connected vertex
                while vertex_cover[r[0]] + vertex_cover[r[1]] > 0:
                    r = choice(edges)
                x, y =r
                u = max(x, y, key=lambda x: gain[x])
                vertex_cover[u] = 1
                for v in graph[u]: #loss and gain updation
                    if vertex_cover[v] == 0:
                        gain[v] -= 1
                    else:
                        loss[v] -= 1
                cur_time = datetime.now()
    return calc
def read_graph(filename):
    graph = {}
    with open(filename, 'r') as file:
        file.readline()
        for i, line in enumerate(file):
            if len(line.strip()) > 0:
                l=[]
                for j in line.split():
                    l.append(int(j)-1)
                graph[i]=set(l)
    return graph

