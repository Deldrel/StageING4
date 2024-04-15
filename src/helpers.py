def time_it(func: callable) -> callable:
    from time import perf_counter

    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"Execution time of {func.__name__}: {end - start:.6f} seconds")
        return result

    return wrapper
