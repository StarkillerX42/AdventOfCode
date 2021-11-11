#!/usr/bin/env julia

using Printf
using ArgParse
using Dates


function check_password(password, verbose=false)
    has_run = false
    hexpwd = collect(password)
    for i in 1:length(hexpwd) - 2
        if hexpwd[i] + 2 == hexpwd[i + 1] + 1== hexpwd[i + 2]
            has_run = true
        end
    end
    forbidden_chars = false
    if 'i' in password || 'o' in password || 'l' in password
        forbidden_chars = true
    end

    prev = ""
    first_pair = ""
    has_separate_pairs = false
    for char in password
        if prev == char && first_pair != char
            if first_pair == ""
                first_pair = char
            else
                has_separate_pairs = true
                break
            end
        end
        prev = char
    end
    if verbose
        @printf("Has run: %d, No forbidden characters: %d, Separate Pairs: %d" ,
            has_run, forbidden_chars, has_separate_pairs)
    end
    return has_separate_pairs && has_run
end


function next_password(password)
    pwd = collect(password)
    for i = length(pwd):-1:1
        if pwd[i] == 'z'
            pwd[i] = 'a'
        else
            pwd[i] += 1
            break
        end
    end
    return String(pwd)
end


function parse_cmdline()
    parser = ArgParseSettings()

    @add_arg_table! parser begin
        "-v", "--verbose"
            help="Verbose debugging"
            action = :count_invocations
        "-t", "--test"
            help="Use test file"
            action = :store_true
        # "count"
            # arg_type=Int
            # required = true
    end
    return parse_args(parser)
end


function main()
    args = parse_cmdline()
    path_parts = split(PROGRAM_FILE, "/")
    day = split(split(path_parts[length(path_parts)], "_")[2], ".")[1]
    project_dir = dirname(dirname(abspath(PROGRAM_FILE)))
    if !args["test"]
        data_path = joinpath(project_dir, "dat/day_" * day * ".txt")
    else
        data_path = joinpath(project_dir, "dat/day_" * day * "_test.txt")
    end
    
    if args["test"]
        println("hijklmmn: ", check_password("hijklmmn"))
        println("abbceffg: ", check_password("abbceffg"))
        println("abbcegjk: ", check_password("abbcegjk"))
        println("abcdefgh: ", check_password("abcdefgh"))
        println("abcdffaa: ", check_password("abcdffaa"))
        println(next_password("abcdffaa"))
        println(next_password("abcdffaz"))
        println(next_password("abcdfzz"))
    else
        old_pwd = "vzbxkghb"
        pwd = next_password(old_pwd)
        count = 0
        while !check_password(pwd) && count < 1000000
            pwd = next_password(pwd)
            count += 1
        end

        if check_password(pwd)
            @printf("Part 1: %s\n", pwd)
        else
            @printf("Couldn't find solution, stopped at %s\n", pwd)
        end

        count = 0
        pwd = next_password(pwd)
        while !check_password(pwd) && count < 1000000
            pwd = next_password(pwd)
            count += 1
        end

        if check_password(pwd)
            @printf("Part 2: %s\n", pwd)
        else
            @printf("Couldn't find solution, stopped at %s\n", pwd)
        end
    end

end

main()
