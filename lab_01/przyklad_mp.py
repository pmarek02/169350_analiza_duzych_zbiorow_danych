from itertools import repeat
from functools import partial
import pandas as pd
from datetime import datetime
from filesplit.split import Split
from multiprocessing import Pool
import os


def count_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(f"Czas wykonania {func.__name__}: {datetime.now() - start} sekund")
        return result
    return wrapper


def apply_args_and_kwargs(func, args, kwargs):
    return func(*args, **kwargs)


def starmap_with_kwargs(pool, func, args_iter, kwargs_iter):
    args_for_starmap = zip(repeat(func), args_iter, kwargs_iter)
    return pool.starmap(apply_args_and_kwargs, args_for_starmap)


def split_file(filepath, chunksize, destination):
    os.makedirs(destination, exist_ok=True)
    split = Split(filepath, destination)
    split.bylinecount(linecount=chunksize, includeheader=True)


@count_time
def load_files(directory):
    files = [[f"{directory}/{f}"] for f in os.listdir(directory) if f.endswith(".csv")]

    with Pool(processes=min(5, os.cpu_count() or 1)) as pool:
        read_csv_custom = partial(pd.read_csv, on_bad_lines="skip")
        results = pool.map(read_csv_custom, [f[0] for f in files])
        results = pd.concat(results, ignore_index=True)

    return results


if __name__ == '__main__':
    split_file('zamowienia_expanded.csv', 2_000_000, 'data')
    df4 = load_files('data')
    df4.info()
