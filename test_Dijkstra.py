# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:18:28 2022

@author: CC-i7-11700
"""
# 目的：根据https://www.cs.usfca.edu/~galles/visualization/Dijkstra.html的实例测试Dijkstra算法的准确性

from route import *
import networkx as nx
from networkx import NetworkXNoPath, NodeNotFound
import time

# # example 1
# AdjacencyList = {"0":{"1":7},
#                   "1":{"0":9,"2":1},
#                   "2":{"3":9},
#                   "3":{"6":4,"10":6},
#                   "4":{"1":4,"5":5},
#                   "6":{"2":5,"3":3},
#                   "7":{"4":2,"8":7,"14":4},
#                   "8":{"4":2,"11":6},
#                   "9":{"6":7,"8":7,"10":1,"13":1},
#                   "10":{"3":2,"9":6,"17":7},
#                   "11":{"7":9,"12":4,"14":4},
#                   "12":{"11":3},
#                   "13":{"10":2},
#                   "14":{"7":9,"11":1},
#                   "15":{"17":2}}
# directed = True

# # example 2
# AdjacencyList = {"0":{"4":2},
#                   "2":{"6":6},
#                   "3":{"10":1,"17":4},
#                   "4":{"1":8,"5":6},
#                   "5":{"1":9,"4":1,"6":3},
#                   "6":{"3":8,"5":4},
#                   "7":{"4":1,"8":7,"11":5},
#                   "8":{"4":1,"11":3},
#                   "9":{"5":9,"8":2,"10":4,"13":7},
#                   "10":{"3":4,"6":6,"9":4,"13":9},
#                   "11":{"7":8,"8":1,"12":9},
#                   "12":{"9":3,"15":4},
#                   "13":{"9":9},
#                   "14":{"7":6},
#                   "15":{"11":7,"12":3},
#                   "16":{"12":6,"17":2},
#                   "17":{"10":9}}
# directed = True

# # example 3
# AdjacencyList = {"0":{"2":1,"4":3},
#                   "1":{"2":9,"4":6,"5":7},
#                   "2":{"1":1},
#                   "4":{"0":9,"5":1,"7":8,"8":8},
#                   "5":{"2":9,"6":5,"8":6},
#                   "6":{"5":8},
#                   "7":{"0":2},
#                   "8":{"9":5},
#                   "9":{"5":4,"13":8},
#                   "10":{"3":1,"6":7,"9":8,"13":7},
#                   "11":{"7":1,"14":5},
#                   "12":{"11":6,"16":7},
#                   "13":{"12":5,"16":5},
#                   "14":{"15":3},
#                   "15":{"11":8,"12":4,"14":2,"17":1},
#                   "16":{"12":4},
#                   "17":{"13":2}}
# directed = True

# example 4
AdjacencyList = {"0":{"4":7,"7":4,"14":3},
                  "1":{"2":7,"4":6,"5":3},
                  "2":{"1":7,"6":6},
                  "3":{"17":2},
                  "4":{"0":7,"1":6,"5":2,"7":6},
                  "5":{"1":3,"4":2,"8":9,"9":5},
                  "6":{"2":6,"9":3,"10":5},
                  "7":{"0":4,"4":6,"8":6,"11":7},
                  "8":{"5":9,"7":6,"9":5,"11":1},
                  "9":{"5":5,"6":3,"8":5,"13":2},
                  "10":{"6":5,"13":1},
                  "11":{"7":7,"8":1,"12":1,"15":9},
                  "12":{"11":1,"15":3,"16":9},
                  "13":{"9":2,"10":1,"16":6},
                  "14":{"0":3,"15":1},
                  "15":{"11":9,"12":3,"14":1,"16":2,"17":4},
                  "16":{"12":9,"13":6,"15":2},
                  "17":{"3":2,"15":4}}
directed = False
#-----------------------------------------------------------------------------#
num_vertex = 18
G = AdjacencyList2networkx(AdjacencyList, directed)

def check_isometric(path1, path2):
    cost1 = 0
    for ii in range(len(path1)-1):
        cost1 += AdjacencyList[path1[ii]][path1[ii+1]]
    cost2 = 0
    for ii in range(len(path2)-1):
        cost2 += AdjacencyList[path2[ii]][path2[ii+1]]
    return cost1 == cost2

Time = [0.0 for _ in range(10)]
for ii in range(18):
    for jj in range(18):
        
        # ii = 0
        # jj = 8
        Vstart_id = str(ii)
        Vend_id = str(jj)
        start = time.time()
        cost01, path01 = Dijkstra_with_AdjacencyList(AdjacencyList, set([str(ii) for ii in range(num_vertex)]), Vstart_id, Vend_id)
        end = time.time()
        Time[0] += end - start
        start = time.time()
        cost02, path02 = Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, set([str(ii) for ii in range(num_vertex)]), Vstart_id, Vend_id)
        end = time.time()
        Time[1] += end - start
        start = time.time()
        cost03, path03 = Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vstart_id, Vend_id)
        end = time.time()
        Time[2] += end - start
        start = time.time()
        cost04, path04 = Dijkstra_with_AdjacencyList_and_heap_v3(AdjacencyList, Vstart_id, Vend_id)
        end = time.time()
        Time[3] += end - start
        start = time.time()
        cost05, path05 = Dijkstra_with_AdjacencyList_and_heap_v4(AdjacencyList, Vstart_id, Vend_id)
        end = time.time()
        Time[4] += end - start
        start = time.time()
        cost06, path06 = Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, Vstart_id, Vend_id, directed)
        end = time.time()
        Time[5] += end - start
        start = time.time()
        cost07, path07 = Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vstart_id, Vend_id, directed)
        end = time.time()
        Time[6] += end - start
        start = time.time()
        try:
            cost08, path08 = bi_dijkstra(G, Vstart_id, Vend_id)
        except NetworkXNoPath:
            if Vstart_id != Vend_id:
                cost08, path08 = float("inf"), []
            else:
                cost08, path08 = 0, [Vstart_id]
        except NodeNotFound:
            if Vstart_id != Vend_id:
                cost08, path08 = float("inf"), []
            else:
                cost08, path08 = 0, [Vstart_id]
        end = time.time()
        Time[7] += end - start
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
        Time[8] += end - start
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
        Time[9] += end - start
                
        # print(cost01, path01)
        # print(cost02, path02)
        # print(cost03, path03)
        # print(cost04, path04)
        # print(cost05, path05)
        # print(cost06, path06)
        # print(cost07, path07)
        label = True
        label = label and check_isometric(path01,path02)
        label = label and check_isometric(path01,path03)
        label = label and check_isometric(path01,path04)
        label = label and check_isometric(path01,path05)
        label = label and check_isometric(path01,path06)
        label = label and check_isometric(path01,path07)
        label = label and check_isometric(path01,path08)
        label = label and check_isometric(path01,path09)
        label = label and check_isometric(path01,path10)
        
        if label:
            pass
            # print(Vstart_id, Vend_id, cost01, path01)
        else:
            print(Vstart_id, Vend_id, "出现错误,需进一步核对!!")


print("Dijkstra_with_AdjacencyList", Time[0])
print("Dijkstra_with_AdjacencyList_and_heap_v1", Time[1])
print("Dijkstra_with_AdjacencyList_and_heap_v2", Time[2])
print("Dijkstra_with_AdjacencyList_and_heap_v3", Time[3])
print("Dijkstra_with_AdjacencyList_and_heap_v4", Time[4])
print("Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1", Time[5])
print("Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2", Time[6])
print("bi_dijkstra", Time[7])
print("nx.single_source_dijkstra", Time[8])
print("nx.bidirectional_dijkstra", Time[9])
