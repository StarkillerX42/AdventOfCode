#!/usr/bin/env python3

import numpy as np
from pathlib import Path


here = Path(__file__).absolute().parent
data_file = here / 'dat/day_2.txt'

verbose = False
count = 0
with data_file.open('r') as f:
    for line in f:
        rnge, char, pwd = line.split()
        rnge = np.array(rnge.split('-'), dtype=int)
        char = char[0]
        num_chars = pwd.count(char)
        if (num_chars <= rnge[1]) and (num_chars >= rnge[0]):
            if verbose:
                print(f'Range: {rnge}, Char: {char}, Password: {pwd}')
            count += 1

print(f'Valid passwords in first method: {count:.0f}')


count = 0
with data_file.open('r') as f:
    for line in f:
        keys, char, pwd = line.split()
        keys = np.array(keys.split('-'), dtype=int)
        char = char[0]
        if verbose:
            print(f'Keys: {keys}, Char: {char}, Password: {pwd}')
        if any(len(pwd) < (keys - 1)):
            print('continuing')
            continue
        matches = np.sum((pwd[keys[0] - 1] == char, pwd[keys[1] - 1] == char))
        if matches == 1:
            count += 1

print(f'Valid passwords in second method: {count:.0f}')
