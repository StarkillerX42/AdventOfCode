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
    
    inputs = readline(open(data_path, "r"))
    crab_poses = Array{Int, 1}(undef, count(==(','), inputs) + 1)
    for (i, pos) in enumerate(split(inputs, ','))
        crab_poses[i] = parse(Int, pos)
    end
    low = findmin(crab_poses)[1]
    high = findmax(crab_poses)[1]
    @printf("Crabs are between %d and %d\n", low, high)

    fits = Array{Int, 1}(undef, high - low + 1)
    fits_2 = Array{Int, 1}(undef, high - low + 1)
    for (i, val) in enumerate(low:high)
        fits[i] = sum(broadcast(abs, crab_poses .- val))
        vals = broadcast(abs, crab_poses .- val)
        vals = (vals .* (vals .+ 1)) .÷ 2
        fits_2[i] = sum(vals)
    end

    part_1 = findmin(fits)[1]

    @printf("Part 1: %d\n", part_1)

    part_2 = findmin(fits_2)[1]

    @printf("Part 2: %d\n", part_2)


end

main()
