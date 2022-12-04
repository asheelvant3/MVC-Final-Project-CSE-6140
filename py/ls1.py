from datetime import datetime, timedelta
from random import choice, seed
from itertools import chain
import networkx as nx 
import time

def removal_edges(graph,vertex_cover,loss):
    for i in range(len(vertex_cover)): #removing vertices with loss 0
        if loss[i] == 0: vertex_cover[i] = 0
        if i in graph:
            for j in graph[i]:loss[j] = loss[j]+1
    return vertex_cover,graph,loss
def fast_vc(graph, cutoff_time, random_seed):
    return_tr=""
    seed(random_seed)
    start_time = time.time()
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
    # print(edges)
    leng=max(graph)+1
    vertex_cover = [0] * leng
    return_tr+=f"{time.time()-start_time}, {len(vertex_cover)}\n"
    print("VC1",len(vertex_cover))
    size=len(vertex_cover)
    loss = [0] * size
    gain = [0] * size
    for u, v in edges: #including all the vertices in the grapgh by adding the edges
        temp1=vertex_cover[u]
        temp2=vertex_cover[v]
        if temp1+temp2== 0:
            if len(graph[u])>=len(graph[v]):
                ind=u
            else:
                ind=v
            vertex_cover[ind] = 1
    return_tr+=f"{time.time()-start_time}, {sum(vertex_cover)}\n"
    for u, v in edges: # changing loss values for vertices included in vertex_cover
        temp1=vertex_cover[u]
        temp2=vertex_cover[v]
        if temp1+temp2== 1: 
            if temp1 < temp2:
                loss[v] += 1
            else:
                loss[u] += 1
    vertex_cover,graph,loss=removal_edges(graph,vertex_cover,loss)
    for u in graph:
        for v in graph[u]:
            if u<v:
                ed.append((u,v))
            else:
                ed.append((v,u))
    edges=set(ed)
    print("VC",sum(vertex_cover))
    calc,runtime=calculation(start_time,cutoff_time,graph,vertex_cover,gain,loss,edges,return_tr)
    t=[]
    t=','.join([str(i + 1) for i in range(len(calc)) if calc[i] == 1]) #getting the list of vertices
    return [str(sum(calc)),t,runtime]
def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    return fast_vc(graph, cutoff_time, random_seed)
def calculation(start_time,cutoff_time,graph,vertex_cover,gain,loss,edges,return_tr):
    edges=list(edges)
    curr_time = time.time()
    count=1
    while curr_time - start_time < cutoff_time:
        is_VC=True #validating if the candidate is a vertex cover
       
        for u in graph:
            for v in graph[u]:
                if vertex_cover[u] + vertex_cover[v] == 0:
                    is_VC =False
        if is_VC: 
            calc = [i for i in vertex_cover] #get the vertex with minimum loss and remove it
            # return_tr += f"{time.time()-start_time}, {sum(calc)}\n"
            l=[i for i in range(len(vertex_cover))]
            min_loss = min(l,key=lambda i: 999999 if vertex_cover[i] == 0 else loss[i])
            vertex_cover[min_loss] = 0
            gain[min_loss] = 0
            gain,loss=operation(graph,vertex_cover,min_loss,1,loss,gain)
        return_tr += f"{time.time()-start_time}, {sum(vertex_cover)}\n"
        print(f"{time.time()-start_time}, {sum(vertex_cover)}\n")
        indices=[]
        for i in range(len(vertex_cover)):
            if vertex_cover[i]==1:
                indices.append(i)
        best_ind = indices[0]
        for i in range(50): #picking vertex with minimum loss and removing it
            ch = choice(indices)
            if loss[best_ind]>=loss[ch]:
                best_ind=ch
        u=best_ind
        vertex_cover[u] = 0
        gain[u] = 0
        gain,loss=operation(graph,vertex_cover,u,1,loss,gain)
        flag=True
        indices=[i for i in range(len(vertex_cover)) if vertex_cover[i]==0]
        first=0
        while(flag and first<len(indices)):# find an uncovered edge and add its most connected vertex
            ind=indices[first]
            output = [x[1] for x in edges if x[0] == ind]
            if output:
                for i in output:
                    # print(vertex_cover[ind],vertex_cover[i])
                    if vertex_cover[ind] + vertex_cover[i]==0: #when the edge is found break
                        x,y=ind,i
                        flag=False
                        break
            first+=1
        if (flag==False):
                u = max(x, y, key=lambda x: gain[x])
                vertex_cover[u] = 1
                gain,loss=operation(graph,vertex_cover,u,0,loss,gain) #update loss and gain after adding vertex

        
        curr_time = time.time()
    return calc,return_tr
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
    # print(graph)
    if val==1:
        for v in graph[ind]: #the loss and gain of all neighbors is assigned to min loss cause egdes are uncovered
                if vertex_cover[v] == 0:gain[v] += 1
                else:loss[v] += 1
                    
    else:
        for v in graph[ind]: #loss and gain updation when vertex is added
            if vertex_cover[v] == 0:gain[v] -= 1
            else:loss[v] -= 1       
    return gain,loss


