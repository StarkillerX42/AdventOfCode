#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON


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
    names = Array{String, 1}(undef, length(inputs))
    speeds = Array{Int, 1}(undef, length(inputs))
    sprint_t = Array{Int, 1}(undef, length(inputs))
    rest_t = Array{Int, 1}(undef, length(inputs))
    leads = fill!(Array{Int, 1}(undef, length(inputs)), 0)
    for (i, deer) in enumerate(inputs)
        words = split(deer)
        names[i] = words[1]
        speeds[i] = parse(Int, words[4])
        sprint_t[i] = parse(Int, words[7])
        rest_t[i] = parse(Int, words[end - 1])
    end
    distances = Array{Int, 1}(undef, length(inputs))
    t_tot = 2503
    for i = 1:length(inputs)
        dist = 0
        t_test = 0
        count = 0
        while t_test < t_tot && count < 1000
            dist += speeds[i] * sprint_t[i]
            t_test += sprint_t[i]
            if t_test < t_tot
                t_test += rest_t[i]
            else
                dist -= speeds[i] * (t_test - t_tot)
            end
            count += 1
        end
        distances[i] = dist
        if args["verbose"] >= 1
            println(names[i], " made it ", dist, " km")
        end

    end

    part_1 = findmax(distances)[1]

    @printf("Part 1: %d\n", part_1)

    positions = fill!(Array{Int, 1}(undef, length(names)), 0)
    last_rest = fill!(Array{Int, 1}(undef, length(names)), 0)
    leading = fill!(Array{Int, 1}(undef, length(names)), 0)
    for t = 1:t_tot
        for (j, deer) in enumerate(names)
            if t - sprint_t[j] <= last_rest[j]  # Sprinting
                positions[j] += speeds[j]
            elseif t >= last_rest[j] + sprint_t[j] + rest_t[j]
                last_rest[j] = t
            end
        end
        leader = findmax(positions)[1]
        for (j, deer) in enumerate(names)
            if positions[j] == leader
                leading[j] += 1
            end
        end
    end
    part_2 = findmax(leading)[1]
    @printf("Part 2: %d\n", part_2)
    return 0
end


main()
