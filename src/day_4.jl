#!/usr/bin/env julia

using MD5
using Printf

# input = "abcdef"  # test
input = "iwrupvqb"  # real

i = 1
part_1 = false
global part_1_i
global part_2_i
part_2 = false
while i < 10000000
    test_str = input * string(i)
    hash = md5(test_str)
    if hash[1] == 0 && hash[2] == 0 && hash[3] < 10 && !part_1
        global part_1 = true
        global part_1_i = i
    end
    if hash[1] == 0 && hash[2] == 0 && hash[3] == 0 && !part_2
        global part_2 = true
        global part_2_i = i
    end
    if part_1 && part_2 
        break
    end
    global i += 1
end
@printf("Part 1: %d\n", part_1_i)
@printf("Part 2: %d\n", part_2_i)
