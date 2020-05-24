
import datetime
import time
import multiprocessing #from multiprocessing import Process
import os
import random

# predict
# forecasting
# valve probability distribution


def controller(q):
    tp = 0
    time.sleep(3)
    tp = random.randint(0,4)
    q.put(tp)
    #print('parent process:', os.getppid())
    print('Control finished - process id:', os.getpid())

it = 0
tau = 5
q = multiprocessing.Queue()
p = multiprocessing.Process(target=controller, args=(q,))
print("calling controller for next it = 0 ")
p.start()
pattern = q.get()
print("Getting the pattern precalculated for it=", it," and using in this status tp: ",pattern)
p = multiprocessing.Process(target=controller, args=(q,))
p.start()
while True:
    #print(datetime.datetime.now())
    if(it%tau == 0 and it != 0):
        pattern = q.get()
        print("Getting the pattern precalculated for it=", it," and using in this status tp: ",pattern)   
        p.join()
        p = multiprocessing.Process(target=controller, args=(q,))
        print("calling controller for next it =", it+tau)
        p.start()
    print("Pattern t = ", it, " is: ", pattern) # tau = 5 min
    time.sleep(1)
    print(it)
    it = it + 1


