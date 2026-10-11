import subprocess
import time
import os

def run_isolated(cmd):
    code = f"""
import subprocess
import resource
import time
t0 = time.time()
p = subprocess.Popen({repr(cmd)}, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
t1 = time.time()
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
# On Linux, maxrss is in Kilobytes.
print(f"{{t1-t0:.4f}}|{{ru.ru_maxrss}}")
"""
    p = subprocess.Popen(["python3", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    parts = stdout.decode().strip().split('|')
    return float(parts[0]), int(parts[1])

print("Tirinta Fibonacci(38) socota...")
py_time, py_mem = run_isolated("python3 test_fib.py")
print(f"Python: Time = {py_time:.4f}s, Peak RSS = {py_mem} KB ({py_mem/1024:.2f} MB)")

tusmo_time, tusmo_mem = run_isolated("./test_fib")
print(f"Tusmo:  Time = {tusmo_time:.4f}s, Peak RSS = {tusmo_mem} KB ({tusmo_mem/1024:.2f} MB)")
