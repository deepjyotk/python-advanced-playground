"""
Multithreading vs Multiprocessing demonstration.

This shows how the Global Interpreter Lock (GIL) prevents true parallel execution
of CPU-bound tasks in Python threads.

The GIL allows only one thread to execute Python code at a time, so CPU-bound
tasks don't benefit from threading - they actually run sequentially.
"""

import threading
import time
import os

def cpu_bound():
    """CPU-bound task that performs intensive computation."""
    total = 0
    for i in range(10**7):
        total += i
    return total

def run_single_threaded():
    """Run the CPU-bound task in a single thread."""
    print("Running single-threaded...")
    start = time.time()
    
    for _ in range(4):
        cpu_bound()
    
    end = time.time()
    print(f"Single-threaded time: {end - start:.4f} seconds")
    return end - start

def run_multithreaded():
    """Run the CPU-bound task using multiple threads."""
    print("Running multithreaded...")
    start = time.time()
    
    threads = []
    for _ in range(4):
        t = threading.Thread(target=cpu_bound)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.time()
    print(f"Multithreaded time: {end - start:.4f} seconds")
    return end - start

if __name__ == '__main__':
    print(f"Number of CPU cores: {os.cpu_count()}")
    print("=" * 50)
    
    # Run single-threaded first
    single_time = run_single_threaded()
    
    print("-" * 30)
    
    # Run multithreaded
    multi_time = run_multithreaded()
    
    print("=" * 50)
    print(f"Speedup: {single_time / multi_time:.2f}x")
    print(f"Expected speedup with true parallelism: ~{os.cpu_count()}x")
    print("\nNote: Due to the GIL, multithreading doesn't provide true parallelism")
    print("for CPU-bound tasks. The tasks run sequentially, not in parallel.")
