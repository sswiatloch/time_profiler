import time_profiler as tp
from time import sleep

@tp.TimeExecution
def foo(x):
    print(x)
    sleep(2)
    return x+1

print(foo(0))