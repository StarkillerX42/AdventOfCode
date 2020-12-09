#!/usr/bin/env python3

from pathlib import Path
import textwrap

data_file = Path('dat/day_8.txt')
lines = data_file.open('r').readlines()

verbose = False

boot_code = []
for line in lines:
    line = line.strip('\n')
    cmd, val = line.split()
    val = int(val)
    boot_code.append([cmd, val])

# Part 1
history_1 = []
count = 0
accumulation = 0
i = 0
no_repeat = True
while no_repeat:
    history_1.append(i)
    cmd, val = boot_code[i]
    if cmd == 'acc':
        accumulation += val
        i += 1
    elif cmd == 'jmp':
        i += val
    elif cmd == 'nop':
        i += 1
    else:
        print('Issue encountered: ', cmd, val, i)
    if i == len(lines):
        print('Reached loop exit, terminating')
        break
    no_repeat = i not in history_1
    count += 1
    if count >= 1000:
        break

print(f'Part 1: {accumulation}')

all_swaps = []


class Node:
    def __init__(self, index, swap=0, accumulation=0, history=None):
        if history is None:
            history = []
        else:
            history = history.copy()
        self.i = index
        self.swap = swap
        self.accumulation = accumulation
        self.history = history + [self.i]

    def search(self):
        keep_going = True
        while_count = 0
        while keep_going:
            cmd, val = boot_code[self.i]
            prev_i = self.i
            self.history.append(self.i)
            if cmd == 'acc':
                self.accumulation += val
                self.i += 1
            elif cmd == 'jmp':
                if self.swap:
                    self.i += val
                elif self.i + 1 not in all_swaps:
                    if verbose:
                        print(f'Swapping at {self.i}')
                    new_swap = Node(self.i + 1, swap=self.i + 1,
                                    accumulation=self.accumulation,
                                    history=self.history.copy())
                    no_swap = Node(self.i + val, swap=self.swap,
                                   accumulation=self.accumulation,
                                   history=self.history.copy())
                    all_swaps.append(self.i + 1)
                    new_swap.search()
                    no_swap.search()
            elif cmd == 'nop':
                if self.swap:
                    self.i += 1
                elif self.i + 1 not in all_swaps:
                    new_swap = Node(self.i + val, swap=self.i + 1,
                                    accumulation=self.accumulation,
                                    history=self.history.copy())
                    no_swap = Node(self.i + 1, swap=self.swap,
                                   accumulation=self.accumulation,
                                   history=self.history.copy())

                    all_swaps.append(self.i + 1)
                    new_swap.search()
                    no_swap.search()
            else:
                raise ValueError(f'Unacceptable point reached at {self.i} with'
                                 f' command {cmd}')

            if self.i == len(boot_code):
                history = textwrap.fill(str(self.history + [len(boot_code)]),
                                        80, initial_indent=" " * 12,
                                        subsequent_indent=" " * 12)
                print(f'Solution found!\n'
                      f'    Swap Location: {self.swap}\n'
                      f'    History:\n{history}\n'
                      f'    Accumulation: {self.accumulation}')
                return
            elif self.i in self.history:
                return

            while_count += 1
            if while_count > 1000:
                break


init = Node(0)
init.search()
