#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


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
    
    inputs = readlines(open(data_path, "r"))

    solution_str = """
        children: 3
        cats: 7
        samoyeds: 2
        pomeranians: 3
        akitas: 0
        vizslas: 0
        goldfish: 5
        trees: 3
        cars: 2
        perfumes: 1
        """
    solution = Dict{String, Int}()
    for line in split(solution_str, '\n')
        if length(line) == 0
            continue
        end
        name, value = split(line, ": ")
        solution[name] = parse(Int, value)
    end

    aunts = []
    for aunt in inputs
        words = split(aunt)
        this_sue = Dict{String, Int}(
            words[3][1:end-1] => parse(Int, words[4][1:end-1]),
            words[5][1:end-1] => parse(Int, words[6][1:end-1]),
            words[7][1:end-1] => parse(Int, words[8]),
        )
        push!(aunts, this_sue)
    end

    part_1 = 0
    part_2 = 0
    for (i, aunt) in enumerate(aunts)
        if args["verbose"] >= 1
            println(i)
        end
        is_match_1 = true
        is_match_2 = true
        for (key, val) in aunt
            if solution[key] != val
                if args["verbose"] >= 2
                    println("Match failed because of ", key)
                end
                is_match_1 = false
            end

            if key in ["cats", "trees"]
                if solution[key] >= val
                    is_match_2 = false
                end
            elseif key in ["pomeranians", "goldfish"]
                if solution[key] <= val
                    is_match_2 = false
                end
            else
                if solution[key] != val
                    is_match_2 = false
                end
            end
        end
        if is_match_1
            part_1 = i
        end
        if is_match_2
            part_2 = i
        end
    end
    @printf("Part 1: %d\n", part_1)
    @printf("Part 2: %d\n", part_2)

    return 0
end

main()
