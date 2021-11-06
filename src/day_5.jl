#!/usr/bin/env julia
using Printf

vowels = "aeiou"

project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
data_file = joinpath(project_dir, "dat/day_5.txt")
fp = open(data_file, "r")
master_list = readlines(fp)


function count_vowels(input::String)
    vowels = "aeiou"
    count = 0
    for i = 1:length(input)
        for j = 1:length(vowels)
            if input[i] == vowels[j]
                count += 1
            end
        end
    end
    return count
end

function back_to_back(input::String)
    last = input[1]
    passes = false
    for i = 2:length(input)
        if input[i] == last
            passes = true
        end
        last = input[i]
    end
    return passes
end


function check_forbidden(input::String)
    is_forbidden = false
    forbiddens = ["ab", "cd", "pq", "xy"]
    for i = 1:length(input) - 1
        for j = 1:length(forbiddens)
            if forbiddens[j] == input[i:i+1]
                is_forbidden = true
            end
        end
    end
    return is_forbidden
end


function check_separated_pairs(input::String)
    is_pair = false
    for i=1:length(input) -3
        matcher = input[i:i+1]
        for j=i+2:length(input) - 1
            if input[j:j+1] == matcher
                is_pair = true
                break
            end
        end
        if is_pair
            break
        end
    end
    return is_pair
end


function check_skip_match(input::String)
    skip_match = false
    matcher = input[1]
    for i=1:length(input)-2
        if input[i + 1] != matcher && input[i + 2] == matcher
            skip_match = true
            break
        end
        matcher = input[i + 1]
    end
    return skip_match
end


n_nice_1 = 0
n_nice_2 = 0
for i = 1:length(master_list)
    n_vowels = count_vowels(master_list[i])
    is_b2b = back_to_back(master_list[i])
    is_forbidden = check_forbidden(master_list[i])
    if (n_vowels >= 3) && is_b2b && !is_forbidden
        global n_nice_1 += 1
    end
    is_sep_pair = check_separated_pairs(master_list[i])
    is_skip_match = check_skip_match(master_list[i])
    if is_sep_pair && is_skip_match
        global n_nice_2 += 1
    end
end

@printf("Part 1: %d\n", n_nice_1)
@printf("Part 2: %d\n", n_nice_2)
