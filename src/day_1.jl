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
    depths = Array{Int, 1}(undef, length(inputs))
    for i=1:length(depths)
        depths[i] = parse(Int, inputs[i])
    end

    prev = 1000000
    part_1 = 0
    for d in depths
        if d > prev
            part_1 += 1
        end
        prev = d
    end

    @printf("Part 1: %d\n", part_1)
    part_2 = 0
    prev = 1000000
    for i=1:length(depths) - 2
        # low = i > 2 ? i - 2 : 1
        # high = i < length(depths) ? i : length(depths)
        window = depths[i:i+2]
        cur = sum(window)
        if cur > prev
            part_2 += 1
        end
        prev = cur
    end

    @printf("Part 2: %d\n", part_2)

end

main()
