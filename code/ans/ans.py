import datetime
import time
import multiprocessing #from multiprocessing import Process
import os
import random
# predict
# forecasting
# valve probability distribution
def controller(q):
    time.sleep(3)
    q.put(random.randint(0,4))
    print('Control finished - process id:', os.getpid())

it = 0
q = multiprocessing.Queue()
p = multiprocessing.Process(target=controller, args=(q,))
print("calling controller for next it = 0 ")
p.start()
pattern = q.get()
print("Getting the pattern precalculated for it=", it," and using in this status tp: ",pattern)
p.join()

p = multiprocessing.Process(target=controller, args=(q,))
print("calling controller for next it = 1 ")
p.start()

while True:
    #print(datetime.datetime.now())
    if(it%5 == 0 and it != 0):
        pattern = q.get()
        print("Getting the pattern precalculated for it=", it," and using in this status tp: ",pattern)
        p.join()
        p = multiprocessing.Process(target=controller, args=(q,))
        print("calling controller for next it =", it+5)
        p.start()
    print("Pattern t = ", it, " is: ", pattern) # tau = 5 min
    time.sleep(1)
    print(it)
    it = it + 1
