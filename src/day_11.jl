#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


function printmat(mat::Array)
    b = IOBuffer()
    show(b, "text/plain", mat)
    println(String(take!(b)))
end


function timestep(octopode_grid::Array{Int, 2}, verbose=0)
    if verbose >= 2
        printmat(octopode_grid)
    end
    octopode_grid = octopode_grid .+ 1
    while count(>(9), octopode_grid) != 0
        for i=1:size(octopode_grid)[1]
            for j=1:size(octopode_grid)[2]
                if octopode_grid[i, j] > 9
                    ilow = i == 1 ? i : i - 1
                    ihigh = i == size(octopode_grid)[1] ? i : i + 1
                    jlow = j == 1 ? j : j - 1
                    jhigh = j == size(octopode_grid)[1] ? j : j + 1
                    for k=ilow:ihigh
                        for el=jlow:jhigh
                            if (k != i || j != el) && octopode_grid[k, el] != 0
                                octopode_grid[k, el] += 1
                            end
                        end
                    end
                    octopode_grid[i, j] = 0
                end
            end
        end
        if verbose >= 3
            println("Interim grid: ")
            printmat(octopode_grid)
        end
    end
    if verbose >= 2
        printmat(octopode_grid)
    end
    return octopode_grid
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
    lines = readlines(open(data_path, "r"))
    octopode = Array{Int, 2}(undef, length(lines[1]), length(lines))
    for (i, line) in enumerate(lines)
        for (j, c) in enumerate(line)
            octopode[i, j] = parse(Int, c)
        end
    end

    if args["verbose"] >= 1
        printmat(octopode)
    end

    part_1 = 0
    cond = true
    while_count = 0
    while cond
        octopode = timestep(octopode, args["verbose"])
        if while_count < 100
            part_1 += count(==(0), octopode)
        end
        while_count += 1
        cond = while_count < 1000 && count(==(0), octopode) < 100
    end

    @printf("Part 1: %d\n", part_1)

    @printf("Part 2: %d\n", while_count)
end


main()
