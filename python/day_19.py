#!/usr/bin/env python3

from pathlib import Path
import click
import tqdm


class Rule:
    def __init__(self, key: int, rules: str, rules_dict, verbose=False):
        self.key = key
        self.rules = rules
        self.rules_dict = rules_dict
        self.verbose = verbose

        if '"' in self.rules:
            self.type = 1
            self.rules = self.rules.split('"')[1]
        elif '|' in self.rules:
            self.type = 2
        else:
            self.type = 3


    def check_match(self, message: str) -> bool:
        if len(message) == 0:
            message_remainder = ""
            return False, message_remainder
        message_remainder = message

        if self.type == 1:
            if len(message) > 0:
                if message[0] == self.rules:
                    message_remainder = message[1:]
                    return True, message_remainder
                else:
                    return False, message_remainder
            else:
                return True, message_remainder

        elif self.type == 2:
            if self.verbose:
                print(f'    Parsing Type 2: {self.rules}')
            opt1, opt2 = self.rules.split('|')
            for rule in opt1.split():
                if self.verbose:
                    print(f'        Going to rule {rule} for'
                          f' {message_remainder}')

                is_match, remainder = self.rules_dict[int(rule)].check_match(
                    message_remainder)

                if is_match:
                    message_remainder = remainder
                    if self.verbose:
                        print(f'        Rule {rule} returned'
                          f' {message_remainder}')
                else:
                    message_remainder = message
                    break
            # This handles the or. If the first solution worked, then the
            # remainder is either empty or shortened
            if message_remainder != message:
                return True, message_remainder

            if self.verbose:
                print(f'    Option {opt1} failed, trying {opt2}')
            for rule in opt2.split():
                if self.verbose:
                    print(f'        Going to rule {rule} for'
                          f' {message_remainder}')
                is_match, remainder = self.rules_dict[int(rule)].check_match(
                    message_remainder)
                if is_match:
                    message_remainder = remainder
                    if self.verbose:
                        print(f'        Rule {rule} returned'
                              f' {message_remainder}')
                else:
                    if self.verbose:
                        print(f'            Rule {rule} failed')
                    return False, message_remainder
            # Checks if the second option succeeded
            if message_remainder != message:
                return True, message_remainder
            else:
                raise ReferenceError("Inputs not solved, exiting")

        elif self.type == 3:
            if self.verbose:
                print(f'    Parsing Type 3: {self.rules}')
            rules = self.rules.split()
            for rule in rules:
                if self.verbose:
                    print('        Going to Rule {}'.format(rule))
                is_match, remainder = self.rules_dict[int(rule)].check_match(
                    message_remainder)
                if self.verbose:
                    print('        Rule {} returned {}'.format(
                        rule, remainder))
                if is_match:
                    message_remainder = remainder 

                else:
                    return False, message_remainder

            if message_remainder != message:
                return True, message_remainder
            else:
                return False, message_remainder
        raise ReferenceError("Inputs not solved, exiting")

    def __str__(self):
        return self.rules


@click.command()
@click.option("-v", "--verbose", is_flag=True)
@click.option("-t", "--test", is_flag=True)
def main(verbose, test):
    
    if not test:
        data_file = Path(__file__).absolute().parent.parent / 'dat/day_19.txt'
    else:
        data_file = Path(__file__).absolute().parent.parent / 'dat/day_19_test.txt'

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


    for k, rule in rules_dict.items():
        rules_dict[k] = Rule(k, rule, rules_dict, verbose)

    match_rule = rules_dict[0]
    print(f"There are {len(messages)} messages")
    valids_1 = []
    for message in messages:
        if verbose:
            print(f'# Solving for {message}')
        is_valid, remainder = match_rule.check_match(message)
        if is_valid and remainder == "":
            if verbose:
                print(f'{message} exited with {is_valid}')
            valids_1.append(is_valid)
        elif verbose:
            print(f'{message} exited with {remainder}')

    print(f'Part 1: {sum(valids_1)}')

    valids_2 = set()
    match_42 = rules_dict[42]
    match_31 = rules_dict[31]
    # rules_dict[8] = Rule(8, "42 | 42 8", rules_dict)
    # rules_dict[11] = Rule(11, "42 31 | 42 11 31", rules_dict)
    v0 = len(valids_2)
    for message in tqdm.tqdm(messages):
        if v0 + 2 == len(valids_2):
            print("Double count!")
        v0 = len(valids_2)
        message_0 = message
        # print(f'# Solving for {message}')
        count_42 = 0
        possible_matches = set()
        remainder = message
        keep_looping = True
        for i in range(1, len(message_0)+1):
            message_1 = message_0[:i]
            is_valid, remainder = match_42.check_match(message_1)
            count = 0
            while remainder != message:
                # print(message)
                message = remainder
                is_valid, remainder = match_42.check_match(message)
                if is_valid and remainder == "":
                    possible_matches.add((message_0[i:], count))
                count += 1
                
        # print(len(possible_matches))
        for match, count in possible_matches:
            is_valid, remainder = match_31.check_match(match)
            if is_valid and remainder == "":
                valids_2.add(message_0)
                break
            keep_looping = True
            count_2 = 0
            while keep_looping:
                # print(message)
                message = remainder
                is_valid, remainder = match_31.check_match(message)
                keep_looping = remainder != message
                if is_valid and remainder == "" and count_2 < count:
                    print(count_2, count)
                    valids_2.add(message_0)
                    keep_looping = False
                count_2 += 1
                
        

    print("\n".join(sorted(valids_2)))
    print(f'Part 2: {len(valids_2)}')

if __name__ == "__main__":
    main()
    