import time

from prefect import flow, task, Flow
# from prefect_dask import DaskTaskRunner
from prefect.task_runners import ConcurrentTaskRunner
from time import sleep
import sys


# measure of time of execution
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return result
    return wrapper

@task
def count_and_sleep(x):
    for i in range(x):
        print(i)
        sleep(1)
    return 'slepping seconds of: ' + str(x)

@flow
def very_simple_flow():
    print('ok')

@flow
def first_flow(x):
    count_and_sleep(x)


@measure_execution_time
@flow(task_runner=ConcurrentTaskRunner())
def concurrent_flow(n, x):
    futures = []
    for i in range(n):
        future = count_and_sleep.submit(x)
        futures.append(future)
    return futures
res_futures = concurrent_flow(6, 3)
res = [fut.result() for fut in res_futures]
print(res)
sys.exit()