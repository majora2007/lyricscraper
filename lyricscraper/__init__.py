from .song import Song


import time
from functools import wraps

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.perf_counter() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait > 0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.perf_counter()
            return ret
        return rateLimitedFunction
    return decorate

def SilentlyFail(default_value=None):
    """ Will silently ignore any errors when executing this function. Will return None by default, can optionally pass return value to default to """

    def silently_fail_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if default_value is not None:
                    return default_value

        return func_wrapper

    return silently_fail_decorator

__version__ = '2020.08.01'