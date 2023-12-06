from time import time, sleep, strftime, gmtime

def calculate_time(func):
    """
    Calculates Function Execution Run time in Minutes.
    """
    def wrapper(*args, **kwargs): 
        start = time() 
        result = func(*args, **kwargs) 
        sleep(1)
        end = time()
        elapsed_time = end - start 
        print('Execution time for Function '+func.__name__+' is ' + strftime("%H:%M:%S", gmtime(elapsed_time)))
        return result 
    return wrapper 