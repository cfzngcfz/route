# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 20:36:04 2022

@author: CC-i7-11700
"""
from route import *
from itertools import permutations,combinations
import math
import time
import random 
#-----------------------------------------------------------------------------#
# # 验证索引到组合的哈希映射
# num_set = 9
# num_selection = 5
# seq = [ii+1 for ii in range(num_set)]

# index = 0
# label = True
# for comb in combinations(seq, num_selection):
#     # print(index, list(comb))
#     temp = index2comb(index, seq, num_selection)
#     label = label and (temp == list(comb))
#     print(index, temp)
#     index += 1
# print("是否与combinations结果一致", label)

#-----------------------------------------------------------------------------#
# # 验证索引到排列的哈希映射
# num_set = 9
# num_selection = 3
# seq = [ii+1 for ii in range(num_set)]

# index = 0
# label = True
# for perm in permutations(seq, num_selection):
#     # print(index, list(perm))
#     temp = index2perm(index, seq, num_selection)
#     label = label and (temp == list(perm))
#     print(index, temp)
#     index += 1
# print("是否与permutations结果一致", label)
#-----------------------------------------------------------------------------#
# # 验证索引到VRP可行解
# num_node = 5
# num_car = 3
# list_node = [ii+1 for ii in range(num_node)]
# index2vrp(2, list_node, num_car)

# start = time.time()
# set_insert0 = set()
# list_solution = insert0_of_vrp(list_node, num_car)
# for solution in list_solution:
#     solution.sort()
#     set_insert0.add(tuple([tuple(solu) for solu in solution]))
# end = time.time()
# print("插0法可行解重复的倍数", len(list_solution)/len(set_insert0))
# print("插0法耗时:",end-start)


# start = time.time()
# total = int(math.factorial(len(list_node)-1)/math.factorial(num_car-1)/math.factorial(len(list_node)-num_car))*int(math.factorial(len(list_node))/math.factorial(num_car))
# set_hash = set()
# for index in range(total):
#     solution = index2vrp(index, list_node, num_car)
#     set_hash.add(tuple([tuple(solu) for solu in solution]))
# end = time.time()
# print("索引到VRP可行解验证",set_insert0 == set_hash)
# print("可行解哈希算法耗时:",end-start)    

#-----------------------------------------------------------------------------#
# # 排列组合哈希法和插0法的对比记录
# import csv
# path = "vrp.csv"
# header = ["num_node", "num_car", "repeat", "time of insert 0", "time of permutation and combination hash", "compare"]
# with open(path, 'w', newline='', encoding="utf-8") as file: # 默认encoding='gbk'
#     spreadsheet = csv.writer(file, delimiter=',')
#     spreadsheet.writerow(header) 
        
#     for num_node in range(6,10):
#         for num_car in range(2,num_node):
#             record = []

#             print("num_node =",num_node,"; num_car =",num_car)
#             record.append(num_node)
#             record.append(num_car)
#             list_node = [ii+1 for ii in range(num_node)]
            
#             start = time.time()
#             set_insert0 = set()
#             list_solution = insert0_of_vrp(list_node, num_car)
#             for solution in list_solution:
#                 solution.sort()
#                 set_insert0.add(tuple([tuple(solu) for solu in solution]))
#             end = time.time()
#             print("插0法可行解重复的倍数", len(list_solution)/len(set_insert0))
#             print("插0法耗时:",end-start)
#             record.append(len(list_solution)/len(set_insert0))
#             record.append(end-start)
            
#             start = time.time()
#             total = int(math.factorial(len(list_node)-1)/math.factorial(num_car-1)/math.factorial(len(list_node)-num_car))*int(math.factorial(len(list_node))/math.factorial(num_car))
#             set_hash = set()
#             for index in range(total):
#                 solution = index2vrp(index, list_node, num_car)
#                 set_hash.add(tuple([tuple(solu) for solu in solution]))
#             end = time.time()
#             print("可行解哈希算法耗时:",end-start)
#             print("索引到VRP可行解验证",set_insert0 == set_hash)
#             record.append(end-start)
#             record.append(set_insert0 == set_hash)
#             spreadsheet.writerow(record)
#-----------------------------------------------------------------------------#
# 根据经纬度寻找顶点
def search_vertex_id(longitude,latitude):
    target_id = "-1"
    target_value = float("inf")
    for key, value in dict_nodes.items():
        if (value[1]-longitude)**2 + (value[0]-latitude)**2 < target_value:
            target_id = key
            target_value = (value[1]-longitude)**2 + (value[0]-latitude)**2
    return target_id


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
num_car = 4
vertexes_id = random.sample(list(dict_nodes.keys()), k=num_vertex)
# vertexes_id = [search_vertex_id(121.1,31.0), search_vertex_id(121.2,31.2),
#                search_vertex_id(121.2,30.9), search_vertex_id(121.3,31.3),
#                search_vertex_id(121.5,30.9), search_vertex_id(121.5,31.3),
#                search_vertex_id(121.6,31.0), search_vertex_id(121.6,31.2)] # 特例
center_id = search_vertex_id(121.4,31.1) # 中心点

# 计算任意两点之间的距离
start = time.time()    
matrix = [[float("inf")]*(num_vertex+1) for _ in range(num_vertex+1)]
for ii in range(num_vertex+1):
    for jj in range(num_vertex+1):
        if ii != jj:
            if ii == 0:
                matrix[ii][jj], temp = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, center_id, vertexes_id[jj-1], False)
            elif jj == 0:
                matrix[ii][jj], temp = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, vertexes_id[ii-1], center_id, False)
            else:
                matrix[ii][jj], temp = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, vertexes_id[ii-1], vertexes_id[jj-1], False)
end = time.time()
print("邻接矩阵耗时:", end-start)

# 顶点id到index的映射
dict_vertex_id2index = {}
for ii in range(num_vertex):
    dict_vertex_id2index[vertexes_id[ii]] = ii+1
dict_vertex_id2index[center_id] = 0



start = time.time()
list_node = [ii+1 for ii in range(num_vertex)]
cost_opt = float("inf")
paths_opt = []
total = int(math.factorial(num_vertex-1)/math.factorial(num_car-1)/math.factorial(num_vertex-num_car))*int(math.factorial(num_vertex)/math.factorial(num_car))
for index in range(total):
    solution = index2vrp(index, list_node, num_car)
    
    cost_cur = 0
    # index转化为id
    solution2 = []
    for car in solution:
        path = [center_id] # 起点
        for vertex_index in car:
            path.append(vertexes_id[vertex_index-1])
        solution2.append(path)
        
        for jj in range(len(path)-1):
            cost_cur += matrix[dict_vertex_id2index[path[jj]]][dict_vertex_id2index[path[jj+1]]]
        cost_cur += matrix[dict_vertex_id2index[path[-1]]][dict_vertex_id2index[path[0]]] # 回到起点
        
    if cost_cur < cost_opt:
        cost_opt = cost_cur
        paths_opt = solution2
    # if index%1000 == 0:
    #     print(index, cost_opt)
end = time.time()
print("最优值", cost_opt)
print("最优路径", paths_opt)
print("VRP计算时间:", end-start)


# import copy
# vrp_opt = copy.deepcopy(paths_opt)
# vrp_opt == paths_opt

# -------- #
import matplotlib.pyplot as plt
color3 = ["#807A7A", "#E2E1E6", "#2286A9"]
color_default = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']
plt.close()
fig = plt.figure(figsize=(40, 40))
ax0 = fig.add_subplot(111)

# 绘制地图
draw_osm(ax0, dict_highways, dict_nodes, color3[0])

for jj in range(len(paths_opt)):
    for ii in range(len(paths_opt[jj])):
        temp, path = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, paths_opt[jj][ii%len(paths_opt[jj])], paths_opt[jj][(ii+1)%len(paths_opt[jj])], False)
        draw_path(ax0, dict_nodes, path, color_default[jj], 200)
ax0.scatter([dict_nodes[center_id][1],], [dict_nodes[center_id][0],], s=500, c="black", marker="o")
ax0.set_title("Connected highways (num_ways = "+str(len(dict_highways))+", num_nodes = "+str(len(dict_nodes))+")\nnum_vertex_of_VRP = "+str(num_vertex+1)+" num_car = "+str(num_car), loc='center', fontsize=20)
