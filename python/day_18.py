#!/usr/bin/env python3

import re
from pathlib import Path
from pprint import pprint

data_file = Path(__file__).absolute().parent.parent / 'dat/day_18_test.txt'

equations = []
with data_file.open('r') as fil:
    for line in fil:
        equations.append(line.strip())

verbose = True
if verbose:
    pprint(equations)


class NewMath:
    def __init__(self, eqn: str):
        self.equation_str_0 = eqn
        self.equation_str = eqn
        while '(' in self.equation_str:
            for exp in re.findall(r'\([0-9 +*]*\)', self.equation_str):
                exp_no_par = exp.rstrip(')').lstrip('(')
                eqn = NewMath(exp_no_par)
                self.equation_str = self.equation_str.replace(exp,
                                                              f'{eqn.value}')

        self.equation = self.equation_str.split()
        self.value = int(self.equation[0])
        operand = ''
        for item in self.equation[1:]:
            try:
                item = int(item)
                if operand == '+':
                    self.value += int(item)
                elif operand == '*':
                    self.value *= int(item)
            except ValueError:
                operand = item

    def __str__(self):
        return f'{self.equation_str_0}= {self.equation_str}= {self.value}'


class AdvancedMath(NewMath):
    """Part 2 solution"""
    def __init__(self, eqn: str):

        self.equation_str = eqn
        # an extra space on the right is important for the addition regex to
        # grab the whole number
        if self.equation_str[-1] != ' ':
            self.equation_str += ' '
        self.equation_str_0 = self.equation_str

        # print(f'Entering advanced math: {self.equation_str}')
        # Parenthesis order of operations
        while '(' in self.equation_str:
            for exp in re.findall(r'\([0-9 +*]*\)', self.equation_str):
                # print('Exp: .{}.'.format(exp))
                exp_no_par = exp.rstrip(')').lstrip('(')
                eqn = AdvancedMath(exp_no_par)
                # print('Subs: .{} .'.format(eqn.value))
                self.equation_str = self.equation_str.replace(exp,
                                                              f'{eqn.value}')
                # print(f'New eqn: .{self.equation_str}.')

        # Simplify each + to a single value until either none remain and only
        # multiplication is left or the equation is two operands "1 + 2 "
        self.equation = self.equation_str.split()
        if len(self.equation) != 3:
            # print(f'Entering while .{self.equation_str}.')
            while '+' in self.equation_str:
                for exp in re.findall(r'\d+ \+ \d+ ', self.equation_str):
                    # print('Exp: .{}.'.format(exp))
                    eqn = AdvancedMath(exp)
                    # print('Subs: .{} .'.format(eqn.value))
                    self.equation_str = self.equation_str.replace(exp,
                                                                  f'{eqn.value} ')
                    # print(f'New eqn: .{self.equation_str}.')

        # After either removing all addition and parenthesis or simplifying it
        # to only 2 values to add, solve the rest of the equation
        self.equation = self.equation_str.split()
        self.value = int(self.equation[0])
        operand = ''
        for item in self.equation[1:]:
            try:
                item = int(item)
                if operand == '+':
                    self.value += int(item)
                elif operand == '*':
                    self.value *= int(item)
            except ValueError:
                operand = item


total = 0
for equation in equations:
    m = NewMath(equation)
    if verbose:
        print(m)
        # print(f' = {m.value}')
    total += m.value

print(f'Part 1: {total}')

total_2 = 0
for equation in equations:
    m = AdvancedMath(equation + ' ')
    if verbose:
        print(m)
        # print(f' = {m.value}')
    total_2 += m.value

print(f'Part 2: {total_2}')


