# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 00:25:05 2022

@author: CC-i7-11700
"""
# 目的：在上海市道路网中检验算法的准确性
from route import *
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

# upper_right_id = "-1"
# upper_right_value = -float("inf")
# lower_left_id = "-1"
# lower_left_value = float("inf")

# upper_left_id = "-1"
# upper_left_value = float("inf")
# lower_right_id = "-1"
# lower_right_value = -float("inf")

# for key, value in dict_nodes.items():
#     # print(value[1], value[0]) # 经度，纬度
#     if value[1] + value[0] > upper_right_value:
#         upper_right_id = key
#         upper_right_value = value[1] + value[0]
#     if value[1] + value[0] < lower_left_value:
#         lower_left_id = key
#         lower_left_value = value[1] + value[0]
#     if value[1] - value[0] < upper_left_value:
#         upper_left_id = key
#         upper_left_value = value[1] - value[0]
#     if value[1] - value[0] > lower_right_value:
#         lower_right_id = key
#         lower_right_value = value[1] - value[0]

# print(upper_right_id, dict_nodes[upper_right_id])
# print(lower_left_id, dict_nodes[lower_left_id])
# print(upper_left_id, dict_nodes[upper_left_id])
# print(lower_right_id, dict_nodes[lower_right_id])


# top_id = "-1"
# top_value = float("inf")
# down_id = "-1"
# down_value = float("inf")
# for key, value in dict_nodes.items():
#     if (value[1]-121.3)**2 + (value[0]-31.5)**2 < top_value:
#         top_id = key
#         top_value = (value[1]-121.3)**2 + (value[0]-31.5)**2
#     if (value[1]-121.3)**2 + (value[0]-30.7)**2 < down_value:
#         down_id = key
#         down_value = (value[1]-121.3)**2 + (value[0]-30.7)**2


# Vstart_id, Vend_id = '1063104783', '7184053847'
# Vstart_id, Vend_id = upper_right_id, lower_left_id
# Vstart_id, Vend_id = '5006175603', '8082913409'

# Vstart_id, Vend_id = upper_left_id, lower_right_id
# Vstart_id, Vend_id = '9231267230', '86736851'


# Vstart_id, Vend_id = '1871453155', '8082913409'
# Vstart_id, Vend_id = top_id, down_id
# Vstart_id, Vend_id = '1221180777', '3569107894'


# Vstart_id, Vend_id = '5097149489', '7553321341'
# Vstart_id, Vend_id = '4780181032', '6480579419' # 存在两条最优路径
# Vstart_id, Vend_id = '3076119106', '6034063363'
# Vstart_id, Vend_id = '1671589395', '64849294'
Vstart_id, Vend_id = '3573834815', '9042536033'


#-----------------------------------------------------------------------------#
record_visited = False
directed = True

# start = time.time()
# cost21, path21 = Dijkstra_with_AdjacencyList(AdjacencyList, set(dict_nodes.keys()), Vstart_id, Vend_id)
# end = time.time()
# time21 = end-start

start = time.time()
cost00, path00 = Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, set(dict_nodes.keys()), Vstart_id, Vend_id)
end = time.time()
time00 = end-start

start = time.time()
cost01, path01 = Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vstart_id, Vend_id, record_visited)
end = time.time()
time01 = end-start

start = time.time()
cost02, path02 = Dijkstra_with_AdjacencyList_and_heap_v3(AdjacencyList, Vstart_id, Vend_id, record_visited)
end = time.time()
time02 = end-start

start = time.time()
cost03, path03 = Dijkstra_with_AdjacencyList_and_heap_v4(AdjacencyList, Vstart_id, Vend_id, record_visited)
end = time.time()
time03 = end-start

start = time.time()
cost04, path04 = Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1(AdjacencyList, Vstart_id, Vend_id, directed)
end = time.time()
time04 = end-start

start = time.time()
cost05, path05 = Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2(AdjacencyList, Vstart_id, Vend_id, directed)
end = time.time()
time05 = end-start

start = time.time()
cost06, path06 = Astar_with_AdjacencyList_and_heap_v2(AdjacencyList, dict_nodes, Vstart_id, Vend_id, record_visited)
end = time.time()
time06 = end-start

start = time.time()
cost07, path07 = Astar_with_AdjacencyList_and_heap_v3(AdjacencyList, dict_nodes, Vstart_id, Vend_id, record_visited)
end = time.time()
time07 = end-start

# start = time.time()
# cost08, path08 = Astar_with_AdjacencyList_and_heap_v4(AdjacencyList, dict_nodes, Vstart_id, Vend_id, record_visited)
# end = time.time()
# time08 = end-start

# start = time.time()
# cost09, path09 = Bidirectional_Astar_with_AdjacencyList_and_heap_v1(AdjacencyList, dict_nodes, Vstart_id, Vend_id, directed=True)
# end = time.time()
# time09 = end-start


start = time.time()
cost10, path10 = Bidirectional_Astar_with_AdjacencyList_and_heap_v2(AdjacencyList, dict_nodes, Vstart_id, Vend_id, directed=True)
end = time.time()
time10 = end-start

# print("Dijkstra_with_AdjacencyList", cost22, time21)
print("Dijkstra_with_AdjacencyList_and_heap_v1", time00)
print("Dijkstra_with_AdjacencyList_and_heap_v2", time01)
print("Dijkstra_with_AdjacencyList_and_heap_v3", time02)
print("Dijkstra_with_AdjacencyList_and_heap_v4", time03)
print("Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v1", time04)
print("Bidirectional_Dijkstra_with_AdjacencyList_and_heap_v2", time05)
print("Astar_with_AdjacencyList_and_heap_v2", time06)
print("Astar_with_AdjacencyList_and_heap_v3", time07)
# print("Astar_with_AdjacencyList_and_heap_v4\n", cost08, time08)
# print("Bidirectional_Astar_with_AdjacencyList_and_heap_v1\n", cost09, time09)
print("Bidirectional_Astar_with_AdjacencyList_and_heap_v2", time10)


# print("路径检验", path00 == path01 == path02 == path03 == path04 == path05 == path06 == path07 == path10)
# num_decimal = 12
# print("cost检验", round(cost00,num_decimal) == round(cost01,num_decimal) == round(cost02,num_decimal)
#       == round(cost03,num_decimal) == round(cost04,num_decimal) == round(cost05,num_decimal) 
#       == round(cost06,num_decimal) == round(cost07,num_decimal) == round(cost10,num_decimal))

def check_isometric(path1, path2):
    cost1 = 0
    for ii in range(len(path1)-1):
        cost1 += distance_to_target(dict_nodes, path1[ii], path1[ii+1])
    cost2 = 0
    for ii in range(len(path2)-1):
        cost2 += distance_to_target(dict_nodes, path2[ii], path2[ii+1])
    return cost1 == cost2

label = True
label = label and check_isometric(path00,path01)
label = label and check_isometric(path00,path02)
label = label and check_isometric(path00,path03)
label = label and check_isometric(path00,path04)
label = label and check_isometric(path00,path05)
label = label and check_isometric(path00,path06)
label = label and check_isometric(path00,path07)
label = label and check_isometric(path00,path10)
print("检验",label)


#-----------------------------------------------------------------------------#
# import matplotlib.pyplot as plt
# color3 = ["#807A7A", "#E2E1E6", "#2286A9"]

# plt.close()
# fig = plt.figure(figsize=(40, 40))
# ax0 = fig.add_subplot(111)

# # 绘制地图
# draw_osm(ax0, dict_highways, dict_nodes, color3[0])
# draw_path(ax0, dict_nodes, path00, "red", 200)
# draw_path(ax0, dict_nodes, path41, color3[1], 200)
# draw_path(ax0, dict_nodes, path42, color3[2], 200)



