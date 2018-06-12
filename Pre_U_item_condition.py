#coding:utf-8
#__author__ = G

import numpy as np

# calculate knowledgement
def Fund_Q(Q_no, dataQi):
    i = 0
    while i<dataQi.shape[0]:
        if Q_no == dataQi[i][0]:
            return i
        i += 1
    return 0
    # raise Exception("Invalid level!"， Fund_Q)

dataQi = np.load('data/dataQiN.npy')
dataUq = np.load('data/dataUqN.npy')
#print(dataQi)
MAXQ = 9946
MAXU = 526
MAXITEM = 164 # no "0"
U_condition = np.zeros([MAXU, MAXITEM])
for ele in dataUq:
    if int(ele[2]) == 1:
        Q_no = int(ele[1])
        Q_location = Fund_Q(Q_no, dataQi)
        x = int(ele[0]) - 1
        #print(dataQi[Q_location][1])
        y = int(dataQi[Q_location][1])
        if U_condition[x][y] == 0:
            U_condition[x][y] = 1
np.save('data/U_condition', U_condition)
print(1)

# calculate relationship
def U_U(U1, U2, Ui_condition):
    in_count = 0
    sum_count = 0
    for i in range(MAXITEM-1):
        i += 1
        if Ui_condition[U1][i] == 1:
            sum_count += 1
            if Ui_condition[U2][i] ==1:
                in_count += 1

        else:
            if Ui_condition[U2][i] ==1:
                sum_count += 1
    return in_count / sum_count if sum_count != 0 else 0
                


Ui_condition = np.load('data/U_condition.npy')

MAXU = 526
UU_condition = np.zeros([MAXU, MAXU])
for i in range(MAXU):
    for j in range(MAXU):
        UU_condition[i][j] = U_U(i, j, Ui_condition)

np.save('data/UU_condition', UU_condition)


'''
# 邻域（用户）算法计算推荐list
MAXCANDIDATE = 10
U_condition = np.load('data/U_condition.npy')
UU_condition = np.load('data/UU_condition.npy')
candidate_list = np.zeros(MAXU, MAXCANDIDATE)

def Pick_10U(ele):
    max_10 = np.zeros([10, 2]) # min in 0
    for index, val in enumerate(ele): # index:U_id, val:相似程度
        if val > max_10[0][1]:
            max_10[0][0], max_10[0][1] = index, val
            j = 1
            #重新有序化
            while j < 10:
                if val > max_10[j][1]:
                    max_10[j-1] = max_10[j]
                    max_10[j] = index, val
                else:
                    break
    return(max_10)

def cal_interest_item(max_10, U_condition):
    cur = np.zeros(163)
    for i in max_10:
        for index, j in enumerate(U_condition[int(i[0])]):
            if j:
                cur[index] += j*i[1]
    return(Pick_10U(cur))

U_calculate_list = np.zeros([MAXU, 10])

for index, ele in enumerate(UU_condition):
    max_10U = Pick_10U(ele)
    U_calculate_list[index] = cal_interest_item(max_10U, U_condition)

np.save('data/U_calculate_list',U_calculate_list)
'''