#!/usr/bin/env python3

import numpy as np
from pathlib import Path

data_file = Path(__file__).absolute().parent.parent / 'dat/day_17.txt'

i_state = []
with data_file.open('r') as f:
    for line in f:
        line = line.strip()
        i_state.append(list(line))
i_state_3 = np.array([i_state]) == '#'
i_state_4 = np.array([[i_state]]) == '#'


class Conway3D:
    """A 3D conway cube model
    """

    def __init__(self, initial_state, verbose=False, trim=True):
        self.state = initial_state
        self.verbose = verbose
        self.trim = trim

    def update(self):
        new_state = np.zeros(np.array(self.state.shape) + 2) == 1
        for i, layer in enumerate(new_state):
            for j, row in enumerate(layer):
                for k, val in enumerate(row):
                    low_lay = i - 2 if i >= 2 else 0
                    high_lay = (i + 1 if i <= self.state.shape[0]
                                else self.state.shape[0])
                    low_row = j - 2 if j >= 2 else 0
                    high_row = (j + 1 if j <= self.state.shape[1]
                                else self.state.shape[1])
                    low_col = k - 2 if k >= 2 else 0
                    high_col = (k + 1 if k <= self.state.shape[2]
                                else self.state.shape[2])
                    neighbors = self.state[low_lay: high_lay,
                                           low_row: high_row,
                                           low_col: high_col]
                    neighbors_sum = np.sum(neighbors)
                    current_state = False
                    if ((i > 0) and (j > 0) and (k > 0)
                            and (i <= self.state.shape[0])
                            and (j <= self.state.shape[1])
                            and (k <= self.state.shape[2])):
                        current_state = self.state[i - 1, j - 1, k - 1]
                        neighbors_sum -= self.state[i - 1, j - 1, k - 1]
                    if current_state and ((neighbors_sum == 2)
                                          or (neighbors_sum == 3)):
                        new_state[i, j, k] = True
                    elif (not current_state) and (neighbors_sum == 3):
                        new_state[i, j, k] = True
        if self.trim:
            if np.sum(new_state[0]) == 0:
                new_state = new_state[1:]
            if np.sum(new_state[-1]) == 0:
                new_state = new_state[0:-1]
            if np.sum(new_state[:, 0]) == 0:
                new_state = new_state[:, 1:]
            if np.sum(new_state[:, -1]) == 0:
                new_state = new_state[:, :-1]
            if np.sum(new_state[:, :, 0]) == 0:
                new_state = new_state[:, :, 1:]
            if np.sum(new_state[:, :, -1]) == 0:
                new_state = new_state[:, :, :-1]
        self.state = new_state

    def __str__(self):
        printable = np.zeros(self.state.shape).astype(str)
        printable[self.state] = '#'
        printable[~self.state] = '.'
        return str(printable)

    def update_for(self, n):
        for i in range(n):
            self.update()
            if self.verbose:
                print(self.count_state())

    def count_state(self):
        return np.sum(self.state)


class Conway4D(Conway3D):
    """A 4D conway cube model
    """

    def __init__(self, initial_state, verbose=False, trim=True):
        super().__init__(initial_state, verbose, trim)
        if len(self.state.shape) != 4:
            raise ValueError(f'Wrong number of dimensions in input'
                             f' {len(self.state.shape)}')

    def update(self):
        new_state = np.zeros(np.array(self.state.shape) + 2) == 1
        for i, layer in enumerate(new_state):
            for j, row in enumerate(layer):
                for k, col in enumerate(row):
                    for m, val in enumerate(col):
                        low_lay = i - 2 if i >= 2 else 0
                        high_lay = (i + 1 if i <= self.state.shape[0]
                                    else self.state.shape[0])
                        low_row = j - 2 if j >= 2 else 0
                        high_row = (j + 1 if j <= self.state.shape[1]
                                    else self.state.shape[1])
                        low_col = k - 2 if k >= 2 else 0
                        high_col = (k + 1 if k <= self.state.shape[2]
                                    else self.state.shape[2])
                        low_slc = m - 2 if m >= 2 else 0
                        high_slc = (m + 1 if m <= self.state.shape[3]
                                    else self.state.shape[3])
                        neighbors = self.state[low_lay: high_lay,
                                               low_row: high_row,
                                               low_col: high_col,
                                               low_slc: high_slc]
                        neighbors_sum = np.sum(neighbors)
                        current_state = False
                        if ((i > 0) and (j > 0) and (k > 0) and (m > 0)
                                and (i <= self.state.shape[0])
                                and (j <= self.state.shape[1])
                                and (k <= self.state.shape[2])
                                and (m <= self.state.shape[3])):
                            current_state = self.state[i - 1, j - 1,
                                                       k - 1, m - 1]
                            neighbors_sum -= self.state[i - 1, j - 1,
                                                        k - 1, m - 1]
                        if current_state and ((neighbors_sum == 2)
                                              or (neighbors_sum == 3)):
                            new_state[i, j, k, m] = True
                        elif (not current_state) and (neighbors_sum == 3):
                            new_state[i, j, k, m] = True
        if self.trim:
            if np.sum(new_state[0]) == 0:
                new_state = new_state[1:]
            if np.sum(new_state[-1]) == 0:
                new_state = new_state[0:-1]
            if np.sum(new_state[:, 0]) == 0:
                new_state = new_state[:, 1:]
            if np.sum(new_state[:, -1]) == 0:
                new_state = new_state[:, :-1]
            if np.sum(new_state[:, :, 0]) == 0:
                new_state = new_state[:, :, 1:]
            if np.sum(new_state[:, :, -1]) == 0:
                new_state = new_state[:, :, :-1]
            if np.sum(new_state[:, :, :, 0]) == 0:
                new_state = new_state[:, :, :, 1:]
            if np.sum(new_state[:, :, :, -1]) == 0:
                new_state = new_state[:, :, :, :-1]
        self.state = new_state


system = Conway3D(i_state_3, False, True)
# system.update()
system.update_for(6)
print(f'Part 1: {system.count_state()}')

system4 = Conway4D(i_state_4, False, True)
system4.update_for(6)
print(f'Part 2: {system4.count_state()}')
