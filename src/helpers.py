def timeit(func: callable) -> callable:
    from time import perf_counter

    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"Execution time of {func.__name__}: {end - start:.6f} seconds")
        return result

    return wrapper


def try_except(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An exception occurred in {func.__name__}: {e}")

    return wrapper
