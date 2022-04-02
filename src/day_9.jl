#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars


function check_point(point, map)
    if point[1] < 1 || point[1] > size(map)[1]
        return false
    elseif point[2] < 1 || point[2] > size(map)[2]
        return false
    elseif map[point[1], point[2]] < 9
        return true
    else
        return false
    end
end


function search_basin(loc, map)
    directions = [0 1; 1 0; -1 0; 0 -1]
    searching = true
    basin_points = []
    push!(basin_points, loc)
    # println(basin_points)
    while searching
        # println("basin_points: ", basin_points)
        n_points = length(basin_points)
        for point in basin_points
            # println(point, typeof(point))
            # println(directions)
            neighbors = directions .+ reshape(point, (1, 2))
            for neighbor in eachrow(neighbors)

                # println("neighbor: ", neighbor)
                # println(typeof(neighbor))
                if check_point(neighbor, map)
                    if !(neighbor in basin_points)
                        # println(typeof(neighbor))
                        push!(basin_points, neighbor)
                    end
                end
            end
        end
        if length(basin_points) == n_points
            searching = false
        end
    end
    # popfirst!(basin_points)
    return basin_points
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
    
    inputs = readlines(open(data_path, "r"))
    heights = Array{Int, 2}(undef, length(inputs), length(inputs[1]))
    for i=1:length(inputs)
        for j=1:length(inputs[1])
            heights[i, j] = parse(Int, inputs[i][j])
        end
    end

    part_1 = 0
    for i=1:size(heights)[1]
        for j=1:size(heights)[2]
            xlow = i > 1 ? i - 1 : i + 1
            xhi = i < size(heights)[1] ? i + 1 : i - 1
            ylow = j > 1 ? j - 1 : j + 1
            yhi = j < size(heights)[2] ? j + 1 : j - 1
            xneighbors = heights[xlow:2:xhi, j]
            yneighbors = heights[i, ylow:2:yhi]
            if heights[i, j] < findmin(vcat(xneighbors, yneighbors))[1]
                part_1 += heights[i, j] + 1
            end
        end
    end

    @printf("Part 1: %d\n", part_1)

    basins = []
    push!(basins, search_basin([1, 1], heights))
    push!(basins, search_basin([1, 10], heights))
    for i=1:size(heights)[1]
        for j in 1:size(heights)[2]
            in_basin = heights[i, j] == 9
            for basin in basins
                if [i, j] in basin
                    in_basin = true
                end
            end
            if !in_basin
                push!(basins, search_basin([i, j], heights))
            end
        end
    end

    large_basins = [0, 0, 0]
    for basin in basins
        added_basin = false
        for (i, bsize) in enumerate(large_basins)
            if length(basin) > bsize && !added_basin
                large_basins[i] = length(basin)
                added_basin = true
                large_basins = sort(large_basins)
            end
        end
    end
    @printf("Part 2: %d\n", prod(large_basins))



end
main()
