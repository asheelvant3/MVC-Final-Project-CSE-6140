from datetime import datetime, timedelta
from random import choice, seed
from itertools import chain
from utils import construct_graph
import networkx as nx 
import os
output_directory = './output/' 
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
def removal_edges(graph,vertex_cover,loss):
    vcn = len(vertex_cover)
    for i in range(0, vcn): #removing vertices with loss 0
        if loss[i] != 0:
            continue
        else:
            if i in graph:
                for j in graph[i]:
                    loss[j] = loss[j] + 1
            vertex_cover[i] = 0
    return vertex_cover,graph,loss
def fast_vc(graph, filename, cutoff_time, random_seed,path_sol):
    seed(random_seed)
    start_time = datetime.now()
    inf = float('inf')
    ed=[]
    calc = None
    for u in graph:
        for v in graph[u]:
            if u<v:
                ed.append((u,v))
            else:
                ed.append((v,u))
    edges=set(ed)
    print(edges)
    leng=max(graph)+1
    vertex_cover = [0] * leng
    size=len(vertex_cover)
    loss = [0] * size
    gain = [0] * len(vertex_cover)
    vertex_cover = [0] * (max(graph) + 1)
    # edges = edges(graph)
    print("EDGES",edges)
    for u, v in edges:
        temp1=vertex_cover[u]
        temp2=vertex_cover[v]
        if temp1+temp2== 0:
            ind=max(u, v, key=lambda x: len(graph[x]))
            vertex_cover[ind] = 1
    for u, v in edges:
        temp1=vertex_cover[u]
        temp2=vertex_cover[v]
        if temp1+temp2== 1:
            if temp1 > temp2:
                loss[u] += 1
            else:
                loss[v] += 1
    vertex_cover,graph,loss=removal_edges(graph,vertex_cover,loss)
    for u in graph:
        for v in graph[u]:
            if u<v:
                ed.append((u,v))
            else:
                ed.append((v,u))
    edges=set(ed)
    calc,runtime=calculation(start_time,cutoff_time,graph,vertex_cover,gain,loss,edges)
    print("OUTPUT",calc,runtime)
    t=[]
    t=','.join([str(i + 1) for i in range(len(calc)) if calc[i] == 1])
    print(t)
    print(runtime)
    print(str(sum(calc)))
    return [str(sum(calc)),t,runtime]

# Run the algorithm on an input graph with a specified time and random seed
def run(filename, cutoff_time, random_seed,path_sol):
    seed(random_seed)
    graph = read_graph(filename)
    return fast_vc(graph, filename, cutoff_time, random_seed,path_sol)
def calculation(start_time,cutoff_time,graph,vertex_cover,gain,loss,edges):
    edges=list(edges)
    curr_time = datetime.now()
    print(vertex_cover)
    print("INITIAL LOSS",loss)
    while curr_time - start_time < timedelta(seconds=cutoff_time):
        is_solution=True
        for u in graph:
            for v in graph[u]:
                if vertex_cover[u] + vertex_cover[v] == 0:
                    is_solution =False
        if is_solution: 
            calc = [i for i in vertex_cover]
            l=[i for i in range(len(vertex_cover))]
            min_loss = min(l,key=lambda i: 999999 if vertex_cover[i] == 0 else loss[i])
            vertex_cover[min_loss] = 0
            gain[min_loss] = 0
            gain,loss=operation(graph,vertex_cover,min_loss,1,loss,gain)
        indices=[]
        for i in range(len(vertex_cover)):
            if vertex_cover [i]==0:
                indices.append(i)
        best_ind = indices[0]
        for i in range(25): #picking vertex with best loss
            
            ch = choice(indices)
            if loss[best_ind]>loss[ch]:best_ind=ch
        u=best_ind
        vertex_cover[u] = 0
        gain[u] = 0
        gain,loss=operation(graph,vertex_cover,u,1,loss,gain)
        ch = choice(edges) #picking an edge not covered and adding the most connected vertex
        v1=vertex_cover[ch[0]]
        v2=vertex_cover[ch[1]]
        while int(v1) + int(v2) > 0:
            ch = choice(edges)
            v1=vertex_cover[ch[0]]
            v2=vertex_cover[ch[1]]
        x, y =ch
        u = max(x, y, key=lambda x: gain[x])
        vertex_cover[u] = 1
        gain,loss=operation(graph,vertex_cover,u,0,loss,gain)
        curr_time = datetime.now()
    return calc,('{:0.2f}'.format((curr_time - start_time).total_seconds()))
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

def operation(graph,vertex_cover,ind,val,loss,gain):
    if val==1:
        for v in graph[ind]: #the loss and gain of all neighbors is assigned to min loss cause egdes are uncovered
                if vertex_cover[v] != 0:
                    loss[v] = loss[v] - 1
                else:
                    gain[v] = gain[v] + 1
    else:
        for v in graph[ind]: #loss and gain updation
            if vertex_cover[v] != 0:
                loss[v] = loss[v] - 1
            else:
                gain[v] = gain[v] + 1
    return gain,loss


