# coding:utf-8
# __author__ = GaoY
# python User_similarity.py

import numpy as np
import math
from filter import SplitData
from attach_difficulty import attach_difficulty

MAXQ = 3911
MAXU = 50
MAXITEM = 10
K = 5
M = 10  # 数据分片

# 选出K个最大的
def MAX_K(ele, K):
    Max_list = np.zeros([K, 2]) # min in 0
    for index, val in enumerate(ele): #  index:U_id, val:相似程度
        if val > Max_list[0][1]:
            Max_list[0] = [index, val]
            j = 1
            # 重新有序化
            while j < K:
                if val > Max_list[j][1]:
                    Max_list[j-1] = Max_list[j]
                    Max_list[j] = index, val
                    j += 1
                else:
                    break
    return(Max_list)


# calculate similarity
def User_similarity(u1, u2, S):
    count = 0
    sim = 0
    for i in range(MAXITEM):
        if S[u1, i] != 0:
            if S[u2, i] != 0:
                sim += 1 - math.fabs((S[u1, i] - S[u2, i]) / 3)
            count += 1
        elif S[u2, i] != 0:
            count += 1

    return sim / count if count != 0 else 0


def predict(Q_dif, s):
    dif = [0.5, 0.625, 0.75, 0.875, 1.]
    pre = s / dif[Q_dif - 1]
    return pre + (1 - pre) * 0.25 if pre <= 1 else pre


all_d = 0
all_d_raw = 0
for tag in range(M):
    test, train = SplitData(M - 1, tag, 5)
    test = np.array(test, dtype=int)
    train = np.array(train, dtype=int)
    dataQi = attach_difficulty()  # [题号， 知识点， 难度]
    S_cal = np.zeros([MAXU, MAXITEM, 2], dtype=float)  # [难度加权，count]
    dif = [1., 1.25, 1.5, 1.75, 2.]

    # 计算难度加权能力值
    for ele in train:
        U_no, Q_no, condition = ele
        ITEM_no = dataQi[Q_no, 1]
        difficulty = dataQi[Q_no, 2]
        # 作对按难度加权，做错减加权倒数
        if condition == 1:
            S_cal[U_no, ITEM_no, 0] += dif[difficulty - 1]
        else:
            S_cal[U_no, ITEM_no, 0] -= 1/dif[difficulty - 1]
        S_cal[U_no, ITEM_no, 1] += 1
    for ele in S_cal:
        for i in ele:
            i[0] = i[0] / i[1] if i[1] else 0
    S = S_cal[:, :, 0]
    S_raw = S
    np.save('data/S', S)

    UU_similarity = np.zeros([MAXU, MAXU])
    for i in range(MAXU):
        for j in range(MAXU):
            if i != j:
                UU_similarity[i][j] = User_similarity(i, j, S)

    np.save('data/UU_similarity', UU_similarity)
    '''
    count = 0
    for i in range(MAXU):
        for j in range(MAXITEM):
            if S[i, j] == 0:
                count += 1
    print(count)
    '''
    # fill the S
    for i in range(MAXU):
        max5 = MAX_K(UU_similarity[i], K)
        temp = np.zeros(MAXITEM, dtype=float)
        for ele in max5:
            temp += ele[1] * S[int(ele[0])]
        for j in range(MAXITEM):
            if S[i, j] == 0:
                S[i, j] = temp[j] / 5

    # 归一化 负值归零
    S[S < 0] = 0
    S = S / np.max(S)

    d = 0
    d_raw = 0
    for ele in test:
        Q_dif = dataQi[ele[1], 2]
        item = dataQi[ele[1], 1]
        s = S[ele[0], item]
        p = predict(Q_dif, s)
        s = S_raw[ele[0], item]
        p_raw = predict(Q_dif, s)
        d += (p - ele[2]) ** 2
        d_raw += (p_raw - ele[2]) ** 2

    d = d / test.shape[0]
    d_raw = d_raw / test.shape[0]
    print(d, d_raw)
    all_d += d
    all_d_raw += d_raw

print(all_d / 10, all_d_raw / 10)