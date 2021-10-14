#!/usr/bin/env python3

from pathlib import Path

data_file = Path(__file__).absolute().parent.parent / 'dat/day_19.txt'

rules_dict = {}
messages = []
with data_file.open('r') as fil:
    line = fil.readline()
    while_count = 0
    while ':' in line:
        line = line.strip('\n')
        k, rule = line.split(': ')
        k = int(k)
        rules_dict[k] = rule
        line = fil.readline()
        while_count += 1
        if while_count >= 1000:
            break

    line = fil.readline()
    while_count = 0
    while line:
        messages.append(line.strip('\n'))
        line = fil.readline()
        while_count += 1
        if while_count >= 1000:
            break


class Rule:
    def __init__(self, key: int, rules: str):
        self.key = key
        self.rules = rules

        if '"' in self.rules:
            self.type = 1
            self.rules = self.rules.split('"')[1]
        elif '|' in self.rules:
            self.type = 2
        else:
            self.type = 3

        self.message_remainder = ""

    def check_match(self, message: str) -> bool:
        if len(message) == 0:
            self.message_remainder = ""
            return False
        self.message_remainder = message

        if self.type == 1:
            if len(message) > 0:
                if message[0] == self.rules:
                    self.message_remainder = message[1:]
                    return True
                else:
                    return False
            else:
                return True

        elif self.type == 2:
            print(f'    Parsing Type 2: {self.rules}')
            opt1, opt2 = self.rules.split('|')
            for rule in opt1.split():
                print(f'        Going to rule {rule} for'
                      f' {self.message_remainder}')

                is_match = rules_dict[int(rule)].check_match(
                    self.message_remainder)


                if is_match:
                    self.message_remainder = rules_dict[
                        int(rule)].message_remainder
                    print(f'        Rule {rule} returned'
                          f' {self.message_remainder}')
                else:
                    self.message_remainder = message
                    break
            # This handles the or. If the first solution worked, then the
            # remainder is either empty or shortened
            if self.message_remainder != message:
                return True

            print(f'    Option {opt1} failed, trying {opt2}')
            for rule in opt2.split():
                print(f'        Going to rule {rule} for'
                      f' {self.message_remainder}')
                is_match = rules_dict[int(rule)].check_match(
                    self.message_remainder)
                if is_match:
                    self.message_remainder = rules_dict[
                        int(rule)].message_remainder
                    print(f'        Rule {rule} returned'
                          f' {self.message_remainder}')
                else:
                    print(f'            Rule {rule} failed')
                    return False
            # Checks if the second option succeeded
            if self.message_remainder != message:
                return True
            else:
                raise ReferenceError("Inputs not solved, exiting")

        elif self.type == 3:
            print(f'    Parsing Type 3: {self.rules}')
            rules = self.rules.split()
            for rule in rules:
                print('        Going to Rule {}'.format(rule))
                is_match = rules_dict[int(rule)].check_match(
                    self.message_remainder)
                print('        Rule {} returned {}'.format(
                    rule, rules_dict[int(rule)].message_remainder))
                if is_match:
                    self.message_remainder = rules_dict[
                        int(rule)].message_remainder

                else:
                    return False

            if self.message_remainder != message:
                return True
            else:
                return False
        raise ReferenceError("Inputs not solved, exiting")

    def __str__(self):
        return self.rules


for k, rule in rules_dict.items():
    rules_dict[k] = Rule(k, rule)

match_rule = rules_dict[0]

valids_1 = []
for message in messages:
    print(f'# Solving for {message}')
    is_valid = match_rule.check_match(message)
    if is_valid and match_rule.message_remainder == "":
        print(f'{message} exited with {is_valid}')
        valids_1.append(is_valid)
    else:
        print(f'{message} exited with {match_rule.message_remainder}')

print(f'Part 1: {sum(valids_1)}')

valids_2 = []
rules_dict[8] = Rule(8, "42 | 42 8")
rules_dict[11] = Rule(11, "42 31 | 42 11 31")
for message in messages:
    print(f'# Solving for {message}')
    is_valid = match_rule.check_match(message)
    if is_valid and match_rule.message_remainder == "":
        print(f'{message} exited with {is_valid}')
        valids_2.append(is_valid)
    else:
        print(f'{message} exited with {match_rule.message_remainder}')

print(f'Part 1: {sum(valids_2)}')
