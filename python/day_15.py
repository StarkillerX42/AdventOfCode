#!/usr/bin/env python3

import datetime
import tqdm
import numpy as np
from pathlib import Path

data_file = Path(__file__).absolute().parent.parent / 'dat/day_15.txt'
numbers = [int(i) for i in data_file.open('r').readline().strip().split(',')]
numbers_dict = {}

i = 0
val = 0
for i, val in enumerate(numbers):
    numbers_dict[int(val)] = i
numbers_dict.pop(int(val))
num = int(val)
verbose = False

if verbose:
    print('Inputs:', numbers, len(numbers))
part_1 = np.nan
part_2 = np.nan

# for i, num in tqdm.tqdm(enumerate(numbers)):
lim = 30000000
t0 = datetime.datetime.now()
pbar = tqdm.tqdm(total=lim)
while i < lim:

    # print(i, num, numbers_dic)
    if i == 2020 - 1:
        print('Found 2020')
        part_1 = num
    elif i == lim - 1:
        print('Found 30,000,000')
        part_2 = num

    if num not in numbers_dict.keys():
        if verbose:
            print(f'{num} was new, saying 0')
        numbers_dict[num] = i
        num = 0
    else:
        diff = i - numbers_dict[num]
        if verbose:
            print(f'{num} was not new, saying {diff}')
        numbers_dict[num] = i
        num = diff

    i += 1
    if i % 100 == 0:
        pbar.update(100)


tf = datetime.datetime.now()
print(f'Time taken: {tf-t0, i}')
print(f'Part 1: {part_1}')
print(f'Part 2: {part_2}')
