import numpy as np
import time
Ntot = 412316890416//100000
arrayA = np.ones(Ntot, dtype='bool')

arrayB = np.random.randint(0,10,Ntot)
q = 5

tic = time.perf_counter()
arrayA = np.logical_and(arrayA, q>arrayB)
toc = time.perf_counter()

print("time of performing np.logical_and for an np array having len = "+str(Ntot)+": "+str(toc-tic)+"s")
