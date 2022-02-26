# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 21:40:46 2022

@author: CC-i7-11700
"""
from itertools import permutations,combinations
import math
import csv, os
import heapq, copy
import networkx as nx

#-----------------------------------------------------------------------------#
# 0.数据读取 & 邻接表
# 读取解析后的csv, 保存为dict, key=id_
def read_csv(path, dtype):
    dict1 = {}
    assert os.path.exists(path)
    assert dtype == "node" or dtype == "way"
    with open(path, 'r', newline='', encoding='utf-8') as file:
        spreadsheet = csv.reader(file)
        next(spreadsheet)       # 跳过表头
        for row in spreadsheet: # 由于spreadsheet只能被遍历一次，所以此时spreadsheet从第二行开始
            id_ = row.pop(0)
            if dtype == "node":
                dict1[id_] = [float(num) for num in row] # value=[lat,lon]
            elif dtype == "way":
                dict1[id_] = row                         # value=[node_id, ...]
    return dict1

def distance_to_target(dict_nodes, Vcur_id, Vtarget_id):
    lat1,lon1 = dict_nodes[Vcur_id][0:2]
    lat2,lon2 = dict_nodes[Vtarget_id][0:2]
    return ((lat1-lat2)**2+(lon1-lon2)**2)**0.5

def Adjacency_List(dict_ways, dict_nodes):
    AdjacencyList = {}
    for way_id, nodes_id in dict_ways.items():
        for ii in range(len(nodes_id)-1):
            # 计算距离
            dist = distance_to_target(dict_nodes, nodes_id[ii], nodes_id[ii+1])
            # lat1,lon1 = dict_nodes[nodes_id[ii]][0:2]
            # lat2,lon2 = dict_nodes[nodes_id[ii+1]][0:2]
            # dist = ((lat1-lat2)**2+(lon1-lon2)**2)**0.5
            # 邻接表
            if nodes_id[ii] not in AdjacencyList:
                AdjacencyList[nodes_id[ii]] = {nodes_id[ii+1]: dist}
            else:
                AdjacencyList[nodes_id[ii]][ nodes_id[ii+1] ] = dist
            # 无向图的邻接表是对称的
            if nodes_id[ii+1] not in AdjacencyList:
                AdjacencyList[nodes_id[ii+1]] = {nodes_id[ii]: dist}
            else:
                AdjacencyList[nodes_id[ii+1]][ nodes_id[ii] ] = dist
    return AdjacencyList

def AdjacencyList2networkx(AdjacencyList, directed=True):
    if directed:
        G = nx.DiGraph() # 有向图
    else:
        G = nx.Graph()   # 无向图
    for Vstart_id in AdjacencyList.keys():
        if Vstart_id not in G.nodes:
            G.add_node(Vstart_id)
        for Vend_id, weight in AdjacencyList[Vstart_id].items():
            if Vend_id not in G.nodes:
                G.add_node(Vend_id)
            G.add_edge(Vstart_id, Vend_id, weight=weight)
    # print("所有顶点:",list(G.nodes))
    # print("所有边:", list(G.edges))
    # print("第一个顶点的相邻顶点", list(G.adj[list(G.nodes)[0]]))
    # print("第一条边的权重", G.edges[list(G.edges)[0]]['weight'])
    return G

#-----------------------------------------------------------------------------#
# 1.最短路（适用范围：无向图 & 有向图，连通图 & 不连通图）
def Dijkstra_with_AdjacencyList(AdjacencyList, set_unvisited, Vcur_id, Vend_id=None):
    # step1. 构造记录: 所有顶点到起点的最短距离(cur_distance_to_Vstart); 路径(path)
    cur_distance_to_Vstart = {}
    paths = {} # 路径
    for vertice_id in set_unvisited:
        cur_distance_to_Vstart[vertice_id] = float('inf')
        paths[vertice_id] = None # 路径
    cur_distance_to_Vstart[Vcur_id] = 0
    
    while len(set_unvisited) > 0 and Vcur_id != Vend_id:
        # step 4.1.从未访问顶点集合移除当前顶点
        set_unvisited.remove(Vcur_id)
        # step 4.2.如果当前顶点在邻接表中
        if Vcur_id in AdjacencyList:
            for Vnext_id, dist in AdjacencyList[Vcur_id].items():
                # step 4.3.如果与当前顶点相连的顶点未被访问过
                if Vnext_id in set_unvisited:
                    # step 4.4.松弛
                    if cur_distance_to_Vstart[Vcur_id]+dist < cur_distance_to_Vstart[Vnext_id]:
                        cur_distance_to_Vstart[Vnext_id] = cur_distance_to_Vstart[Vcur_id]+dist
                        paths[Vnext_id] = Vcur_id # 路径,记录上一个顶点
    
        # step3. 在未访问的顶点集合中，寻找距起点最近的顶点作为当前顶点（贪婪思想）
        Vcur_id = None
        label_find = False
        distance_temp = float('inf')
        for Vcandidate_id in set_unvisited:
            if cur_distance_to_Vstart[Vcandidate_id] < distance_temp:
                distance_temp = cur_distance_to_Vstart[Vcandidate_id]
                Vcur_id = Vcandidate_id
                label_find = True
        if not label_find: # 如果找不到，说明 当前顶点及剩余未访问的顶点 均与起点不连通，提前跳出循环
            break
    
    if Vend_id == None:
        # 根据 paths 反推路径 routes
        routes = {}
        for vertice_id in cur_distance_to_Vstart.keys():
            if cur_distance_to_Vstart[vertice_id] < float("inf"):
                temp = [vertice_id]
                while paths[temp[-1]] != None:
                    temp.append(paths[temp[-1]])
                routes[vertice_id] = temp[::-1]
            else:
                routes[vertice_id] = []
        return cur_distance_to_Vstart, routes # 返回所有顶点到起点的最短距离，及其路径
    else:
        # 根据 paths 反推路径 route
        route = []
        if cur_distance_to_Vstart[Vend_id] < float("inf"):
            route.append(Vend_id)
            while paths[route[-1]] != None:
                route.append(paths[route[-1]])
        return cur_distance_to_Vstart[Vend_id], route[::-1] # 返回终点到起点的最短距离，及其路径

def Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, set_unvisited, Vcur_id, Vend_id=None):
    # step1. 构造记录: 所有顶点到起点的最短距离(cur_distance_to_Vstart); 路径(path)
    cur_distance_to_Vstart = {}
    paths = {} # 路径
    for vertice_id in set_unvisited:
        cur_distance_to_Vstart[vertice_id] = float('inf')
        paths[vertice_id] = None # 路径
    cur_distance_to_Vstart[Vcur_id] = 0
    
    # 构造堆/heap，存储(当前顶点到起点的最短距离, 当前顶点的id)
    Heap = [(0, Vcur_id)]
    
    while Heap and Vcur_id != Vend_id:
        # step3. 从堆顶取一个顶点，作为当前顶点（贪婪）
        cost, Vcur_id = heapq.heappop(Heap)
        if Vcur_id in set_unvisited: # 如果当前顶点未被访问过
        
            # step 4.1.从未访问顶点集合移除当前顶点
            set_unvisited.remove(Vcur_id)
            # step 4.2.如果当前顶点在邻接表中
            if Vcur_id in AdjacencyList:
                for Vnext_id, dist in AdjacencyList[Vcur_id].items():
                    # step 4.3.如果与当前顶点相连的顶点未被访问过
                    if Vnext_id in set_unvisited:
                        # step 4.4.松弛
                        if cur_distance_to_Vstart[Vcur_id]+dist < cur_distance_to_Vstart[Vnext_id]:
                            cur_distance_to_Vstart[Vnext_id] = cur_distance_to_Vstart[Vcur_id]+dist
                            paths[Vnext_id] = Vcur_id # 路径,记录上一个顶点
                            heapq.heappush(Heap, (cur_distance_to_Vstart[Vcur_id]+dist, Vnext_id))
    
    if Vend_id == None:
        # 根据 paths 反推路径 routes
        routes = {}
        for vertice_id in cur_distance_to_Vstart.keys():
            if cur_distance_to_Vstart[vertice_id] < float("inf"):
                temp = [vertice_id]
                while paths[temp[-1]] != None:
                    temp.append(paths[temp[-1]])
                routes[vertice_id] = temp[::-1]
            else:
                routes[vertice_id] = []   
        return cur_distance_to_Vstart, routes # 返回所有顶点到起点的最短距离，及其路径
    else:
        # 根据 paths 反推路径 route
        route = []
        if cur_distance_to_Vstart[Vend_id] < float("inf"):
            route.append(Vend_id)
            while paths[route[-1]] != None:
                route.append(paths[route[-1]])
        return cur_distance_to_Vstart[Vend_id], route[::-1] # 返回终点到起点的最短距离，及其路径

def Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vcur_id, Vend_id=None, record_visited=False):
    # 相对于Dijkstra_with_AdjacencyList_and_heap_v1，将set_unvisited更改为set_visited
    # step1. 构造记录: 所有顶点到起点的最短距离(cur_distance_to_Vstart); 路径(path)
    cur_distance_to_Vstart = {Vcur_id:0}
    paths = {} # 路径
    set_visited = set()
    
    # 构造堆/heap，存储(当前顶点到起点的最短距离, 当前顶点的id)
    Heap = [(0, Vcur_id)]
    
    if record_visited:
        list_visited = [] # 记录访问过的顶点，用于绘图
    
    while Heap and Vcur_id != Vend_id:
        
        if record_visited:
            set_visited_old = copy.deepcopy(set_visited)
            
        # step3. 从堆顶取一个顶点，作为当前顶点（贪婪）
        cost, Vcur_id = heapq.heappop(Heap)
        if Vcur_id not in set_visited: # 如果当前顶点未被访问过
        
            # step 4.1.从未访问顶点集合移除当前顶点
            set_visited.add(Vcur_id)
            # step 4.2.如果当前顶点在邻接表中
            if Vcur_id in AdjacencyList:
                for Vnext_id, dist in AdjacencyList[Vcur_id].items():
                    # step 4.3.如果与当前顶点相连的顶点未被访问过
                    if Vnext_id not in set_visited:
                        # step 4.4.松弛
                        len_cur2next = cur_distance_to_Vstart[Vcur_id]+dist
                        if (Vnext_id in cur_distance_to_Vstart and len_cur2next < cur_distance_to_Vstart[Vnext_id]) or Vnext_id not in cur_distance_to_Vstart:
                            cur_distance_to_Vstart[Vnext_id] = len_cur2next
                            paths[Vnext_id] = Vcur_id # 路径,记录上一个顶点
                            heapq.heappush(Heap, (cur_distance_to_Vstart[Vnext_id], Vnext_id))
                            
        if record_visited:
            if set_visited != set_visited_old:
                set_diff = set_visited - set_visited_old
                list_visited.append( set_diff.pop() )
    
    if Vend_id == None:
        # 根据 paths 反推路径 routes
        routes = {}
        for vertice_id in cur_distance_to_Vstart.keys():
            if cur_distance_to_Vstart[vertice_id] < float("inf"):
                temp = [vertice_id]
                while temp[-1] in paths:
                    temp.append(paths[temp[-1]])
                routes[vertice_id] = temp[::-1]
            else:
                routes[vertice_id] = []   
        return cur_distance_to_Vstart, routes # 返回所有顶点到起点的最短距离，及其路径
    else:
        # 根据 paths 反推路径 route
        route = []
        if Vend_id in cur_distance_to_Vstart and cur_distance_to_Vstart[Vend_id] < float("inf"):
            route.append(Vend_id)
            while route[-1] in paths:
                route.append(paths[route[-1]])
            return cur_distance_to_Vstart[Vend_id], route[::-1] # 返回终点到起点的最短距离，及其路径
        else:
            return float("inf"), route
        
def Dijkstra_with_AdjacencyList_and_heap_v3(AdjacencyList, Vcur_id, Vend_id=None, record_visited=False):
    # 相对于Dijkstra_with_AdjacencyList_and_heap_v1， 移除set_unvisited，并将其功能整合到cur_distance_to_Vstart
    # 相对于Dijkstra_with_AdjacencyList_and_heap_v2， 移除set_visited，并将其功能整合到cur_distance_to_Vstart
    # step1. 构造记录: 所有顶点到起点的最短距离(cur_distance_to_Vstart); 路径(path)
    cur_distance_to_Vstart = {Vcur_id:0}
    paths = {} # 路径
    Heap = [(0, Vcur_id)]# 构造堆/heap，存储(当前顶点到起点的最短距离, 当前顶点的id)
    
    if record_visited:
        list_visited = [] # 记录访问过的顶点，用于绘图
        
    while Heap and Vcur_id != Vend_id:
        
        if record_visited:
            visited_old = copy.deepcopy(cur_distance_to_Vstart.keys())
            
        # step3. 从堆顶取一个顶点，作为当前顶点（贪婪）
        cost, Vcur_id = heapq.heappop(Heap)

        if Vcur_id in AdjacencyList:
            for Vnext_id, dist in AdjacencyList[Vcur_id].items():
                # step 4.4.松弛
                len_cur2next = cur_distance_to_Vstart[Vcur_id]+dist
                if (Vnext_id in cur_distance_to_Vstart and len_cur2next < cur_distance_to_Vstart[Vnext_id]) or Vnext_id not in cur_distance_to_Vstart:
                    cur_distance_to_Vstart[Vnext_id] = len_cur2next
                    paths[Vnext_id] = Vcur_id # 路径,记录上一个顶点
                    heapq.heappush(Heap, (cur_distance_to_Vstart[Vnext_id], Vnext_id))
                    
        if record_visited:
            if cur_distance_to_Vstart.keys() != visited_old:
                diff = cur_distance_to_Vstart.keys() - visited_old
                list_visited.append( diff.pop() )
                
    if Vend_id == None:
        # 根据 paths 反推路径 routes
        routes = {}
        for vertice_id in cur_distance_to_Vstart.keys():
            if cur_distance_to_Vstart[vertice_id] < float("inf"):
                temp = [vertice_id]
                while temp[-1] in paths:
                    temp.append(paths[temp[-1]])
                routes[vertice_id] = temp[::-1]
            else:
                routes[vertice_id] = []   
        return cur_distance_to_Vstart, routes # 返回所有顶点到起点的最短距离，及其路径
    else:
        # 根据 paths 反推路径 route
        route = []
        if Vend_id in cur_distance_to_Vstart and cur_distance_to_Vstart[Vend_id] < float("inf"):
            route.append(Vend_id)
            while route[-1] in paths:
                route.append(paths[route[-1]])
            return cur_distance_to_Vstart[Vend_id], route[::-1] # 返回终点到起点的最短距离，及其路径
        else:
            return float("inf"), route

def Dijkstra_with_AdjacencyList_and_heap_v4(AdjacencyList, Vcur_id, Vend_id=None, record_visited=False):
    # 相对于 Dijkstra_with_AdjacencyList_and_heap_v3， 增加了跳过部分循环
    # step1. 构造记录: 所有顶点到起点的最短距离(cur_distance_to_Vstart); 路径(path)
    cur_distance_to_Vstart = {Vcur_id:0}
    paths = {} # 路径
    Heap = [(0, Vcur_id)]# 构造堆/heap，存储(当前顶点到起点的最短距离, 当前顶点的id)
    
    if record_visited:
        list_visited = [] # 记录访问过的顶点，用于绘图
        
    while Heap and Vcur_id != Vend_id:
        
        if record_visited:
            visited_old = copy.deepcopy(cur_distance_to_Vstart.keys())
            
        # step3. 从堆顶取一个顶点，作为当前顶点（贪婪）
        cost, Vcur_id = heapq.heappop(Heap)
        # ----------------------------------------------------#
        # 与Dijkstra_with_AdjacencyList_and_heap_v3的不同之处
        if cur_distance_to_Vstart[Vcur_id] < cost: # 堆中pop出来的顶点Vcur_id，到起点的距离cost 比cur_distance_to_Vstart中的记录大，说明该点已经访问过，跳过当前循环
            continue
        # ----------------------------------------------------#
        if Vcur_id in AdjacencyList:
            for Vnext_id, dist in AdjacencyList[Vcur_id].items():
                # step 4.4.松弛
                len_cur2next = cur_distance_to_Vstart[Vcur_id]+dist
                if (Vnext_id in cur_distance_to_Vstart and len_cur2next < cur_distance_to_Vstart[Vnext_id]) or Vnext_id not in cur_distance_to_Vstart:
                    cur_distance_to_Vstart[Vnext_id] = len_cur2next
                    paths[Vnext_id] = Vcur_id # 路径,记录上一个顶点
                    heapq.heappush(Heap, (cur_distance_to_Vstart[Vnext_id], Vnext_id))
                    
        if record_visited:
            if cur_distance_to_Vstart.keys() != visited_old:
                diff = cur_distance_to_Vstart.keys() - visited_old
                list_visited.append( diff.pop() )
                
    if Vend_id == None:
        # 根据 paths 反推路径 routes
        routes = {}
        for vertice_id in cur_distance_to_Vstart.keys():
            if cur_distance_to_Vstart[vertice_id] < float("inf"):
                temp = [vertice_id]
                while temp[-1] in paths:
                    temp.append(paths[temp[-1]])
                routes[vertice_id] = temp[::-1]
            else:
                routes[vertice_id] = []   
        return cur_distance_to_Vstart, routes # 返回所有顶点到起点的最短距离，及其路径
    else:
        # 根据 paths 反推路径 route
        route = []
        if Vend_id in cur_distance_to_Vstart and cur_distance_to_Vstart[Vend_id] < float("inf"):
            route.append(Vend_id)
            while route[-1] in paths:
                route.append(paths[route[-1]])
            return cur_distance_to_Vstart[Vend_id], route[::-1] # 返回终点到起点的最短距离，及其路径
        else:
            return float("inf"), route


def Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, Vstart_id, Vend_id, directed=True):
    # 参考了 bi_dijkstra 的中止规则
    if Vstart_id == Vend_id:
        return 0, [Vend_id]
    else:
        if directed:
            # 构造反向的邻接表
            AdjacencyList_Reverse = {}
            for Vforward_id in AdjacencyList.keys():
                for Vbackward_id,cost in AdjacencyList[Vforward_id].items():
                    # print(Vforward_id, Vbackward_id, cost)
                    if Vbackward_id not in AdjacencyList_Reverse:
                        AdjacencyList_Reverse[Vbackward_id] = {Vforward_id: cost}
                    else:
                        AdjacencyList_Reverse[Vbackward_id][Vforward_id] = cost
            Adj = [AdjacencyList, AdjacencyList_Reverse] # 正向邻接表，反向邻接表
        else:
            Adj = [AdjacencyList, AdjacencyList] # 正向邻接表，正向邻接表
    
        cur_distance = [{Vstart_id: 0}, {Vend_id: 0}]  # 记录当前顶点分别到起点/终点的距离
        after_pop = [{}, {}]                           # 记录从堆中pop出的顶点到起点/终点的距离，用于中止规则
        Heap = [[(0, Vstart_id)], [(0, Vend_id)]]      # 小顶堆，记录到起点/终点的距离最近的顶点（最短距离+顶点id）
        paths = [{}, {}]                               # 记录松弛成立时的上一个顶点
        
        # 双向搜索
        finaldist = float("inf")
        finalpath = []
        forward_or_backward = 1
        while len(Heap[0]) > 0 and len(Heap[1]) > 0:
            # 前向和后向交替搜索
            forward_or_backward = 1 - forward_or_backward
            cost, Vcur_id = heapq.heappop(Heap[forward_or_backward])
    
            if Vcur_id in after_pop[forward_or_backward]: # 如果从堆中pop出的顶点再次在after_pop中出现，跳过
                continue
              
            after_pop[forward_or_backward][Vcur_id] = cost
            
            # Heap中pop出的顶点同时在after_pop[0]和after_pop[1]出现，算法中止条件
            if Vcur_id in after_pop[1-forward_or_backward]: 
                break
            
            if Vcur_id in Adj[forward_or_backward]:
                for Vnext_id, dist in Adj[forward_or_backward][Vcur_id].items():
                    dist_cur2next = cur_distance[forward_or_backward][Vcur_id] + dist
                    
                    if (Vnext_id in cur_distance[forward_or_backward] and dist_cur2next < cur_distance[forward_or_backward][Vnext_id]) or Vnext_id not in cur_distance[forward_or_backward]:
                        # relaxing
                        cur_distance[forward_or_backward][Vnext_id] = dist_cur2next
                        paths[forward_or_backward][Vnext_id] = Vcur_id
                        heapq.heappush(Heap[forward_or_backward], (dist_cur2next, Vnext_id))
                        # 更新全局最短路径
                        if Vnext_id in cur_distance[0] and Vnext_id in cur_distance[1]:
                            totaldist = cur_distance[0][Vnext_id] + cur_distance[1][Vnext_id]
                            if finaldist > totaldist:
                                finaldist = totaldist
                                path_start = [Vnext_id]
                                while path_start[-1] in paths[0]:
                                    path_start.append(paths[0][path_start[-1]])
                                path_end = [Vnext_id]
                                while path_end[-1] in paths[1]:
                                    path_end.append(paths[1][path_end[-1]])
                                finalpath = path_start[::-1]+path_end[1:]
    return finaldist, finalpath

def Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vstart_id, Vend_id, directed=True):
    # 相对于Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1， 修改了搜索方向的选择方式
    if Vstart_id == Vend_id:
        return 0, [Vend_id]
    else:
        if directed:
            # 构造反向的邻接表
            AdjacencyList_Reverse = {}
            for Vforward_id in AdjacencyList.keys():
                for Vbackward_id,cost in AdjacencyList[Vforward_id].items():
                    # print(Vforward_id, Vbackward_id, cost)
                    if Vbackward_id not in AdjacencyList_Reverse:
                        AdjacencyList_Reverse[Vbackward_id] = {Vforward_id: cost}
                    else:
                        AdjacencyList_Reverse[Vbackward_id][Vforward_id] = cost
            Adj = [AdjacencyList, AdjacencyList_Reverse]
        else:
            Adj = [AdjacencyList, AdjacencyList]
    
        cur_distance = [{Vstart_id: 0}, {Vend_id: 0}]
        scanned = [set(), set()]
        Heap = [[(0, Vstart_id)], [(0, Vend_id)]]
        paths = [{}, {}]
        
        # 双向搜索
        finaldist = float("inf")
        finalpath = []
        forward_or_backward = 1
        while len(Heap[0]) > 0 or len(Heap[1]) > 0:
            # ----------------------------------------- #
            # 选择堆元素少的方向
            if len(Heap[0]) > 0 and len(Heap[1]) > 0 and len(Heap[0]) <= len(Heap[1]):
                forward_or_backward = 0
            elif len(Heap[0]) > 0 and len(Heap[1]) > 0 and len(Heap[0]) > len(Heap[1]):
                forward_or_backward = 1
            elif len(Heap[0]) > 0 and len(Heap[1]) == 0:
                forward_or_backward = 0
            else:
                forward_or_backward = 1
            # ----------------------------------------- #
            cost, Vcur_id = heapq.heappop(Heap[forward_or_backward])
    
            if Vcur_id in scanned[forward_or_backward]:
                continue
            scanned[forward_or_backward].add(Vcur_id)
            
            # The algorithm terminates when the search in one directing selects a vertex 
            # that has been scanned in the other direction.
            if Vcur_id in scanned[1-forward_or_backward]:
                break
            
            if Vcur_id in Adj[forward_or_backward]:
                for Vnext_id, dist in Adj[forward_or_backward][Vcur_id].items():
                    dist_cur2next = cur_distance[forward_or_backward][Vcur_id] + dist
                    
                    # When an arc (v,w) is scanned by the forward search and w has already been scanned in the reversed direction, 
                    # we know the shortest s-v and w-t paths of lengths ds(v) and dt(w), respectively.
                    # If finalpath > ds(v) + l(v,w) + dt(w), we have found a shorter path than those seen before, 
                    # so we update finalpath and its path accordingly.
                    if (Vnext_id in cur_distance[forward_or_backward] and dist_cur2next < cur_distance[forward_or_backward][Vnext_id]) or Vnext_id not in cur_distance[forward_or_backward]:
                        # relaxing
                        cur_distance[forward_or_backward][Vnext_id] = dist_cur2next
                        paths[forward_or_backward][Vnext_id] = Vcur_id
                        heapq.heappush(Heap[forward_or_backward], (dist_cur2next, Vnext_id))
                        if Vnext_id in cur_distance[0] and Vnext_id in cur_distance[1]:
                            totaldist = cur_distance[0][Vnext_id] + cur_distance[1][Vnext_id]
                            if finaldist > totaldist:
                                finaldist = totaldist
                                path_start = [Vnext_id]
                                while path_start[-1] in paths[0]:
                                    path_start.append(paths[0][path_start[-1]])
                                path_end = [Vnext_id]
                                while path_end[-1] in paths[1]:
                                    path_end.append(paths[1][path_end[-1]])
                                finalpath = path_start[::-1]+path_end[1:]
    return finaldist, finalpath



def bi_dijkstra(G, source, target, weight="weight"):
    # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.bidirectional_dijkstra.html

    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    if source == target:
        return (0, [source])

    # weight = _weight_function(G, weight)
    push = heapq.heappush
    pop = heapq.heappop
    # Init:  [Forward, Backward]
    dists = [{}, {}]  # dictionary of final distances
    paths = [{source: [source]}, {target: [target]}]  # dictionary of paths
    fringe = [[], []]  # heap of (distance, node) for choosing node to expand
    seen = [{source: 0}, {target: 0}]  # dict of distances to seen nodes
    # initialize fringe heap
    push(fringe[0], (0, source))
    push(fringe[1], (0, target))
    # neighs for extracting correct neighbor information
    if G.is_directed():
        neighs = [G._succ, G._pred]
    else:
        neighs = [G._adj, G._adj]
    # variables to hold shortest discovered path
    finaldist = float("inf")
    finalpath = []
    dir = 1
    while fringe[0] and fringe[1]:
        # choose direction
        # dir == 0 is forward direction and dir == 1 is back
        dir = 1 - dir
        # extract closest to expand
        (dist, v) = pop(fringe[dir])
        if v in dists[dir]:
            # Shortest path to v has already been found
            continue
        # update distance
        dists[dir][v] = dist  # equal to seen[dir][v]
        if v in dists[1 - dir]:
            # if we have scanned v in both directions we are done
            # we have now discovered the shortest path
            return (finaldist, finalpath)

        for w, d in neighs[dir][v].items():
            if dir == 0:  # forward
                # vwLength = dists[dir][v] + weight(v, w, d)
                vwLength = dists[dir][v] + G.edges[v, w]['weight']
            else:  # back, must remember to change v,w->w,v
                # vwLength = dists[dir][v] + weight(w, v, d)
                vwLength = dists[dir][v] + G.edges[w, v]['weight']
            if w in dists[dir]:
                if vwLength < dists[dir][w]:
                    raise ValueError("Contradictory paths found: negative weights?")
            elif w not in seen[dir] or vwLength < seen[dir][w]:
                # relaxing
                seen[dir][w] = vwLength
                push(fringe[dir], (vwLength, w))
                paths[dir][w] = paths[dir][v] + [w]
                if w in seen[0] and w in seen[1]:
                    # see if this path is better than the already
                    # discovered shortest path
                    totaldist = seen[0][w] + seen[1][w]
                    if finalpath == [] or finaldist > totaldist:
                        finaldist = totaldist
                        revpath = paths[1][w][:]
                        revpath.reverse()
                        finalpath = paths[0][w] + revpath[1:]
    raise nx.NetworkXNoPath(f"No path between {source} and {target}.")

def Astar_with_AdjacencyList_and_heap_v2(AdjacencyList, dict_nodes, Vcur_id, Vend_id, record_visited=False):
    # 相对于 Dijkstra_with_AdjacencyList_and_heap_v2，修改Heap的构造及heappush
    # step1. 构造记录: 所有顶点到起点的最短距离(cur_distance_to_Vstart); 路径(path)
    cur_distance_to_Vstart = {Vcur_id:0}
    paths = {} # 路径
    set_visited = set()
    
    # 构造堆/heap，存储(当前顶点到起点的最短距离, 当前顶点的id)
    Heap = [(0+distance_to_target(dict_nodes,Vcur_id,Vend_id), Vcur_id)] # 与 Dijkstra_with_AdjacencyList_and_heap_v2 的不同之处
    
    if record_visited:
        list_visited = [] # 记录访问过的顶点，用于绘图
    
    while Heap and Vcur_id != Vend_id:
        
        if record_visited:
            set_visited_old = copy.deepcopy(set_visited)
                    
        # step3. 从堆顶取一个顶点，作为当前顶点（贪婪）
        cost, Vcur_id = heapq.heappop(Heap)
        if Vcur_id not in set_visited: # 如果当前顶点未被访问过
        
            # step 4.1.从未访问顶点集合移除当前顶点
            set_visited.add(Vcur_id)
            # step 4.2.如果当前顶点在邻接表中
            if Vcur_id in AdjacencyList:
                for Vnext_id, dist in AdjacencyList[Vcur_id].items():
                    # step 4.3.如果与当前顶点相连的顶点未被访问过
                    if Vnext_id not in set_visited:
                        # step 4.4.松弛
                        len_cur2next = cur_distance_to_Vstart[Vcur_id]+dist
                        if (Vnext_id in cur_distance_to_Vstart and len_cur2next < cur_distance_to_Vstart[Vnext_id]) or Vnext_id not in cur_distance_to_Vstart:
                            cur_distance_to_Vstart[Vnext_id] = len_cur2next
                            paths[Vnext_id] = Vcur_id # 路径,记录上一个顶点
                            heapq.heappush(Heap, (cur_distance_to_Vstart[Vnext_id]+distance_to_target(dict_nodes,Vnext_id,Vend_id), Vnext_id))   # 与 Dijkstra_with_AdjacencyList_and_heap_v2 的不同之处
                                
        if record_visited:
            if set_visited != set_visited_old:
                set_diff = set_visited - set_visited_old
                list_visited.append( set_diff.pop() )
    
    # 根据 paths 反推路径 route
    route = []
    if Vend_id in cur_distance_to_Vstart and cur_distance_to_Vstart[Vend_id] < float("inf"):
        route.append(Vend_id)
        while route[-1] in paths:
            route.append(paths[route[-1]])
        return cur_distance_to_Vstart[Vend_id], route[::-1] # 返回终点到起点的最短距离，及其路径
    else:
        return float("inf"), route

def Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, Vcur_id, Vend_id, record_visited=False):
    # 相对于 Dijkstra_with_AdjacencyList_and_heap_v3，修改Heap的构造及heappush
    # 相对于 Astar_with_AdjacencyList_and_heap_v2，  移除set_visited，并将其功能整合到cur_distance_to_Vstart
    # step1. 构造记录: 所有顶点到起点的最短距离(cur_distance_to_Vstart); 路径(path)
    cur_distance_to_Vstart = {Vcur_id:0}
    paths = {} # 路径    
    # 构造堆/heap，存储(当前顶点到起点的最短距离, 当前顶点的id)
    Heap = [(0+distance_to_target(dict_nodes,Vcur_id,Vend_id), Vcur_id)] # 与 Dijkstra_with_AdjacencyList_and_heap_v3 的不同之处
    
    if record_visited:
        list_visited = [] # 记录访问过的顶点，用于绘图
    
    while Heap and Vcur_id != Vend_id:
        
        if record_visited:
            visited_old = copy.deepcopy(cur_distance_to_Vstart.keys())
                    
        # step3. 从堆顶取一个顶点，作为当前顶点（贪婪）
        cost, Vcur_id = heapq.heappop(Heap)
        
        # step 4.2.如果当前顶点在邻接表中
        if Vcur_id in AdjacencyList:
            for Vnext_id, dist in AdjacencyList[Vcur_id].items():
                # step 4.4.松弛
                len_cur2next = cur_distance_to_Vstart[Vcur_id]+dist
                if (Vnext_id in cur_distance_to_Vstart and len_cur2next < cur_distance_to_Vstart[Vnext_id]) or Vnext_id not in cur_distance_to_Vstart:
                    cur_distance_to_Vstart[Vnext_id] = len_cur2next
                    paths[Vnext_id] = Vcur_id # 路径,记录上一个顶点
                    heapq.heappush(Heap, (cur_distance_to_Vstart[Vnext_id]+distance_to_target(dict_nodes,Vnext_id,Vend_id), Vnext_id))        # 与 Dijkstra_with_AdjacencyList_and_heap_v3 的不同之处
                                
        if record_visited:
            if cur_distance_to_Vstart.keys() != visited_old:
                diff = cur_distance_to_Vstart.keys() - visited_old
                list_visited.append( diff.pop() )
    
    # 根据 paths 反推路径 route
    route = []
    if Vend_id in cur_distance_to_Vstart and cur_distance_to_Vstart[Vend_id] < float("inf"):
        route.append(Vend_id)
        while route[-1] in paths:
            route.append(paths[route[-1]])
        return cur_distance_to_Vstart[Vend_id], route[::-1] # 返回终点到起点的最短距离，及其路径
    else:
        return float("inf"), route


def Bidirectional_Astar_with_AdjacencyList_and_heap_v2(AdjacencyList, dict_nodes, Vstart_id, Vend_id, directed=True):
    # Symmetric Approach
    # 相对于 Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2， 修改了搜索方向的选择方式
    # 相对于 Bidirectional_Astar_with_AdjacencyList_and_heap_v1， 修改了搜索方向的选择方式
    if Vstart_id == Vend_id:
        return 0, [Vend_id]
    else:
        if directed:
            # 构造反向的邻接表
            AdjacencyList_Reverse = {}
            for Vforward_id in AdjacencyList.keys():
                for Vbackward_id,cost in AdjacencyList[Vforward_id].items():
                    # print(Vforward_id, Vbackward_id, cost)
                    if Vbackward_id not in AdjacencyList_Reverse:
                        AdjacencyList_Reverse[Vbackward_id] = {Vforward_id: cost}
                    else:
                        AdjacencyList_Reverse[Vbackward_id][Vforward_id] = cost
            Adj = [AdjacencyList, AdjacencyList_Reverse]
        else:
            Adj = [AdjacencyList, AdjacencyList]
    
        cur_distance = [{Vstart_id: 0}, {Vend_id: 0}]
        scanned = [{}, {}]
        # ------------------------------------ #
        Heap = [[(0+distance_to_target(dict_nodes,Vstart_id,Vend_id), Vstart_id)],
                [(0+distance_to_target(dict_nodes,Vend_id,Vstart_id), Vend_id)]]
        # ------------------------------------ #
        paths = [{}, {}]
        
        # 双向搜索
        finaldist = float("inf")
        finalpath = []
        forward_or_backward = 1
        while len(Heap[0]) > 0 or len(Heap[1]) > 0:
            # ----------------------------------------- #
            # 选择堆元素少的方向
            if len(Heap[0]) > 0 and len(Heap[1]) > 0 and len(Heap[0]) <= len(Heap[1]):
                forward_or_backward = 0
            elif len(Heap[0]) > 0 and len(Heap[1]) > 0 and len(Heap[0]) > len(Heap[1]):
                forward_or_backward = 1
            elif len(Heap[0]) > 0 and len(Heap[1]) == 0:
                forward_or_backward = 0
            else:
                forward_or_backward = 1
            # ----------------------------------------- #
            cost, Vcur_id = heapq.heappop(Heap[forward_or_backward])
    
            if Vcur_id in scanned[forward_or_backward]:
                continue
            scanned[forward_or_backward][Vcur_id] = cost
            
            # 中止准则
            # Stop when one of the searches is about to scan a vertex v with dist(s,v) + Pi(v,t) >= finaldist 
            # or when both searches have no labeled vertices. Pi(v,t) gives an estimate on the distance from v to t.
            if forward_or_backward == 0 and cur_distance[0][Vcur_id] + distance_to_target(dict_nodes,Vcur_id,Vend_id) >= finaldist:
                break
            elif forward_or_backward == 1 and cur_distance[1][Vcur_id] + distance_to_target(dict_nodes,Vcur_id,Vstart_id) >= finaldist:
                break
                
            if Vcur_id in Adj[forward_or_backward]:
                for Vnext_id, dist in Adj[forward_or_backward][Vcur_id].items():
                    dist_cur2next = cur_distance[forward_or_backward][Vcur_id] + dist
                    
                    if (Vnext_id in cur_distance[forward_or_backward] and dist_cur2next < cur_distance[forward_or_backward][Vnext_id]) or Vnext_id not in cur_distance[forward_or_backward]:
                        # relaxing
                        cur_distance[forward_or_backward][Vnext_id] = dist_cur2next
                        paths[forward_or_backward][Vnext_id] = Vcur_id
                        # ------------------------------------ #
                        if forward_or_backward == 0:
                            heapq.heappush(Heap[0], (dist_cur2next+distance_to_target(dict_nodes,Vnext_id,Vend_id), Vnext_id))
                        else:
                            heapq.heappush(Heap[1], (dist_cur2next+distance_to_target(dict_nodes,Vnext_id,Vstart_id), Vnext_id))
                        # ------------------------------------ #
                        if Vnext_id in cur_distance[0] and Vnext_id in cur_distance[1]:
                            totaldist = cur_distance[0][Vnext_id] + cur_distance[1][Vnext_id]
                            if finaldist > totaldist:
                                finaldist = totaldist
                                path_start = [Vnext_id]
                                while path_start[-1] in paths[0]:
                                    path_start.append(paths[0][path_start[-1]])
                                path_end = [Vnext_id]
                                while path_end[-1] in paths[1]:
                                    path_end.append(paths[1][path_end[-1]])
                                finalpath = path_start[::-1]+path_end[1:]
    return finaldist, finalpath

#-----------------------------------------------------------------------------#
# 2. TSP and VRP

# 插0法求解VRP<所有>可行解
def insert0_of_vrp(list_node, num_car):
    list_solution = []
    for perm in permutations(list_node, len(list_node)):
        for comb in combinations([ii+1 for ii in range(len(list_node)-1)],num_car-1):
            perm2 = list(perm)
            comb2 = list(comb)
            comb2.append(len(list_node))
            solution = []
            for ii in range(len(comb2)):
                if ii == 0:
                    solution.append(perm2[0:comb2[ii]])
                else:
                    solution.append(perm2[comb2[ii-1]:comb2[ii]])
            list_solution.append(solution)
    return list_solution

#-----------------------------------------------------------------------------#
# 绘图

# 绘制主要的连通highway
def draw_osm(ax0, dict_highways, dict_nodes, color):
    for highway_id, nodes_id in dict_highways.items():
        seq_lat = []
        seq_lon = []
        for node_id in nodes_id:
            seq_lat.append(dict_nodes[node_id][0])
            seq_lon.append(dict_nodes[node_id][1])
        ax0.plot(seq_lon, seq_lat, color=color, linewidth=1)

# 绘制一条路径
def draw_path(ax0, dict_nodes, path, color, size):
    seq_lat = []
    seq_lon = []
    for node_id in path:
        seq_lat.append(dict_nodes[node_id][0])
        seq_lon.append(dict_nodes[node_id][1])
    ax0.plot(seq_lon, seq_lat, color=color, linewidth=6)
    ax0.scatter([seq_lon[0],seq_lon[-1]], [seq_lat[0],seq_lat[-1]], s=size, c=color, marker="*")

