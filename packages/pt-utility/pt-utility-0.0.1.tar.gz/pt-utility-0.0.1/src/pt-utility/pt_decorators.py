from time import time

def calculate_time(func):
    """
    Calculates Function Execution Run time in Minutes.
    """
    def wrapper(*args, **kwargs): 
        start = time() 
        result = func(*args, **kwargs) 
        end = time() 
        print('Function '+func.__name__+' executed in ' + str((end-start)/60)[:6] +'m')
        return result 
    return wrapper 