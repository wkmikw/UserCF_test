#coding=utf-8
#__author__ = GaoY
#python filter.py

import numpy as np
import gc
import time
import math
import random

MAXMOVIE = 1682
MAXUSER = 943

def SplitData(M, k, seed):
    data = np.loadtxt('data/dataUq.csv', dtype=int, delimiter=',')
    test = []
    train = []
    random.seed(seed)
    for ele in data:
        if random.randint(0, M) == k:
            test.append(ele)
        else:
            train.append(ele)
    test = np.array(test)
    train = np.array(train)
    return test, train
if __name__ == '__main__':
    test, train = SplitData(9, 5, 1)
    test = np.array(test)
    train = np.array(train)
    np.save('data/test', test)
    np.save('data/train', train)






