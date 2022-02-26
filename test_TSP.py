# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 22:40:44 2021

@author: CC-i7-11700
"""
# 索引到排列的哈希映射 应用到 TSP求解

from route import *
import time
import random

#-----------------------------------------------------------------------------#
# seq = [num+1 for num in range(4)]
# label = True
# for index in range(math.factorial(len(seq))):
#     perm1 = index_to_perm(index, seq)
#     perm2 = index2perm(index, seq, len(seq))
#     print(index, perm1, perm2)
#     label = label and (perm1 == perm2)
# print("验证索引到排列的哈希映射", label)
#-----------------------------------------------------------------------------#
# # 测试1：随机生成
# import math
# num_vertex = 20
# matrix = [[float("inf")]*num_vertex for _ in range(num_vertex)]
# for ii in range(num_vertex):
#     for jj in range(num_vertex):
#         if ii != jj:
#             matrix[ii][jj] = random.randint(0, 100)

# vertexes_id = [num for num in range(num_vertex)]
# total = math.factorial(num_vertex)
# step = 10**13
# # step = 10**12

# start = time.time()
# cost_opt = float("inf")
# path_opt = []
# for index in range(0, total, step):
#     path = index2perm(index,vertexes_id,len(vertexes_id))
#     # print(index, path)
#     cost_cur = 0
#     for jj in range(len(path)-1):
#         cost_cur += matrix[path[jj]][path[jj+1]]
#     cost_cur += matrix[path[-1]][path[0]]
#     if cost_cur < cost_opt:
#         cost_opt = cost_cur
#         path_opt = path
# end = time.time()
# print("最优值", cost_opt)
# print("最优路径", path_opt)
# print("计算时间:", end-start)

#-----------------------------------------------------------------------------#
# 测试2：上海市路网
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

num_vertex = 10
vertexes_id = random.sample(list(dict_nodes.keys()), k=num_vertex)

start = time.time()    
matrix = [[float("inf")]*num_vertex for _ in range(num_vertex)]
for ii in range(num_vertex):
    for jj in range(num_vertex):
        if ii != jj:
            matrix[ii][jj], temp = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, vertexes_id[ii], vertexes_id[jj], False)
end = time.time()
print("邻接矩阵耗时:", end-start)
dict_vertex_id2index = {}
for ii in range(len(vertexes_id)):
    dict_vertex_id2index[vertexes_id[ii]] = ii

total = math.factorial(num_vertex)
step = 1
start = time.time()
cost_opt = float("inf")
path_opt = []
for index in range(0, total, step):
    path = index2perm(index,vertexes_id,len(vertexes_id))
    # print(index, path)
    cost_cur = 0
    for jj in range(len(path)-1):
        cost_cur += matrix[dict_vertex_id2index[path[jj]]][dict_vertex_id2index[path[jj+1]]]
    cost_cur += matrix[dict_vertex_id2index[path[-1]]][dict_vertex_id2index[path[0]]]
    if cost_cur < cost_opt:
        cost_opt = cost_cur
        path_opt = path
end = time.time()
print("最优值", cost_opt)
print("最优路径", path_opt)
print("TSP计算时间:", end-start)


# import copy
# tsp_path = copy.deepcopy(path_opt)

# -------- #
import matplotlib.pyplot as plt
color3 = ["#807A7A", "#E2E1E6", "#2286A9"]
plt.close()
fig = plt.figure(figsize=(40, 40))
ax0 = fig.add_subplot(111)

# 绘制地图
draw_osm(ax0, dict_highways, dict_nodes, color3[0])
for ii in range(len(path_opt)):
    temp, path = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, path_opt[ii%len(path_opt)], path_opt[(ii+1)%len(path_opt)], False)
    if ii%2 == 0:
        draw_path(ax0, dict_nodes, path, "red", 200)
    else:
        draw_path(ax0, dict_nodes, path, color3[2], 200)
        
ax0.set_title("Connected highways (num_ways = "+str(len(dict_highways))+", num_nodes = "+str(len(dict_nodes))+")\nnum_vertex_of_TSP ="+str(num_vertex), loc='center', fontsize=20)
