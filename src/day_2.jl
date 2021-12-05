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

    depth = 0
    depth_2 = 0
    dist = 0
    for line in inputs
        dir, val = split(line)
        val = parse(Int, val)

        if dir == "forward"
            dist += val
            depth_2 += depth * val
        elseif dir == "down"
            depth += val
        elseif dir == "up"
            depth -= val
            # depth = depth < 0 ? 0 : depth
        end
        println("Depth: ", depth_2, " Aim: ", depth, " Dist: ", dist)
    end

    part_1 = depth * dist
    @printf("Part 1: %d\n", part_1)
    part_2 = depth_2 * dist
    @printf("Part 2: %d\n", part_2)
end


main()
