# coding:utf-8
# __author__ = GaoY
# python fill_S_with_rules.py

import numpy as np
import math, time
from computing_scr import Hash_Q_item, fill_SCR

MAXQ = 30119
MAXU = 500
MAXITEM = 163

RC = np.zeros([MAXU, MAXQ])
RD = np.zeros([MAXU, MAXQ])

dataQi = np.loadtxt('data/dataQi1.csv', dtype=int, delimiter=',')
dataUq = np.loadtxt('data/dataUq1.csv', dtype=int, delimiter=',')

for ele in dataUq:
    RC[ele[0], ele[1]] = ele[2]
    RD[ele[0], ele[1]] = 1
# RCS1 每一题做对总数
RCS1 = np.sum(RC, axis=0)
# RDS1 每一题做过总数
RDS1 = RD.sum(axis=0)
# D21是被除数组，以下处理防止除0
RDS1[RDS1 < 1] = 1
# D3 某题目难度系数=每一题做对总数/每一题做过总数
QDD = RCS1/RDS1
# RCS2 每人做对的题目之和，对列求和（压缩列）
RCS2 = RC.sum(axis=1)
# D22  每人做过的题目之和
RDS2 = RD.sum(axis=1)
RDS2[RDS2 < 1] = 1
# D4  个人做题正确率
PCR = RCS2/RDS2
# Q矩阵：试题考查知识点矩阵
Q = np.zeros([MAXQ, MAXITEM])
for ele in dataQi:
    Q[int(ele[0])-1, int(ele[1])-1] = 1
# SR1 各个知识点下的作对题情况
SR1 = np.dot(RC, Q)
# SD1 学生各个知识点下做过的题目数量
SD1 = np.dot(RD, Q)
SD1[SD1 <= 0] = -1  # 未做过标识为-1
# SCR 学生各个知识点下做题的正确率
SCR = SR1/SD1
SCR[SD1 < 0] = -1  # 未做过标识为-1


# 映射知识点关系
Hash_Q = Hash_Q_item()
# 知识点下的题目数
item_Q_num = np.sum(Q, axis=0)
# 计算填充未有答题记录项
SCR = fill_SCR(SCR, PCR, Hash_Q, item_Q_num)


# RS1 用户每题对应的知识点下做对的题目数量
QT = Q.T
RS1 = np.dot(SR1, QT)
# RD1 用户每题对应的知识点下做对的题目数量
RD1 = np.dot(SD1, QT)
RD1[RD1 <= 0] = 1


# 学生每一题的正确率
RS2 = RS1/RD1

# 利用该题的难度系数以及学生个人做题正确率，学生对该知识点下题目的正确率
# R矩阵：学生做题正确情况
R = np.zeros([MAXU, MAXQ])

QDD_U = np.tile(QDD, (MAXU, 1))

PCR_Q = np.zeros((MAXU, MAXQ), dtype=float)  # 初始化个人题目正确率填充矩阵
for i in range(PCR_Q.shape[0]):
    for j in range(PCR_Q.shape[1]):
        item = dataQi[j, 1]
        PCR_Q[i, j] = SCR[i, item]  # 填充为各级知识点正确率

RS2[RS2 == 0] = PCR_Q[RS2 == 0]  # 填充未答过的题目

R = QDD_U*0.25 + RS2*0.75
R[RC > R] = RC[RC > R]
# 学生能力
S1 = np.dot(R, Q)
# 知识点下的题目
Q1 = np.sum(Q, axis=0)
Q1[Q1 <= 0] = 1
# 平均能力
S = S1/Q1
S[SCR > S] = SCR[SCR > S]
np.save('data/S_fill_rule', S)
