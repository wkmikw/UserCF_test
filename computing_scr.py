# coding=utf-8
# __author__ = GaoY
# python computing_scr.py



import numpy as np
import gc
import time
import math

def Hash_Q_item(): # 知识点关系映射表生成函数 单向映射，child to parent
    DIVISION1 = 1000 # 取二级知识点编号
    DIVISION2 = 1000000 # 取一级知识点编号
    NUM_ITEMS = 163
    data = np.loadtxt('data/item_map.csv', dtype=int, delimiter=',') # 读入知识点id与完整编号
    Hash_Q = np.zeros((NUM_ITEMS, 3), dtype=int) # 初始化三级映射表
    temp1st = data[0, 1] // DIVISION1 # 初始化暂存对比编号
    temp2nd = data[0, 1] // DIVISION2
    #temp3rd = 1
    cur1st = 0 # 初始化映射标记
    cur2nd = 0
    cur3rd = 0
    for i in range(NUM_ITEMS):
        code = data[i, 1]
        if code // DIVISION1 == temp1st: # 同一二级知识点
            Hash_Q[i] = [cur1st, cur2nd, cur3rd]
        elif code // DIVISION2 == temp2nd: # 同一一级知识点
            cur1st += 1
            temp1st = code // DIVISION1
            Hash_Q[i] = [cur1st, cur2nd, cur3rd]
        else: # 不同的一级知识点
            cur1st += 1
            cur2nd += 1
            temp1st = code // DIVISION1
            temp2nd = code // DIVISION2
            Hash_Q[i] = [cur1st, cur2nd, cur3rd]
    # np.save('data/Hash_Q', Hash_Q)
    return Hash_Q



def fill_SCR(SCR, PCR, Hash_Q, item_Q_num, NUM_USERS):
    NUM_ITEMS_up = 71
    NUM_ITEMS_upup = 19
    # 利用SCR计算上级知识点正确率
    SCRup = np.zeros((NUM_USERS, NUM_ITEMS_up, 2)) # 初始化上级知识点下答题正确率
    SCRupup = np.zeros((NUM_USERS, NUM_ITEMS_upup, 2))
    for i in range(SCR.shape[0]): # 循环计算上级正确率
        for j in range(SCR.shape[1]):
            if SCR[i, j] != -1:
                SCRup[i, Hash_Q[j, 0], 0] += SCR[i, j] * item_Q_num[j] # 分别存储正确率累加与题目数量
                SCRup[i, Hash_Q[j, 0], 1] += item_Q_num[j]
                SCRupup[i,Hash_Q[j, 1], 0] += SCR[i, j] * item_Q_num[j]
                SCRupup[i,Hash_Q[j, 1], 1] += item_Q_num[j]
    for ele in SCRup:
        for i in ele:
            i[0] = i[0] / i[1] if i[1] != 0 else 0 # 相除得实际正确率
    SCRup = SCRup[:, :, 0] # 舍弃不需要的题目数量数据
    for ele in SCRupup:
        for i in ele:
            i[0] = i[0] / i[1] if i[1] != 0 else 0
    SCRupup = SCRupup[:, :, 0]   
    SCR_all = PCR # 若一级知识点下正确率为0则取个人总正确率
    # 反过来填充SCR的-1项，即未有答题记录项
    for i in range(SCR.shape[0]) :
        for j in range(SCR.shape[1]):
            if SCR[i, j] == -1:
                if SCR[i, Hash_Q[j,0]]:
                    SCR[i, j] = SCRup[i, Hash_Q[j, 0]]
                elif SCR[i, Hash_Q[j, 1]]:
                    SCR[i, j] = SCRupup[i, Hash_Q[j, 1]]
                else:
                    SCR[i, j] = SCR_all[i]
    # np.save('data/SCR', SCR)
    return SCR

if __name__ == '__main__':
    NUM_USERS = 10515
    NUM_ITEMS = 163
    NUM_QUESTION = 42289

    Hash_Q = Hash_Q_item()
    #print(Hash_Q)

    SCR = np.load('data/SCR.npy')
    PCR = np.load('data/PCR.npy')
    Q = np.load('data/Q.npy')
    # 知识点下的题目数
    item_Q_num = np.sum(Q, axis=0)

    SCR = fill_SCR(SCR, PCR, Hash_Q, item_Q_num)





