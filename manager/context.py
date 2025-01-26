import time
from contextlib import contextmanager


@contextmanager
def time_it(label: str = "Execution"):
    """
    Context manager to measure the execution time of a block of code.
    """

    start_time = time.time()
    try:
        yield
    finally:
        elapsed_time = time.time() - start_time
        print(f"[{label}]: Time Taken: {elapsed_time:.4f} seconds")
