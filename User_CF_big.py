# coding:utf-8
# __author__ = GaoY
# python User_similarity.py

import numpy as np
import math, time
from filter import SplitData
from attach_difficulty import attach_difficulty

MAXQ = 30119
MAXU = 500
MAXITEM = 163
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
    return Max_list


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
    return pre + (1 - pre) * 0.25 if pre <= 1 else 1


def go_test(S, test, dataQi):
    d = 0  # 方差
    e = 0  # 期望正确率
    r = 0  # 实际正确率
    for ele in test:
        Q_dif = dataQi[ele[1], 2]
        item = dataQi[ele[1], 1]
        s = S[ele[0], item]
        p = predict(Q_dif, s)
        d += (p - ele[2]) ** 2
        e += p
        r += ele[2]
    d = d / test.shape[0]
    e = e / test.shape[0]
    r = r / test.shape[0]
    return [d, e, r]

S_rules = np.load('data/S_fill_rule.npy') - 0.4
S_rules[S_rules < 0] = 0
all_d = 0
all_d_raw = 0
start = time.time()
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
    S_raw = S.copy()
    np.save('data/S', S)
    end = time.time()
    print('Task S completed at %ds' % (end - start))

    # 计算相似度
    UU_similarity = np.zeros([MAXU, MAXU])
    for i in range(MAXU):
        for j in range(i + 1, MAXU):
            UU_similarity[i][j] = User_similarity(i, j, S)
            UU_similarity[j][i] = UU_similarity[i][j]

    np.save('data/UU_similarity', UU_similarity)
    end = time.time()
    print('Task Sim completed at %ds' % (end - start))

    # fill the S
    S_fill = np.zeros([MAXU, MAXITEM], dtype=float)
    for i in range(MAXU):
        maxK = MAX_K(UU_similarity[i], K)
        temp = np.zeros(MAXITEM, dtype=float)
        simacc = 0
        for ele in maxK:
            temp += ele[1] * S[int(ele[0])]
            simacc += ele[1]
        for j in range(MAXITEM):
            if S[i, j] == 0:
                S_fill[i, j] = temp[j] / simacc
    S[S == 0] = S_fill[S == 0]

    # 归一化 负值归零
    S[S < 0] = 0
    S = S / np.max(S)
    #S = S
    S[S < 0] = 0
    S_raw = S_raw / np.max(S_raw)
    S_raw = S_raw + 0.07
    # test
    d, e, r = go_test(S, test, dataQi)
    print(d, e, r, 'CF')
    d, e, r = go_test(S_rules, test, dataQi)
    print(d, e, r, 'rules')
    d, e, r = go_test(S_raw, test, dataQi)
    print(d, e, r, 'raw')

    #S_raw[S_raw == 0] = S_rules[S_raw == 0]
    #d, e, r = go_test(S_raw, test, dataQi)
    #print(d, e, r, 'raw+rule')

# print(all_d / M, all_d_raw / M)




