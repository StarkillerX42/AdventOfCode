#!/usr/bin/env python3

import numpy as np
from pathlib import Path

data_file = Path('dat/day_10.txt')
jolts = np.loadtxt(data_file.as_posix(), dtype=int)
jolts = np.append([0, jolts.max() + 3], jolts)

verbose = True

jolts.sort()

steps = np.diff(jolts)
step_0 = np.sum(steps == 0)
step_1 = np.sum(steps == 1)
step_2 = np.sum(steps == 2)
step_3 = np.sum(steps == 3)
if np.any(steps > 3) or step_0:
    print('Invalid data')
if verbose:
    print(jolts)
    print(f'1 Jolt: {step_1}')
    print(f'2 Jolt: {step_2}')
    print(f'3 Jolt: {step_3}')
    print(f'Total: {step_1 + step_2 + step_3}')
print(f'Part 1: {step_1 * step_3}')


jolts = jolts[:-1]
ways_to_reach = [1] + ([0] * (len(jolts) - 1))
for i, jolt in enumerate(jolts):
    j = i + 1
    while j < len(jolts) and jolts[j] - jolt <= 3:
        print(i, j, ways_to_reach[i], ways_to_reach[j])
        ways_to_reach[j] += ways_to_reach[i]
        j += 1
    print(f'Part 2: {ways_to_reach[-1]}')
