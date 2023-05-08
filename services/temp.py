import math
import time
from functools import wraps

func_time = {}

def get_func_time(count=1):
    def wrapper_ext(func):
        global func_time
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal count
            start = time.time()
            res = func(*args, **kwargs)
            duration = time.time() - start
            func_time[func.__name__] = [count, duration]
            count += 1
            return res
        return wrapper
    return wrapper_ext


@get_func_time()
def func1(a,b):
    if a > b:
        temp = b
    else:
        temp = a
    for i in range(1, temp + 1):
        if ((a % i == 0) and (b % i == 0)):
            gcd = i
    return gcd

@get_func_time(count=11)
def func2(a,b):
    return math.log(a,b)


func1(1976456, 546782)
func1(1973456, 541782)

func2(9566776,327)
func2(9568966,32)
print(func_time)
