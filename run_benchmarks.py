import subprocess
import time
import os
import resource

def run_proc(cmd):
    # Get resource usage before
    before_ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    
    # Run subprocess
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    
    t1 = time.time()
    after_ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    
    # Peak RSS difference (or total child peak RSS in kilobytes)
    # In Linux, maxrss is returned in kilobytes
    max_rss_kb = after_ru.ru_maxrss
    
    return t1 - t0, max_rss_kb, stdout.decode().strip()

print("--- ORONDSIINAYA BENCHMARKS ---")
python_time, python_mem, python_out = run_proc("python3 test_fib.py")
print(f"Python: Time = {python_time:.4f}s, Peak RAM = {python_mem / 1024:.2f} MB, Out = {python_out}")

tusmo_time, tusmo_mem, tusmo_out = run_proc("./test_fib")
print(f"Tusmo:  Time = {tusmo_time:.4f}s, Peak RAM = {tusmo_mem / 1024:.2f} MB, Out = {tusmo_out}")
