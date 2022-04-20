from concurrent.futures import ThreadPoolExecutor
import functools


def run_process(func,args,lst):
    partial = functools.partial(func,args)
    with ThreadPoolExecutor(8) as executor:
        results = executor.map(partial, lst)
        return results