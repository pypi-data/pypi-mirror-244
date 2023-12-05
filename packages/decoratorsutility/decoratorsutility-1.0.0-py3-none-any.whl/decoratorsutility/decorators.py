import logging
from time import (
    sleep,
    time,
    gmtime,
    strftime
)
from typing import (
    Union,
    List,
    Callable
)
from decoratorsutility.utils.errors import TimeoutException
from pathutility import PathUtils
import threading
from decoratorsutility.utils.logs import log_error
pu=PathUtils()


def exception_dec(exc_mod, exc_path):
    r"""
    Decorator that handles exceptions by logging errors to a specified file path.

    Args:
    - exc_mod (str): The module being executed.
    - exc_path (str): The path where the output file will be stored.

    :Usage:

    .. code-block:: python

        @exception_dec('module_name', '/path/to/logfile.log')
        def function_name(*args, **kwargs):
            try:
                # Function execution
                return func(*args, **kwargs)
            except Exception as err:
                # Logs the error to the specified file path
                log_error(module=exc_mod, file_path=exc_path, error=err)
                logging.error(err)
    """

    def def_task(func):
        """Defines the function with appropriate error handling."""

        def exec_task(*args, **kwargs):
            """Executes the function with the supplied parameters."""
            try:
                return func(*args, **kwargs)
            except Exception as err:
                log_error(module=exc_mod, file_path=exc_path, error=err)
                logging.error(err)
        return exec_task

    return def_task


def repeat_on_error(
        max_try: int = 3,
        error_log: str = None,
        show_error: bool = True
):
    """
    Decorator that retries function execution a set number of times in case of exceptions.

    :param max_try: Maximum number of retries.
    :param error_log: File path to log errors (txt or csv format).
    :param show_error: Flag to display errors (default is True).

    :return: Decorated function.

    :Usage:

    .. code-block:: python

        @repeat_on_error(max_try=3, error_log='log/logfile.log', show_error=True)
        def test_dummy(arg1:int):
        return arg1/0
        
        if __name__ == '__main__':
            test_dummy(1)

    """
    def checking(function):
        def checked(*args, **kwargs):
            for _ in range(max_try):
                try:
                    return function(*args, **kwargs)
                except Exception as problem:
                    print("An unexpected error occurred")

                    if show_error:
                        logging.error(problem)

                    if kwargs.get('error_filepath') or error_log is not None:
                        fp = kwargs.get('error_filepath') or error_log
                        log_error(module=__name__, file_path=fp, error=problem)
                        print('The error has been saved in the error log')
                    if _ == max_try - 1:
                        raise problem  # Raising the exception after max_try attempts
        return checked
    return checking

class _Timer:
    """
    class to estimate the time it takes to run a function 
    and number of executions
    
    :Usage:

    .. code-block:: python

        from decoratorsutility import timer_decorator
        
        
        @timer_decorator
        def dummy(x):
            return x+1
            
        for i in range(10):
            x=dummy(i)
        
        #get the information of the function
        timer_decorator.data
        {'dummy': {'executions': 10, 'total_time': 0.0}}
    
    """    
    def __init__(self):
        self.data={}

    #decorator of a function to extract the time it takes to run it
    def __call__(self,func):
        def wrapper(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            end = time()
            elapsed_time = round(end - start, 3)
            
            # update the global dictionary with function information
            if func.__name__ not in self.data:
                self.data[func.__name__] = {'executions': 1, 'total_time': elapsed_time}
            else:
                self.data[func.__name__]['executions'] += 1
                self.data[func.__name__]['total_time'] += elapsed_time
            
            return result
        return wrapper

    def __str__(self) -> str:
        return str(self.data)
    
    def __repr__(self) -> str:
        return self.__str__()

timer_decorator=_Timer()
    

def timeout_decorator(timeout):
    """decorrator to set a timeout to a function
    
    :param timeout: time in seconts
    :type timeout: int
    
    :Usage:

    .. code-block:: python

        import time
        from svh_utils.decorators import timeout_decorator
        
        @timeout_decorator(timeout=5)
        def my_function():
            time.sleep(6)  # Simulate a long-running function
            return "Success!"
            
        if __name__ == '__main__':
            a=my_function()
    """    
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            error = [None]
            event = threading.Event()

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    error[0] = e
                finally:
                    event.set()

            thread = threading.Thread(target=target)
            thread.start()

            if not event.wait(timeout):
                # Timeout exceeded
                raise TimeoutException(f"Timeout exceeded: {timeout} seconds.")

            if error[0] is not None:
                raise error[0]

            return result[0]
        return wrapper
    return decorator