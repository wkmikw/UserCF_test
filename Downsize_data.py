# coding=utf-8
# __author__ = GaoY
# python Downsize_data.py

import numpy as np

NUM_USERS = 10515
NUM_ITEMS = 163
NUM_QUESTION = 42289  # 有空编号
NUM_UQC = 538675

# 选出K个最大的带编号返回
def MAX_K(ele, K):
    Max_list = np.zeros([K, 2], dtype=int)  # min in 0
    for index, val in enumerate(ele):
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


dataUq = np.loadtxt('data/uqc.csv', dtype=int, delimiter=',')
dataQi = np.loadtxt('data/qi.csv', dtype=int, delimiter=',')

Q = np.zeros([NUM_QUESTION, NUM_ITEMS], dtype=int)
for ele in dataQi:
    Q[ele[0]-1, ele[1]-1] = 1
item_Q_num = np.sum(Q, axis=0)  # 0-162
RD = np.zeros([NUM_USERS, NUM_QUESTION], dtype=int)
RC = np.zeros([NUM_USERS, NUM_QUESTION], dtype=int)
for ele in dataUq:
    RD[ele[0] - 1, ele[1] - 1] = 1
    RC[ele[0] - 1, ele[1] - 1] = ele[2]
# print(item_Q_num)

# 精简知识点,并删掉Q矩中题目
Downsizing_item = MAX_K(item_Q_num, 10)
label_item = np.zeros(NUM_ITEMS, dtype=int)
for ele in Downsizing_item:
    label_item[ele[0]] = 1  # 0-162

for i in range(NUM_ITEMS):
    if label_item[i] == 0:
        Q[:, i] = np.zeros(NUM_QUESTION, dtype=int)
label_Q = np.sum(Q, axis=1)
# Q 净化
Q_new = []
for i in range(NUM_ITEMS):
    if label_item[i]:
        Q_new.append(Q[:, i])
Q = np.array(Q_new, dtype=int).T
'''
# 从QI标记label_Q
label_Q = np.ones(NUM_QUESTION, dtype=int) 
for i in range(dataQi.shape[0]):
    if label_item[dataQi[i, 1] - 1] == 0:  # 1-163 to 0-162
        label_Q[dataQi[i, 0] - 1] = 0
        # dataQi = np.delete(dataQi, i, axis=0)  # 可考虑标记重组加快速度
# np.save('data/dataQi', dataQi)
'''

# 从RD中删掉已删掉题目
for i in range(NUM_QUESTION):
    if label_Q[i] == 0:
        RD[:, i] = np.zeros(NUM_USERS, dtype=int)
        RC[:, i] = np.zeros(NUM_USERS, dtype=int)


'''
label_uq = np.ones(dataUq.shape[0], dtype=int)
for i in range(dataUq.shape[0]):
    if label_Q[dataUq[i, 1] - 1] == 0:
        label_uq[i] = 0
dataUq_New = []
for i in range(dataUq.shape[0]):
    if label_uq[i]:
        dataUq_New.append(dataUq[i])
dataUq = np.array(dataUq_New, dtype=int)
'''

# 50个User
# 标记答题最多50个用户
U_Q_num = np.sum(RD, axis=1)  # 个人答题数
Downsizing_User = MAX_K(U_Q_num, 50)  # 答题最多的50个
label_User = np.zeros(NUM_USERS, dtype=int)
for ele in Downsizing_User:
    label_User[ele[0]] = 1  # 0start

# RD删除未标记User,刷新RD
for i in range(NUM_USERS):
    if label_User[i] == 0:
        RD[i] = np.zeros(RD.shape[1], dtype=int)
        RC[i] = np.zeros(RC.shape[1], dtype=int)
RD_New = []
RC_New = []
for i in range(RD.shape[0]):  # 选出有记录的User
    if label_User[i]:
        RD_New.append(RD[i])
        RC_New.append(RC[i])
