import sys
import cv2
import numpy as np
import dpkt
from multiprocessing import pool
import requests
import pprint
import numba
import random
from numba import jit, njit, vectorize
import timeit

def TablePrint(content):
    format_str= pprint.pformat(content, width=98)
    pprint.pprint("|"+format_str+"|",)
    pprint.pprint('_'*100)
    pass 


#print(sys.stdout.name)
#TablePrint('test')

@njit
def Monte_Carlo_pi(nsamples):
    acc=0
    for i in range(nsamples):
        x=random.random()
        y=random.random()
        if (x**2+y**2)<1:
            acc+=1
    return 4*acc/nsamples

nsamples=1000000

result=Monte_Carlo_pi(nsamples)
print(result)

@jit(nopython=True)
def cannot_compile(x):
    return x['key']

#print(cannot_compile({'key':"value"}))
b=np.array([10,20,30,40])
c=np.arange(16)
#print(c.reshape((4,4)))

@vectorize(['int64(int64, int64)'], target='cuda')
def add_ufunc(x, y):
    return x+y

print(add_ufunc(4,3223))
#print(timeit.timeit('add_ufunc(4545,2311)', 1000))