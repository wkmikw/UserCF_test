# coding=utf-8
# __author__ = GaoY
# python attach_difficulty.py

import numpy as np


def attach_difficulty(MAXQ):
    # MAXQ = 34301

    difficulty = np.loadtxt('data/difficulty.csv', dtype=int, delimiter='\t')
    Hash_Q = np.load('data/Hash_Q.npy')
    difficulty_attached = np.zeros(MAXQ, dtype=int)
    for ele in difficulty:
        if Hash_Q[ele[0]] != -1:
            difficulty_attached[Hash_Q[ele[0]]] = ele[1]
    # np.save('data/difficulty_attached', difficulty_attached)

    dataQi = np.loadtxt('data/dataQi1.csv', dtype=int, delimiter=',')
    dataQi_new = []
    for ele in dataQi:
        dataQi_new.append([ele[0], ele[1], difficulty_attached[ele[0]]])
    dataQi = np.array(dataQi_new, dtype=int)
    return dataQi


if __name__ == '__main__':
    dataQi = attach_difficulty()
    a=1

