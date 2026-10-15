# pool na windowsie nie widzi funkcji z komorki, dlatego jest w pliku
import os
from multiprocessing import Pool

import pandas as pd
from filesplit.split import Split


def split_file(filepath, chunksize, destination):
    os.makedirs(destination, exist_ok=True)
    for name in os.listdir(destination):
        if name.endswith('.csv'):
            os.remove(destination + '/' + name)
    split = Split(filepath, destination)
    split.bylinecount(linecount=chunksize, includeheader=True)


def load_files(directory, processes):
    files = []
    for f in os.listdir(directory):
        if f.endswith('.csv'):
            files.append(directory + '/' + f)

    with Pool(processes=processes) as pool:
        results = pool.map(pd.read_csv, files)
        results = pd.concat(results, ignore_index=True)

    return results


def suma_likes(path):
    df = pd.read_csv(path)
    return df['likes'].sum()


def suma_likes_mp(pliki, processes):
    with Pool(processes=processes) as pool:
        return pool.map(suma_likes, pliki)
