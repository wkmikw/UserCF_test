#coding=utf-8
#python recommend_list.py

import numpy as np
import math
# 邻域（用户）算法计算推荐list
MAXQ = 9946
MAXU = 526
MAXITEM = 164 # no "0"
MAXCANDIDATE = 10

U_condition = np.load('data/U_condition.npy')
UU_condition = np.load('data/UU_condition.npy')
candidate_list = np.zeros([MAXU, MAXCANDIDATE])

def Pick_10U(ele, U_id):
    max_10 = np.zeros([10, 2]) # min in 0
    for index, val in enumerate(ele): # index:U_id, val:相似程度
        if index != U_id: # 除掉自身
            if val > max_10[0][1]:
                max_10[0][0], max_10[0][1] = index, val
                j = 1
                #重新有序化
                while j < 10:
                    if val > max_10[j][1]:
                        max_10[j-1] = max_10[j]
                        max_10[j] = index, val
                        j += 1
                    else:
                        break
    return(max_10)

def Pick_10item(ele):
    max_10 = np.zeros([10, 2]) # min in 0
    for index, val in enumerate(ele): # index:U_id, val:相似程度
        if val > max_10[0][1]:
            max_10[0] = [index, val]
            j = 1
            #重新有序化
            while j < 10:
                if val > max_10[j][1]:
                    max_10[j-1] = max_10[j]
                    max_10[j] = index, val
                    j += 1
                else:
                    break
    return(max_10)

def cal_interest_item(max_10, U_condition, U_id):
    item_interest = np.zeros(MAXITEM)
    #是否做过
    label = U_condition[U_id]
    for i in max_10:
        for index, j in enumerate(U_condition[int(i[0])]):
            if j and label[index] != 1:
                item_interest[index] += j*i[1]
    return(Pick_10item(item_interest))

def cal_interest_item_pop(max_10, U_condition, U_id):
    item_interest = np.zeros(MAXITEM)
    popular = np.load('data/item_popular_multi_P.npy')
    #是否做过
    label = U_condition[U_id]
    for i in max_10:
        for index, j in enumerate(U_condition[int(i[0])]):
            if j and label[index] != 1:
                item_interest[index] += j*i[1] / math.log(1 + popular[index])
    return(Pick_10item(item_interest))


U_calculate_list = np.zeros([MAXU, 10])
U_calculate_list_pop = np.zeros([MAXU, 10])
# 普通CF_User
for index, ele in enumerate(UU_condition):
    max_10U = Pick_10U(ele, index)
    temp = cal_interest_item(max_10U, U_condition, index)
    temp = temp.T
    U_calculate_list[index] = temp[0]

np.save('data/U_calculate_list',U_calculate_list)
#print(U_calculate_list[::20])
print(1)

#print('\n\n\n')
# 考虑流行度
for index, ele in enumerate(UU_condition):
    max_10U = Pick_10U(ele, index)
    temp = cal_interest_item_pop(max_10U, U_condition, index)
    temp = temp.T
    U_calculate_list_pop[index] = temp[0]
#print(U_calculate_list[::20])
print(2)
'''
# 比较是否考虑流行度影响
U_calculate_list_compare = np.zeros([MAXU*2, 10])
for i in range(MAXU):
    U_calculate_list_compare[i*2] = U_calculate_list[i]
    U_calculate_list_compare[i*2+1] = U_calculate_list_pop[i]
for i in range(MAXU*2):
    if np.sum(U_calculate_list_compare[i]) != 0:
        print(U_calculate_list_compare[i])
'''