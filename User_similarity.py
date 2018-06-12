# coding:utf-8
# __author__ = GaoY
# python

import numpy as np
import math
from filter import SplitData
from attach_difficulty import attach_difficulty

MAXQ = 3911
MAXU = 50
MAXITEM = 10

test, train = SplitData(9, 5, 1)
test = np.array(test)
train = np.array(train)
dataQi = attach_difficulty()  # [题号， 知识点， 难度]
S_cal = np.zeros([MAXU, MAXITEM, 2], dtype=float)  # [难度加权，count]
dif = [1., 1.25, 1.5, 1.75, 2.]

# 计算难度加权能力值
for ele in train:
    U_no, Q_no, condition = ele
    ITEM_no = dataQi[Q_no, 1]
    difficulty = dataQi[Q_no, 2]
    if condition == 1:
        S_cal[U_no, ITEM_no, 0] += dif[difficulty - 1]
    else:
        S_cal[U_no, ITEM_no, 0] -= dif[difficulty - 1]
    S_cal[U_no, ITEM_no, 1] += 1
for ele in S_cal:
    for i in ele:
        i[0] = i[0] / i[1] if i[1] else 0
S = S_cal[:, :, 0]
np.save('data/S', S)

'''
count = 0
for i in S:
    for j in i:
        if j == 0:
            count += 1
print(count)
'''

# calculate similarity
def User_similarity(u1, u2, S):
    count = 0
    sim = 0
    for i in range(MAXITEM):
        if S[u1, i] != 0:
            if S[u2, i] != 0:
                sim += 1 - math.fabs((S[u1, i] - S[u2, i]) / 4)
            count += 1
        elif S[u2, i] != 0:
            count += 1

    return sim / count if count != 0 else 0

UU_similarity = np.zeros([MAXU, MAXU])
for i in range(MAXU):
    for j in range(MAXU):
        if i != j:
            UU_similarity[i][j] = User_similarity(i, j, S)

np.save('data/UU_similarity', UU_similarity)


