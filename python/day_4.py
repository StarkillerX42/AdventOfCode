#!/usr/bin/env python3
import pprint
from pathlib import Path

data_file = Path('dat/day_4.txt')

verbose = False
required_keys = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')

entries = []
if data_file.exists():
    with data_file.open('r') as fil:
        person_data = {}
        for line in fil:
            line = line.strip('\n')
            key_pairs = line.split()
            for key_pair in key_pairs:
                key, val = key_pair.split(':')
                if verbose:
                    print(key, val)
                # if key in ('byr', 'iyr', 'cid', 'eyr', 'pid'):
                #     person_data[key] = int(val)
                # else:
                #     person_data[key] = val
                person_data[key] = val
            if line == '':
                if verbose:
                    print('Making a new user')
                person_data['valid'] = True
                entries.append(person_data)
                person_data = {}
else:
    print('Data unavailable')

if verbose:
    pprint.pprint(entries)

n_valid_1 = 0
n_valid_2 = 0

for entry in entries:
    keys = entry.keys()
    for k in required_keys:
        if k not in keys:
            entry['valid'] = False
    n_valid_1 += entry['valid']

    if not entry['valid']:
        continue

    if len(entry['byr']) != 4:
        entry['valid'] = False
    else:
        entry['byr'] = int(entry['byr'])

    if (entry['byr'] < 1920) or (entry['byr'] > 2002):
        entry['valid'] = False

    if len(entry['iyr']) != 4:
        entry['valid'] = False
    else:
        entry['iyr'] = int(entry['iyr'])

    if (entry['iyr'] < 2010) or (entry['iyr'] > 2020):
        entry['valid'] = False

    if len(entry['eyr']) != 4:
        entry['valid'] = False
    else:
        entry['eyr'] = int(entry['eyr'])

    if (entry['eyr'] < 2020) or (entry['eyr'] > 2030):
        entry['valid'] = False

    if 'cm' in entry['hgt']:
        hgt = int(entry['hgt'][:-2])
        if (hgt < 150) or (hgt > 193):
            entry['valid'] = False
    elif 'in' in entry['hgt']:
        hgt = int(entry['hgt'][:-2])
        if (hgt < 59) or (hgt > 76):
            entry['valid'] = False
    else:
        entry['valid'] = False

    if entry['hcl'][0] != '#':
        entry['valid'] = False
    elif len(entry['hcl']) != 7:
        entry['valid'] = False
    else:
        try:
            int('0x' + entry['hcl'][1:], 16)
        except ValueError:
            entry['valid'] = False

    if len(entry['ecl']) != 3:
        entry['valid'] = False
    else:
        if entry['ecl'] not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl',
                                'oth'):
            entry['valid'] = False

    if len(entry['pid']) != 9:
        entry['valid'] = False
    else:
        if entry['pid'] != f'{int(entry["pid"]):0>9.0f}':
            entry['valid'] = False

    n_valid_2 += entry['valid']


print(f'Part 1 valid entries: {n_valid_1}')

print(f'Part 2 valid entries: {n_valid_2}')
