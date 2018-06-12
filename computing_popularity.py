#coding=utf-8
#__author__ = GaoY
#python computing_popularity.py

import numpy as np
import time

MAXMOVIE = 1682
MAXUSER = 943

def computing_popularity():
    train = np.load('data/train.npy')
    popularity = np.zeros(MAXMOVIE + 1, dtype=int)
    for i in train:
        popularity[i[1]] += 1
    np.save('data/popularity', popularity)
    #print(popularity[::20])

if __name__ == '__main__':
    computing_popularity()

