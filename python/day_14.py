#!/usr/bin/env python3

import numpy as np
from pathlib import Path

data_file = Path(__file__).absolute().parent.parent / 'dat/day_14.txt'
lines = data_file.open('r').readlines()


def mask_val(value: int, data_mask: str):
    bin_data = f'{value:0>36b}'
    result = ''
    for b, m in zip(bin_data, data_mask):
        result += b if m == 'X' else m
    return int(result, 2)


def mask_ind(value: int, data_mask: str):
    bin_data = f'{value:0>36b}'
    results = ['']
    for b, m in zip(bin_data, data_mask):
        if m == '0':
            for i, result in enumerate(results):
                results[i] += b
        elif m == '1':
            for i, result in enumerate(results):
                results[i] += m
        elif m == 'X':
            for i in range(len(results)):
                added = results[i] + '0'
                results.append(added)
                results[i] += '1'

    for i, result in enumerate(results):
        results[i] = int(result, 2)

    return results


verbose = False
mem_1 = {}
mem_2 = {}
mask = ''

for line in lines:
    if 'mask' in line:
        mask = line.strip().split(' = ')[-1]
        if verbose:
            print(f'Mask: {mask}')
    elif 'mem' in line:
        mem_key, val = line.strip().split(' = ')
        key = int(mem_key.strip(']').split('[')[-1])
        val = int(val)
        # print(type(key), type(read_mask(val, mask)))
        if verbose:
            print(f'Val : {mask_val(val, mask)}')
        masked_keys = mask_ind(key, mask)
        mem_1[key] = mask_val(val, mask)
        for k in masked_keys:
            mem_2[k] = val
    else:
        raise IOError(f'Unparsable line: {line}')

print(f'Part 1: {np.sum(list(mem_1.values()))}')
print(f'Part 2: {np.sum(list(mem_2.values()))}')
