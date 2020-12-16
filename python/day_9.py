#!/usr/bin/env python3
import numpy as np
from pathlib import Path

data_path = Path('dat/day_9.txt')
numbers = np.loadtxt(data_path.as_posix(), dtype=int)

invalid_ind = np.nan
invalid_num = np.nan
for i, val in enumerate(numbers[25:]):
    num_pool = numbers[i:i + 25]
    outer_sum = num_pool.reshape((25, 1)) + num_pool.reshape((1, 25))
    if not np.sum((val == outer_sum)):
        invalid_ind = i
        invalid_num = val

print(f'Part 1: {invalid_num}')

done_searching = False
for i in range(0, invalid_ind - 1):
    for j in range(i + 1, invalid_ind):
        window = numbers[i:j + 1]
        if invalid_num == window.sum():
            print(f'Part 2: {window.max() + window.min()}')
            exit()
