# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 00:25:05 2022

@author: CC-i7-11700
"""
# 目的：随机生成1万对起点和重点，测试算法的效率
from route import *
import networkx as nx
from networkx import NetworkXNoPath, NodeNotFound
import time
start = time.time()
dict_highways = read_csv("shanghai_highways.csv","way")
dict_nodes = read_csv("shanghai_nodes_in_highways.csv","node")
end = time.time()
print("数据读取耗时:", end-start)
print("number of ways in connected highways:", len(dict_highways))
print("number of nodes in connected highways:", len(dict_nodes))

start = time.time()
AdjacencyList = Adjacency_List(dict_highways, dict_nodes)
end = time.time()
print("邻接表耗时:", end-start)
#-----------------------------------------------------------------------------#

nodes_id = list(dict_nodes.keys())
vertex_pair = []
import random
for ii in range(10000):
    vertex_pair.append(random.sample(nodes_id, k=2))

record_visited = False
directed = True
G = AdjacencyList2networkx(AdjacencyList, directed)

def check_isometric(path1, path2):
    cost1 = 0
    for ii in range(len(path1)-1):
        cost1 += distance_to_target(dict_nodes, path1[ii], path1[ii+1])
    cost2 = 0
    for ii in range(len(path2)-1):
        cost2 += distance_to_target(dict_nodes, path2[ii], path2[ii+1])
    return cost1 == cost2

#-----------------------------------------------------------------------------#

Time = [0.0 for _ in range(12)]

index = 0
for Vstart_id, Vend_id in vertex_pair:
    # print(Vstart_id, Vend_id)
    if index%500 == 0:
        print(index)

    start = time.time()
    cost00, path00 = Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, set(dict_nodes.keys()), Vstart_id, Vend_id)
    end = time.time()
    Time[0] += end-start
    
    start = time.time()
    cost01, path01 = Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vstart_id, Vend_id, record_visited)
    end = time.time()
    Time[1] += end-start
    
    start = time.time()
    cost02, path02 = Dijkstra_with_AdjacencyList_and_heap_v3(AdjacencyList, Vstart_id, Vend_id, record_visited)
    end = time.time()
    Time[2] += end-start
    
    start = time.time()
    cost03, path03 = Dijkstra_with_AdjacencyList_and_heap_v4(AdjacencyList, Vstart_id, Vend_id, record_visited)
    end = time.time()
    Time[3] += end-start
    
    start = time.time()
    cost04, path04 = Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, Vstart_id, Vend_id, directed)
    end = time.time()
    Time[4] += end-start
    
    start = time.time()
    cost05, path05 = Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vstart_id, Vend_id, directed)
    end = time.time()
    Time[5] += end-start
    
    start = time.time()
    cost06, path06 = Astar_with_AdjacencyList_and_heap_v2(AdjacencyList, dict_nodes, Vstart_id, Vend_id, record_visited)
    end = time.time()
    Time[6] += end-start
    
    start = time.time()
    cost07, path07 = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, Vstart_id, Vend_id, record_visited)
    end = time.time()
    Time[7] += end-start
    
    start = time.time()
    cost08, path08= Bidirectional_Astar_with_AdjacencyList_and_heap_v2(AdjacencyList, dict_nodes, Vstart_id, Vend_id, directed=True)
    end = time.time()
    Time[8] += end-start
    
    start = time.time()
    try:
        cost09, path09 = nx.single_source_dijkstra(G, Vstart_id, target=Vend_id)
    except NetworkXNoPath:
        if Vstart_id != Vend_id:
            cost09, path09 = float("inf"), []
        else:
            cost09, path09 = 0, [Vstart_id]
    except NodeNotFound:
        if Vstart_id != Vend_id:
            cost09, path09 = float("inf"), []
        else:
            cost09, path09 = 0, [Vstart_id]
    end = time.time()
    Time[9] += end - start
    
    start = time.time()
    try:
        cost10, path10 = nx.bidirectional_dijkstra(G, Vstart_id, Vend_id)
    except NetworkXNoPath:
        if Vstart_id != Vend_id:
            cost10, path10 = float("inf"), []
        else:
            cost10, path10 = 0, [Vstart_id]
    except NodeNotFound:
        if Vstart_id != Vend_id:
            cost10, path10 = float("inf"), []
        else:
            cost10, path10 = 0, [Vstart_id]
    end = time.time()
    Time[10] += end - start
    
    start = time.time()
    try:
        cost11, path11 = bi_dijkstra(G, Vstart_id, Vend_id)
    except NetworkXNoPath:
        if Vstart_id != Vend_id:
            cost11, path11 = float("inf"), []
        else:
            cost11, path11 = 0, [Vstart_id]
    except NodeNotFound:
        if Vstart_id != Vend_id:
            cost11, path11 = float("inf"), []
        else:
            cost11, path11 = 0, [Vstart_id]
    end = time.time()
    Time[11] += end - start
    
    label = True
    label = label and check_isometric(path00,path01)
    label = label and check_isometric(path00,path02)
    label = label and check_isometric(path00,path03)
    label = label and check_isometric(path00,path04)
    label = label and check_isometric(path00,path05)
    label = label and check_isometric(path00,path06)
    label = label and check_isometric(path00,path07)
    label = label and check_isometric(path00,path08)
    label = label and check_isometric(path00,path09)
    label = label and check_isometric(path00,path10)
    label = label and check_isometric(path00,path11)
    if label:
        pass
    else:
        print(Vstart_id, Vend_id, "出错了，需要进一步检查")
    
    index += 1

print("Dijkstra_with_AdjacencyList_and_heap_v1", Time[0])
print("Dijkstra_with_AdjacencyList_and_heap_v2", Time[1])
print("Dijkstra_with_AdjacencyList_and_heap_v3", Time[2])
print("Dijkstra_with_AdjacencyList_and_heap_v4", Time[3])
print("Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1", Time[4])
print("Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2", Time[5])
print("Astar_with_AdjacencyList_and_heap_v2", Time[6])
print("Astar_with_AdjacencyList_and_heap_v3", Time[7])
print("Bidirectional_Astar_with_AdjacencyList_and_heap_v2", Time[8])
print("bi_dijkstra", Time[11])
print("nx.single_source_dijkstra", Time[9])
print("nx.bidirectional_dijkstra", Time[10])

# print("路径检验", path00 == path01 == path02 == path03 == path04 == path05 == path06 == path07 == path08)
# print("cost检验", round(cost00,13) == round(cost01,13) == round(cost02,13) == round(cost03,13) == round(cost04,13) 
#       == round(cost05,13) == round(cost06,13) == round(cost07,13) == round(cost08,13))





