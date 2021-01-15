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

    def check_match(self, message: str):
        message_remainder = message

        if self.type == 1:
            if message[0] == self.rules:
                return message[1:]
            else:
                return False

        elif self.type == 2:
            print(f'    Parsing Type 2: {self.rules}')
            opt1, opt2 = self.rules.split('|')
            for rule in opt1.split():
                print(f'        Going to rule {rule} for {message_remainder}')
                message_remainder = rules_dict[int(rule)].check_match(
                    message_remainder)
                print(f'        Rule {rule} returned {message_remainder}')
                if message_remainder == '':
                    return True
                elif message_remainder == False:
                    message_remainder = message
                    break
            # This handles the or. If the first solution worked, then the
            # remainder is either empty or shortened
            if message_remainder != message:
                return message_remainder
            print(f'    Option {opt1} failed, trying or')
            for rule in opt2.split():
                print(f'        Going to rule {rule} for {message_remainder}')
                message_remainder = rules_dict[int(rule)].check_match(
                    message_remainder)
                print(f'        Rule {rule} returned {message_remainder}')
                if message_remainder == '':
                    return True
                elif message_remainder == False:
                    message_remainder = message
            # Checks if the second option succeeded
            if message_remainder != message:
                return message_remainder
            else:
                return False

        elif self.type == 3:
            print(f'    Parsing Type 3: {self.rules}')
            rules = self.rules.split()
            for rule in rules:
                print('        Going to Rule {}'.format(rule))
                message_remainder = rules_dict[int(rule)].check_match(
                    message_remainder)
                print('        Rule {} returned {}'.format(rule, message_remainder))
                if (message_remainder == '') and (rule == rules[-1]):
                    return True
                elif message_remainder == '':
                    return False
                elif message_remainder is False:
                    return False

        if message_remainder:
            return False

    def __str__(self):
        return self.rules


for k, rule in rules_dict.items():
    rules_dict[k] = Rule(k, rule)

match_rule = rules_dict[0]

valids = []
for message in messages[:1]:
    print(f'# Solving for {message}')
    is_valid = match_rule.check_match(message)
    print(f'{message} exited with {is_valid}')
    valids.append(is_valid)

print(f'Part 1: {sum(valids)}')