RD = np.array(RD_New, dtype=int)  # 50 X max
RC = np.array(RC_New, dtype=int)
U_Q_num = np.sum(RD, axis=1)  # 个人答题数
Q_U_num = np.sum(RD, axis=0)  # 题目作答数
RD_New = []
RC_New = []
Hash_Q = np.tile(-1, RD.shape[1] + 1)
cur = 0
for i in range(RD.shape[1]):
    if Q_U_num[i]:
        RD_New.append(RD[:, i])
        RC_New.append(RC[:, i])
        Hash_Q[i + 1] = cur
        cur += 1
#np.save('data/Hash_Q', Hash_Q)
RD = np.array(RD_New, dtype=int).T
RC = np.array(RC_New, dtype=int).T
# 用Hash_Q刷新Q
Q_new = []
for i in range(NUM_QUESTION):
    if label_Q[i] and Q_U_num[i]:
        Q_new.append(Q[i])
Q = np.array(Q_new, dtype=int)


'''
RD_New = []
for i in range(RD.shape[0]):
    if label_User[i]:
        RD_New.append(RD[i])
RD = np.array(RD_New, dtype=int)  # 50 X max
print(RD.shape)
# 删掉User后再次标记Q
label_Q = np.zeros(RD.shape[1], dtype=int)
Q_U_num = np.sum(RD, axis=0)  # 删掉部分User后每题目答过的人数
RD_New = []
for i in range(RD.shape[1]):  # 选出有记录的题
    if Q_U_num[i]:
        RD_New.append(RD[:, i])
        label_Q[i] = 1  # 0-max

RD = np.array(RD_New, dtype=int)
RD = RD.T
print(RD.shape)



# delete dataQi
dataQi_New = []
for i in range(dataQi.shape[0]):
    if label_Q[dataQi[i, 0] - 1]:
        dataQi_New.append(dataQi[i])
dataQi = np.array(dataQi_New, dtype=int)

# delete dataUq again
label_uq = np.ones(dataUq.shape[0], dtype=int)  # 标签初值为1
for i in range(dataUq.shape[0]):
    if label_Q[dataUq[i, 1] - 1] == 0 or label_User[dataUq[i, 0] - 1] == 0:
        label_uq[i] = 0
dataUq_New = []
for i in range(dataUq.shape[0]):
    if label_uq[i]:
        dataUq_New.append(dataUq[i])
dataUq = np.array(dataUq_New, dtype=int)


# hash映射使数据序号连续
# 映射数组下标为原值(U_id)，填充为真值
hash_Q = np.tile(-1, NUM_QUESTION + 1)
hash_U = np.tile(-1, NUM_USERS + 1)
hash_item = np.tile(-1, NUM_ITEMS + 1)
# 映射U_id
for i in range(Downsizing_User.shape[0]):
    hash_U[Downsizing_User[i, 0] + 1] = i  # downsize 是0-（10515-1）
# 映射ITEM_id
for i in range(Downsizing_item.shape[0]):
    hash_item[Downsizing_item[i, 0] + 1] = i  # 0-9
# 映射Q_id
temp = 0
for i in range(dataQi.shape[0]):
    hash_Q[dataQi[i, 0]] = i

print("mapping completed")
# 刷新dataUq和dataQi
for ele in dataUq:
    ele[0] = hash_U[ele[0]]  # 0-49
    ele[1] = hash_Q[ele[1]]
for ele in dataQi:
    ele[0] = hash_Q[ele[0]]
'''
np.save('data/Q', Q)
np.save('data/RD', RD)
np.save('data/RC', RC)
with open('/python/CDM/data/dataUq.csv', 'w') as f:
    for i in range(RD.shape[0]):
        for j in range(RD.shape[1]):
            if RD[i, j]:
                f.write('%d,%d,%d\n' % (i, j, RC[i, j]))

with open('/python/CDM/data/dataQi.csv', 'w') as f:
    for i in range(Q.shape[0]):
        for j in range(Q.shape[1]):
            if Q[i, j]:
                f.write('%d,%d\n' % (i, j))
                break
