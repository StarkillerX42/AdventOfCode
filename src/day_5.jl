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
    points = Array{Int, 3}(undef, length(inputs), 2, 2)
    for (i, line) in enumerate(inputs)
        left, right = split(line, " -> ")
        points[i, 1, 1] = parse(Int, split(left, ",")[1])
        points[i, 1, 2] = parse(Int, split(left, ",")[2])
        points[i, 2, 1] = parse(Int, split(right, ",")[1])
        points[i, 2, 2] = parse(Int, split(right, ",")[2])
    end

    println("There are ", length(inputs)[1], " lines")
    println("x Max: ", findmax(points[:, :, 1])[1], " y Max: ", findmax(points[:, :, 2])[1])
    println("x Min: ", findmin(points[:, :, 1])[1], " y Min: ", findmin(points[:, :, 2])[1])

    part_1_grid = fill!(Array{Int, 2}(undef, findmax(points[:, :, 1])[1] + 1, findmax(points[:, :, 2])[1] + 1), 0)
    part_2_grid = fill!(Array{Int, 2}(undef, findmax(points[:, :, 1])[1] + 1, findmax(points[:, :, 2])[1] + 1), 0)

    for i=1:size(points)[1]
        # println(i)
        jind = points[i, 1, 1] < points[i, 2, 1] ? 1 : -1
        jl = 0
        for j=points[i, 1, 1]:jind:points[i, 2, 1]
            # println("    ", j)
            kind = points[i, 1, 2] < points[i, 2, 2] ? 1 : -1
            kl = 0
            for k=points[i, 1, 2]:kind:points[i, 2, 2]
                # println("        ", k)
                # println(points[i, 1, 1] - points[i, 2, 1] == 0, points[i, 1, 2] - points[i, 2, 2] == 0)
                if (points[i, 1, 1] - points[i, 2, 1] == 0) | (points[i, 1, 2] - points[i, 2, 2] == 0)
                    # println("            ", j, ", ", k)
                    part_1_grid[j + 1, k + 1] += 1
                    part_2_grid[j + 1, k + 1] += 1
                elseif jl == kl
                    part_2_grid[j + 1, k + 1] += 1
                end
                kl += 1
            end
            jl += 1
        end
    end

    part_1 = 0
    part_2 = 0
    for i=1:size(part_1_grid)[1]
        for j=1:size(part_1_grid)[2]
            if part_1_grid[i, j] > 1
                part_1 += 1
            end
            if part_2_grid[i, j] > 1
                part_2 += 1
            end
        end
    end
    # println("Straight Lines: ", n_straight_lines, "/",length(inputs))
    @printf("Part 1: %d\n", part_1)
    @printf("Part 2: %d\n", part_2)
end

main()
