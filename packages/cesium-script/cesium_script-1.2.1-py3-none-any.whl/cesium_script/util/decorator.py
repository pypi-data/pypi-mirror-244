import logging
from time import time


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        if (t2 - t1) > 0.01:
            logging.debug(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func
