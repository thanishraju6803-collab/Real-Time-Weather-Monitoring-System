import functools
import logging
import time
from pathlib import Path

def setup_logging():
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(log_dir / "app.log", encoding="utf-8"), logging.StreamHandler()]
    )

def timed(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            logging.getLogger(function.__module__).info(
                "%s finished in %.6f seconds", function.__name__, time.perf_counter() - start)
    return wrapper

def make_temperature_filter(threshold):
    # Closure: this returned function remembers threshold.
    def is_above(record):
        return float(record["temperature"]) >= threshold
    return is_above

def apply_operation(values, operation):
    # Higher-order function: receives another function as an argument.
    return [operation(value) for value in values]
