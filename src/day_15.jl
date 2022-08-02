#!/usr/bin/env julia

using Printf
using ArgParse
using Dates
using JSON
using ProgressBars
using Statistics
using Combinatorics

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


function display_map(grid::Array{Int, 2}, path)
    point_path = path2points(path)
    for (i, v) in enumerate(grid)
        is_path = false
        for k in axes(point_path)[1]
            if (point_path[k, 1] % size(grid)[1] == i % size(grid)[1]
                && point_path[k, 2] == div(i - 1, size(grid)[1]) + 1)
                is_path = true
            end
        end
        if is_path
            printstyled("$(v) ", color=:red, bold=true)
        else
            printstyled("$(v) ")
        end
        if i % size(grid)[1] == 0
            print('\n')
        end
    end
    score = eval_path(grid, path)
    println("Score: $(score)")
    
end


function eval_path(grid::Array{Int, 2}, path, verbose::Int=0)
    if verbose >= 1
        println(path)
    end
    score = 0
    ptr = [1, 1]
    for d in path
        if d == 1
            ptr[1] += 1
        elseif d == 2
            ptr[2] -= 1
        elseif d == 3
            ptr[1] -= 1
        elseif d == 4
            ptr[2] += 1
        end
        if (ptr[1] > size(grid)[1]) || (ptr[2] > size(grid)[2])
            return -1
        end
        score += grid[ptr[1], ptr[2]]
        # println(grid[ptr[1], ptr[2]], ", (", ptr[1], ", ", ptr[2], ")")
    end
    if (ptr[1] != size(grid)[1]) || (ptr[2] != size(grid)[2])
        return -1
    end
    return score
end


function gen_path_candidates(path::Vector{Int}, attempted_paths::Vector
    )::Vector{Vector{Int}}
    candidates = []
    for (i, v) in enumerate(path[begin:end - 1])
        new_path = path
        if v == 1 && path[i + 1] == 4
            new_path = copy(path)
            new_path[i] = 4
            new_path[i + 1] = 1
        elseif v == 4 && path[i + 1] == 1
            new_path = copy(path)
            new_path[i] = 1
            new_path[i + 1] = 4
        end
        if new_path != path
            if !(new_path in attempted_paths)
                push!(candidates, new_path)
            end
        end
    end

    for (i, v) in enumerate(path[begin:end - 2])
        new_path = path
        if v == 1 && path[i + 1] == 4 && path[i + 1] == 4
            new_path = copy(path)
            new_path[i] = 4
            new_path[i + 1] = 4
            new_path[i + 2] = 1
        elseif v == 1 && path[i + 1] == 1 && path[i + 1] == 4
            new_path = copy(path)
            new_path[i] = 4
            new_path[i + 1] = 1
            new_path[i + 1] = 1
        end
        if new_path != path
            if !(new_path in attempted_paths)
                push!(candidates, new_path)
            end
        end
    end

    return candidates
end


function path2points(path)
    point_list = Array{Int, 2}(undef, length(path), 2)

    ptr = [1, 1]
    for (i, d) in enumerate(path)
        if d == 1
            ptr[1] += 1
        elseif d == 2
            ptr[2] -= 1
        elseif d == 3
            ptr[1] -= 1
        elseif d == 4
            ptr[2] += 1
        end
        point_list[i, :] = ptr
    end
    return point_list
end


function get_neighbors(point::Tuple{Int, Int}, is_frontier::BitMatrix)
    neighbors = []
    for p in [
        (point[1] - 1, point[2]),
        (point[1] + 1, point[2]),
        (point[1], point[2] - 1),
        (point[1], point[2] + 1)
        ]
        if (p[1] >= 1 && p[1] <= size(is_frontier)[1] && p[2] >= 1
            && p[2] <= size(is_frontier)[2]
            )
            if !is_frontier[p[1], p[2]]
                push!(neighbors, p)
            end
        end
    end
    return neighbors
end

function djikstra_solve_grid(grid, verbose::Int)
    nx, ny = size(grid)
    if verbose >= 1
        println("Array is of size $(nx)x$(ny)")
    end
    if verbose >= 3
        display_map(grid, [])
    end

    is_frontier = grid .!= 0
    efforts = Array{Int, 2}(undef, size(grid)[1], size(grid)[2])
    efforts[:, :] .= typemax(Int)
    efforts[1, 1] = 0
    is_frontier[1, 1] = 0
    is_exhausted = Array{Int, 2}(undef, size(grid)[1], size(grid)[2])
    is_exhausted .= 0
    all_frontier = efforts .!= -1
    no_frontier = .!all_frontier

    count = 0
    count_lim = 1000
    while any(is_frontier .== 1) && count < count_lim
        for (i, point) in enumerate(grid)
            x = (div(i - 1, ny) + 1)
            y = (i - 1) % nx + 1
            if is_exhausted[x, y] >= 5
                continue
            elseif length(get_neighbors((x, y), is_frontier)) != 0
                exhausted = true
                for neighbor in get_neighbors((x, y), no_frontier)
                    if is_frontier[neighbor[1], neighbor[2]]
                        exhausted = false
                    end
                end
                if exhausted
                    is_exhausted[x, y] += 1
                end
            end
            for neighbor in get_neighbors((x, y), is_frontier)
                efforts[x, y] = min(efforts[x, y],
                    efforts[neighbor[1], neighbor[2]] + grid[x, y]
                )
            end
        end
        is_frontier = efforts .== typemax(Int)
        if verbose >= 1 && count % 10 == 0
            complete = sum(is_frontier .== 0)
            total = length(is_frontier)
            completion = complete / total
            println("Djikstra Loop $count, $(completion*100)% complete")
        end
        if verbose >= 3 && count % 10 == 0
            display_map(efforts, [])
        end
        count += 1
    end
    if count == count_lim
        complete = sum(is_frontier .== 0)
        total = length(is_frontier)
        throw(ErrorException("Couldn't Reach solution, $complete/$total complete."))
    end
    return efforts
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

    grid = Array{Int, 2}(undef, length(lines), length(lines))
    for (i, line) in enumerate(lines)
        for (j, chr) in enumerate(line)
            grid[j, i] = parse(Int, chr)
        end
    end

    part_1_efforts = djikstra_solve_grid(grid, args["verbose"])
    part_1 = part_1_efforts[end, end]

    println("Part 1: $part_1")

    nx, ny = size(grid)

    grid_2 = Array{Int, 2}(undef, length(lines) * 5, length(lines) * 5)
    println("Filling Grid")
    for i in ProgressBar(0:4)
        for j in 0:4
            for (k, val) in enumerate(grid)
                x = i * nx + div(k - 1, ny) + 1
                y = j * ny + ((k - 1) % nx) + 1
                # println(x, ", ", y, " = ", val + i + j)
                grid_2[x, y] = val + i + j
            end
        end
    end
    # display_map(grid_2, [])
    grid_2 = (grid_2 .- 1) .% 9 .+ 1
    if args["verbose"] >= 2
        display_map(grid_2, [])
    end

    part_2_efforts = djikstra_solve_grid(grid_2, args["verbose"])
    part_2 = part_2_efforts[end, end]
    println("Part 2: $part_2")


end

main()
