#!/usr/bin/env julia
using Printf
using ArgParse


function parse_cmdline()
    parser = ArgParseSettings()

    @add_arg_table! parser begin
        "-v", "--verbose"
            help="Verbose debugging"
            action = :count_invocations
        "-t", "--test"
            help="Use test file"
            action = :store_true
    end
    return parse_args(parser)
end


function calc_distance(distances, path)
    distance = 0
    for i in 1:length(path) - 1
        distance += distances[path[i]][path[i + 1]]
    end
    return distance
end


function add_city(path, distances, verbose=false)
    if length(path) == length(keys(distances))
        global part_1
        global part_2
        new_dist = calc_distance(distances, path)
        # if part_1 > new_dist && verbose
            # println("New optimal solution of ", part_1, " via ", path)
        # end
        part_1 = min(part_1, new_dist)
        part_2 = max(part_2, new_dist)
    else
        for city in keys(distances)
            if !(city in path)
                add_city(push!(copy(path), city), distances, verbose)
            end
        end
    end
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
    
    fp = open(data_path, "r")
    distance_ascii = readlines(fp)
    distances = Dict()
    for distance in distance_ascii
        source, right = split(distance, " to ")
        dest, dist = split(right, " = ")
        if !(source in keys(distances))
            distances[source] = Dict(dest => parse(Int, dist))
        else
            distances[source][dest] = parse(Int, dist)
        end

        if !(dest in keys(distances))
            distances[dest] = Dict(source => parse(Int, dist))
        else
            distances[dest][source] = parse(Int, dist)
        end
    end

    global part_1 = 1000000
    global part_2 = 0
    add_city([], distances, args["verbose"])

    @printf("Part 1: %d\n", part_1)
    @printf("Part 2: %d\n", part_2)
end


main()

