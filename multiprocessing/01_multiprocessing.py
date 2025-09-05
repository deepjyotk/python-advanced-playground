

"""
The GIL is a global lock that prevents multiple threads from executing Python code simultaneously.
This is a problem for CPU-bound tasks, because the GIL prevents multiple threads from
executing the same code in parallel.

The solution is to use multiple processes instead of multiple threads.

Are python threads bind to platform threads? Yes, they are. But, the GIL is a global lock that prevents
multiple threads from executing Python code simultaneously.


So, alll in all python is a single thread language, but we can use multiprocessing to run multiple processes in parallel.
"""
import os
from multiprocessing import Process
import time

print(f"Module level - __name__: {__name__}, PID: {os.getpid()}")

def cpu_bound():
    print(f"Child process - __name__: {__name__}, PID: {os.getpid()}")
    total = 0
    for i in range(10**7):
        total += i

if __name__ == '__main__':
    print(f"Main process - __name__: {__name__}, PID: {os.getpid()}")
    start = time.time()
    processes = []
    for i in range(4):
        p = Process(target=cpu_bound)
        processes.append(p)
        # i am starting the process
        p.start()

    
    # Wait for all processes to finish
    for p in processes:
        p.join()
    
    end = time.time()
    print(f"Multiprocessing time: {end - start}")
