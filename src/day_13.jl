#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON


function calc_happiness(seats, pairs)
    happiness = 0
    for i in 1:length(seats) - 1
        happiness += pairs[seats[i]][seats[i + 1]]
        happiness += pairs[seats[i + 1]][seats[i]]
    end
    happiness += pairs[seats[1]][seats[end]]
    happiness += pairs[seats[end]][seats[1]]

    return happiness
end

function add_person(seats, pairs, verbose::Int=0)
    if  length(seats) == length(keys(pairs))
        global part_1, part_2
        hap = calc_happiness(seats, pairs)
        if part_2 < hap && verbose >= 1
            println("New optimal arrangement: ", seats)
        end
        part_1 = max(part_1, hap)
        part_2 = max(part_2, hap)
    else
        for pair in keys(pairs)
            if !(pair in seats)
                add_person(push!(copy(seats), pair), pairs, verbose)
            end
        end
    end
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

    pairs = Dict{String, Dict}()
    inputs = readlines(open(data_path, "r"))
    for inp in inputs
        words = split(inp)
        host = words[1]
        recv = words[end][1:end-1]
        if words[3] == "lose"
            val = parse(Int, "-" * words[4])
        elseif words[3] == "gain"
            val = parse(Int, words[4])
        end

        if !(host in keys(pairs))
            pairs[host] = Dict{String, Int}(recv => val)
        else
            pairs[host][recv] = val
        end
    end
    
    global part_1 = 0
    global part_2 = 0
    add_person([], pairs, args["verbose"])
    pairs_2 = copy(pairs)
    pairs_2["Me"] = Dict{String, Int}()
    for key in keys(pairs)
        pairs_2["Me"][key] = 0
        pairs_2[key]["Me"] = 0
    end

    add_person([], pairs, args["verbose"])
    part_2 = 0
    add_person([], pairs_2, args["verbose"])

    @printf("Part 1: %d\n", part_1)
    @printf("Part 2: %d\n", part_2)
    
    return 0
end

main()
